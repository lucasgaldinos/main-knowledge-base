#!/usr/bin/env python3
"""
Academic Knowledge Base Database Setup
=====================================

Initializes SQLite databases for research data management with proper schema,
indexes, and foreign key constraints for academic workflow optimization.

Usage:
    python3 setup_databases.py

Databases Created:
    - knowledge.db: Research findings and academic content
    - analytics.db: Tool usage patterns and performance metrics  
    - citations.db: Academic references and bibliographic data
    - workflows.db: Research process and lifecycle tracking
"""

import sqlite3
import os
from pathlib import Path
from datetime import datetime

# Database file paths
DB_DIR = Path(__file__).parent
DATABASES = {
    'knowledge': DB_DIR / 'knowledge.db',
    'analytics': DB_DIR / 'analytics.db', 
    'citations': DB_DIR / 'citations.db',
    'workflows': DB_DIR / 'workflows.db'
}

def create_knowledge_db(db_path):
    """Create knowledge database with research content tracking."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Research content table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            methodology TEXT,
            confidence_level TEXT CHECK(confidence_level IN ('high', 'medium', 'low')),
            status TEXT CHECK(status IN ('draft', 'in-review', 'published', 'deprecated', 'archived')),
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL,
            file_path TEXT,
            citation_count INTEGER DEFAULT 0,
            validation_sources TEXT,
            UNIQUE(title, file_path)
        )
    """)
    
    # Research categories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            parent_category INTEGER,
            FOREIGN KEY (parent_category) REFERENCES categories(id)
        )
    """)
    
    # Content-category relationships
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_categories (
            content_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (content_id, category_id),
            FOREIGN KEY (content_id) REFERENCES research_content(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    
    # Create indexes for performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_status ON research_content(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_confidence ON research_content(confidence_level)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_created ON research_content(created_date)")
    
    conn.commit()
    conn.close()
    print(f"✅ Knowledge database created: {db_path}")

def create_analytics_db(db_path):
    """Create analytics database for tool usage and performance tracking."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Tool usage logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tool_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            execution_time REAL,
            success BOOLEAN NOT NULL,
            error_message TEXT,
            context TEXT,
            parameters TEXT,
            timestamp TEXT NOT NULL,
            user_session TEXT
        )
    """)
    
    # Performance metrics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            avg_execution_time REAL,
            success_rate REAL,
            usage_count INTEGER,
            last_updated TEXT NOT NULL,
            UNIQUE(tool_name)
        )
    """)
    
    # Workflow patterns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workflow_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_name TEXT NOT NULL,
            tool_sequence TEXT NOT NULL,
            frequency INTEGER DEFAULT 1,
            avg_completion_time REAL,
            success_rate REAL,
            last_seen TEXT NOT NULL
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tool_usage_name ON tool_usage(tool_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tool_usage_timestamp ON tool_usage(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tool_usage_success ON tool_usage(success)")
    
    conn.commit()
    conn.close()
    print(f"✅ Analytics database created: {db_path}")

def create_citations_db(db_path):
    """Create citations database for academic reference management."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Academic papers and sources
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation_key TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            year INTEGER,
            journal TEXT,
            volume TEXT,
            pages TEXT,
            doi TEXT,
            url TEXT,
            arxiv_id TEXT,
            citation_type TEXT CHECK(citation_type IN ('journal', 'conference', 'book', 'thesis', 'preprint', 'web')),
            added_date TEXT NOT NULL,
            last_accessed TEXT,
            notes TEXT
        )
    """)
    
    # Citation usage tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citation_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation_id INTEGER NOT NULL,
            content_file TEXT NOT NULL,
            usage_context TEXT,
            usage_date TEXT NOT NULL,
            FOREIGN KEY (citation_id) REFERENCES citations(id)
        )
    """)
    
    # Research topics/keywords
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)
    
    # Citation-topic relationships
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citation_topics (
            citation_id INTEGER,
            topic_id INTEGER,
            relevance_score REAL DEFAULT 1.0,
            PRIMARY KEY (citation_id, topic_id),
            FOREIGN KEY (citation_id) REFERENCES citations(id),
            FOREIGN KEY (topic_id) REFERENCES research_topics(id)
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_citations_key ON citations(citation_key)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_citations_year ON citations(year)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_citations_type ON citations(citation_type)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_file ON citation_usage(content_file)")
    
    conn.commit()
    conn.close()
    print(f"✅ Citations database created: {db_path}")

def create_workflows_db(db_path):
    """Create workflows database for research process tracking."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Research projects
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT UNIQUE NOT NULL,
            description TEXT,
            status TEXT CHECK(status IN ('active', 'completed', 'on-hold', 'archived')),
            start_date TEXT NOT NULL,
            end_date TEXT,
            primary_researcher TEXT,
            collaborators TEXT,
            project_path TEXT
        )
    """)
    
    # Workflow steps/phases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workflow_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            step_name TEXT NOT NULL,
            step_order INTEGER NOT NULL,
            description TEXT,
            tools_used TEXT,
            start_time TEXT,
            end_time TEXT,
            status TEXT CHECK(status IN ('pending', 'in-progress', 'completed', 'blocked')),
            output_files TEXT,
            notes TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
    """)
    
    # Methodology documentation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS methodologies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            methodology_name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            steps TEXT NOT NULL,
            tools_required TEXT,
            expected_outputs TEXT,
            validation_criteria TEXT,
            created_date TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0
        )
    """)
    
    # Project-methodology relationships
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_methodologies (
            project_id INTEGER,
            methodology_id INTEGER,
            adaptation_notes TEXT,
            PRIMARY KEY (project_id, methodology_id),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (methodology_id) REFERENCES methodologies(id)
        )
    """)
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_workflow_project ON workflow_steps(project_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_workflow_status ON workflow_steps(status)")
    
    conn.commit()
    conn.close()
    print(f"✅ Workflows database created: {db_path}")

def initialize_default_data():
    """Insert default categories, methodologies, and reference data."""
    
    # Initialize knowledge categories
    knowledge_conn = sqlite3.connect(DATABASES['knowledge'])
    cursor = knowledge_conn.cursor()
    
    default_categories = [
        ('AI and Machine Learning', 'Artificial intelligence research and applications'),
        ('Academic Research', 'Research methodologies and academic practices'),
        ('Tool Documentation', 'Software tools and technical documentation'),
        ('Data Science', 'Data analysis and statistical methods'),
        ('Software Engineering', 'Programming and development practices')
    ]
    
    cursor.executemany(
        "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
        default_categories
    )
    knowledge_conn.commit()
    knowledge_conn.close()
    
    # Initialize default methodologies
    workflows_conn = sqlite3.connect(DATABASES['workflows'])
    cursor = workflows_conn.cursor()
    
    default_methodologies = [
        (
            'Systematic Literature Review',
            'Comprehensive review of academic literature on a specific topic',
            '1. Define research question\n2. Search academic databases\n3. Screen and select papers\n4. Extract and synthesize data\n5. Document findings',
            'mcp_arxiv-mcp-ser_search_arxiv, mcp_google-schola_search_google_scholar_advanced, mcp_deep-research_deep-research',
            'Literature review document, citation database, synthesis report',
            'Minimum 20 relevant papers, peer review of methodology, external validation'
        ),
        (
            'Tool Documentation Enhancement',
            'Systematic enhancement of technical documentation with external validation',
            '1. Analyze existing documentation\n2. Research current practices\n3. Validate with external sources\n4. Enhance content\n5. Document methodology',
            'read_file, vscode-websearchforcopilot_webSearch, get_vscode_api, replace_string_in_file',
            'Enhanced documentation, completion report, validation sources',
            'External validation from 3+ authoritative sources, measurable improvement metrics'
        )
    ]
    
    cursor.executemany(
        "INSERT OR IGNORE INTO methodologies (methodology_name, description, steps, tools_required, expected_outputs, validation_criteria) VALUES (?, ?, ?, ?, ?, ?)",
        default_methodologies
    )
    workflows_conn.commit()
    workflows_conn.close()
    
    print("✅ Default data initialized")

def main():
    """Main setup function."""
    print("🔧 Setting up Academic Knowledge Base Databases")
    print("=" * 50)
    
    # Create database directory if it doesn't exist
    DB_DIR.mkdir(exist_ok=True)
    
    # Create each database
    create_knowledge_db(DATABASES['knowledge'])
    create_analytics_db(DATABASES['analytics'])
    create_citations_db(DATABASES['citations'])
    create_workflows_db(DATABASES['workflows'])
    
    # Initialize with default data
    initialize_default_data()
    
    print("\n🎉 Database setup complete!")
    print(f"📁 Databases created in: {DB_DIR}")
    print("\nNext steps:")
    print("1. Run backup script: scripts/backup-databases.sh")
    print("2. Configure automation: scripts/yaml-frontmatter-enforcer.py")
    print("3. Test database connectivity with sample queries")

if __name__ == "__main__":
    main()
