# High-throughput Python strategies for asynchronous LaTeX/TeX processing and PDF conversion of arXiv papers

This research report outlines production-grade design patterns for processing arXiv papers at scale using Python's asynchronous and parallel computing primitives.

## Executive Summary

The workload covers: discovering arXiv items, downloading source tarballs and/or PDFs, extracting and normalizing TeX projects, compiling to PDF with latexmk/pdflatex/xelatex, optional post-processing (compression, OCR, text extraction), and persisting artifacts and logs.

**High-level recommendation: Use a hybrid concurrency model:**

- Use asyncio + async/await for all network and disk I/O (httpx + aiofiles), with strict rate limiting and backpressure
- Use asyncio subprocesses for LaTeX compilation and other external tool invocations (latexmk, ghostscript, qpdf, pdftotext), which sidestep GIL concerns
- Use ProcessPoolExecutor (concurrent.futures) for CPU-bound in-Python tasks (e.g., PDF parsing with pure Python libraries) and ThreadPoolExecutor only for the occasional small blocking call where process overhead is unjustified
- Bound concurrency by CPU and memory, not just by task count; LaTeX compiles are both CPU- and disk-heavy

## Key Architecture Principles

### 1. Workload Characterization: I/O vs CPU

**I/O-bound stages:**

- HTTP fetches (metadata, PDFs, source tarballs)
- Sequential file writes (download streams)
- Reading/writing many small files during TeX compilation

**CPU-bound stages:**

- LaTeX engine runs (pdflatex/xelatex/lualatex) - external processes, GIL doesn't apply
- Compression (ghostscript/qpdf), OCR (tesseract), PDF parsing, checksum hashing, decompression

**Contention hotspots:**

- Disk: many concurrent LaTeX compiles cause seeks and cache churn
- Memory: TeX plus spawned tools can use hundreds of MB per job

### 2. Pipeline Architecture

```
Stage A: Discovery → Stage B: Download → Stage C: Extract/Normalize → 
Stage D: Compile → Stage E: Post-process → Stage F: Persist/Index
```

### 3. Async Network I/O with httpx

```python
# Key patterns:
- One shared AsyncClient per worker process, enable HTTP/2
- Conservative timeouts (connect, read, write, pool)
- Global token bucket or asyncio.Semaphore for rate limiting
- Retry policy with capped exponential backoff
- Stream with response.aiter_bytes() to avoid memory spikes
```

### 4. LaTeX Compilation Orchestration

```python
# Core pattern:
await asyncio.create_subprocess_exec(
    "latexmk", "-pdf", "-interaction=nonstopmode", 
    "-halt-on-error", "-file-line-error",
    f"-outdir={out_dir}", f"-auxdir={out_dir}", main_tex
)
```

**Key features:**

- Containerize TeX: use pinned TeX Live Docker image
- Security: sandbox with no network, read-only TEXMF, resource limits
- Reproducibility: pin environment, disable shell-escape by default

### 5. Concurrency Control

**Recommended limits:**

- Network: ~5-10 concurrent requests per process
- Compilation: N ≈ min(physical_cores/2, memory-based cap), start with 2-4
- Post-processing: size to remaining CPU headroom

### 6. Performance Optimization Patterns

**Caching:**

- HTTP: ETag/Last-Modified validations
- latexmk: reuse .fdb_latexmk files for incremental builds
- Persistent TEXMF trees and font caches

**Infrastructure:**

- Use local NVMe for tmp dirs
- Mount tmpfs for auxiliary directories if memory allows
- uvloop on Linux for event loop improvements

### 7. Security Model for Untrusted TeX

**Isolation:**

- Run compiles in containers with no network, read-only TEXMF
- seccomp profile blocking dangerous syscalls
- CPU/memory limits, wall-clock timeout, FS quotas per job

**Input Sanitation:**

- Validate archive paths and encodings
- Reject suspicious constructs, limit file counts and sizes
- Default to -no-shell-escape

## Implementation Priority Checklist

**Top Priorities:**

1. ✅ Core hybrid engine (asyncio + httpx + aiofiles + asyncio subprocess)
2. ✅ Constrain compile concurrency (start with 2-4 per machine)
3. ✅ Reproducible environment (containerized TeX Live)
4. ✅ Security (sandbox compiles, no shell-escape default)
5. ✅ Caching and idempotency (persist HTTP artifacts, reuse latexmk state)
6. ✅ Observability (structured logging, metrics)

**Next-level improvements:**

- Prewarming caches and tmpfs for aux/out dirs
- uvloop on Linux for marginal gains
- Global cluster-aware rate limiting for horizontal scaling
- Resource-aware scheduler accounting for memory/disk pressure
- Automated remediation with limited package install from pinned TeX Live repo

## Example Code Patterns

### Async Download with Rate Limiting

```python
import asyncio
import httpx
import aiofiles

class RateLimiter:
    def __init__(self, rate_per_sec: float):
        self._interval = 1.0 / rate_per_sec
        self._lock = asyncio.Lock()
        self._last = 0.0

    async def acquire(self):
        async with self._lock:
            now = asyncio.get_running_loop().time()
            wait = max(0.0, self._last + self._interval - now)
            if wait:
                await asyncio.sleep(wait)
            self._last = asyncio.get_running_loop().time()

async def download_stream(client, url, dest, limiter, max_retries=4):
    backoff = 1.0
    for attempt in range(max_retries):
        await limiter.acquire()
        try:
            async with client.stream("GET", url, follow_redirects=True) as resp:
                resp.raise_for_status()
                async with aiofiles.open(dest + ".part", "wb") as f:
                    async for chunk in resp.aiter_bytes(chunk_size=131072):
                        await f.write(chunk)
            await asyncio.to_thread(os.replace, dest + ".part", dest)
            return dest
        except (httpx.HTTPError, httpx.ReadTimeout) as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 8.0)
```

### Pipeline with TaskGroups (Python 3.11+)

```python
async def pipeline(arxiv_ids: list[str]):
    download_q = asyncio.Queue(maxsize=100)
    extract_q = asyncio.Queue(maxsize=50)
    compile_q = asyncio.Queue(maxsize=20)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer())
        for _ in range(3):
            tg.create_task(downloader())
        tg.create_task(extractor())
        for _ in range(2):
            tg.create_task(compiler())
```

## Conclusions

The most robust pattern for large-scale arXiv TeX-to-PDF processing is a hybrid approach that:

- Drives workflow with asyncio for I/O concurrency
- Leverages httpx and aiofiles for efficient networking and disk streaming
- Pushes heavy lifting into external processes (latexmk/TeX engines, ghostscript/poppler)
- Uses ProcessPoolExecutor for CPU-bound pure-Python code when necessary

This sidesteps the GIL for expensive operations, maintains backpressure and rate limits, and keeps the system responsive and scalable.

**Success factors:**

- Bound concurrency by actual resources
- Rigorous sandboxing for untrusted inputs
- Strong caching strategies
- First-class observability
- Favor systemic performance levers over micro-optimizations
- Emphasize correctness, reproducibility, and safety

Research date: September 6, 2025
