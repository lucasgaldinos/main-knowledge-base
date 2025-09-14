#!/usr/bin/env python3
"""
Source HTML Cleaner Script

Cleans Angular-style HTML sources from markdown files and converts them
to clean HTML or markdown format.

Usage:
    python3 clean_sources.py <input_file> [--output <output_file>] [--format html|markdown]
"""

import re
import argparse
import sys
from pathlib import Path


def extract_source_data(html_content):
    """Extract source data from complex HTML structure using regex."""
    sources = []

    # Find all href links
    href_pattern = r'href="(https?://[^"]+)"'
    href_matches = re.findall(href_pattern, html_content)

    # For each unique URL, extract associated data
    processed_urls = set()

    for url in href_matches:
        if url in processed_urls:
            continue
        processed_urls.add(url)

        # Find the section containing this URL
        url_section_pattern = rf'href="{re.escape(url)}".*?(?=href="|$)'
        url_match = re.search(url_section_pattern, html_content, re.DOTALL)

        if not url_match:
            continue

        section = url_match.group(0)

        # Extract favicon
        favicon_pattern = r'src="([^"]*faviconV2[^"]*)"'
        favicon_match = re.search(favicon_pattern, section)
        favicon = favicon_match.group(1) if favicon_match else ''

        # Extract domain name
        domain_pattern = r'class="display-name"[^>]*>([^<]+)'
        domain_match = re.search(domain_pattern, section)
        domain = domain_match.group(1).strip() if domain_match else ''

        # Extract title/subtitle
        title_pattern = r'class="sub-title"[^>]*>([^<]+(?:<[^>]+>[^<]*)*)'
        title_match = re.search(title_pattern, section)
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            # Clean up multiple whitespaces
            title = ' '.join(title.split())
        else:
            title = ''

        # Extract domain from URL if no domain found
        if not domain:
            domain_from_url = re.search(r'https?://([^/]+)', url)
            domain = domain_from_url.group(1) if domain_from_url else ''

        if url and (title or domain):
            sources.append({
                'url': url,
                'title': title or domain,
                'domain': domain,
                'favicon': favicon
            })

    return sources


def format_as_clean_html(sources):
    """Format sources as clean HTML."""
    html_parts = []

    for source in sources:
        if source['favicon']:
            html_parts.append(f'''
<a target="_blank" href="{source['url']}">
    <img class="favicon" src="{source['favicon']}">
    <span class="sub-title">{source['title']}</span>
    <span class="display-name">{source['domain']}</span>
</a>''')
        else:
            html_parts.append(f'''
<a target="_blank" href="{source['url']}">
    <span class="sub-title">{source['title']}</span>
    <span class="display-name">{source['domain']}</span>
</a>''')

    return '\n'.join(html_parts)


def format_as_markdown(sources):
    """Format sources as markdown links."""
    markdown_parts = []

    for source in sources:
        if source['favicon']:
            # Markdown with favicon
            markdown_parts.append(f"[![]({source['favicon']}) {source['title']} {source['domain']}]({source['url']})")
        else:
            # Simple markdown link
            markdown_parts.append(f"[{source['title']} - {source['domain']}]({source['url']})")

    return '\n'.join(markdown_parts)


def clean_sources_in_file(input_file, output_file=None, format_type='html'):
    """Clean sources in a markdown file."""
    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Read the file
    content = input_path.read_text(encoding='utf-8')

    # Find the sources section (between ## Sources and end of file or next section)
    sources_pattern = r'(## Sources.*?)(?=\n## |\Z)'
    sources_match = re.search(sources_pattern, content, re.DOTALL)

    if not sources_match:
        print("No sources section found in the file.")
        return False

    sources_section = sources_match.group(1)

    # Extract HTML content from the sources section
    html_pattern = r'<deep-research-source-lists.*?</deep-research-source-lists>'
    html_match = re.search(html_pattern, sources_section, re.DOTALL)

    if not html_match:
        print("No HTML sources found in the sources section.")
        return False

    html_content = html_match.group(0)

    # Extract source data
    sources = extract_source_data(html_content)

    if not sources:
        print("No valid sources extracted from HTML.")
        return False

    print(f"Extracted {len(sources)} sources")

    # Format sources
    if format_type == 'markdown':
        formatted_sources = format_as_markdown(sources)
    else:
        formatted_sources = format_as_clean_html(sources)

    # Replace the complex HTML with clean format
    new_sources_section = f"## Sources\n\n{formatted_sources}\n"
    new_content = content.replace(sources_match.group(0), new_sources_section)

    # Write output
    output_path = Path(output_file) if output_file else input_path
    output_path.write_text(new_content, encoding='utf-8')

    print(f"Sources cleaned and saved to: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description='Clean Angular-style HTML sources in markdown files')
    parser.add_argument('input_file', help='Input markdown file')
    parser.add_argument('--output', '-o', help='Output file (default: overwrite input)')
    parser.add_argument('--format', '-f', choices=['html', 'markdown'], default='html',
                        help='Output format (default: html)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    try:
        success = clean_sources_in_file(args.input_file, args.output, args.format)
        if success:
            print("Sources cleaned successfully!")
            sys.exit(0)
        else:
            print("Failed to clean sources.")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
