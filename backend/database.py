import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dar_agrovet.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Search Tasks
    cur.execute('''
    CREATE TABLE IF NOT EXISTS search_tasks (
        search_task_id TEXT PRIMARY KEY,
        category TEXT,
        district TEXT,
        area TEXT,
        search_term TEXT,
        source TEXT,
        status TEXT,
        results_found INTEGER DEFAULT 0,
        date_completed TEXT
    )
    ''')
    
    # 2. Raw Records
    cur.execute('''
    CREATE TABLE IF NOT EXISTS raw_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_type TEXT,
        source_id TEXT,
        source_url TEXT,
        query_used TEXT,
        search_task_id TEXT,
        raw_payload TEXT,
        extracted_at TEXT
    )
    ''')
    
    # 3. Master Businesses
    cur.execute('''
    CREATE TABLE IF NOT EXISTS master_businesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_name TEXT NOT NULL,
        normalized_business_name TEXT NOT NULL,
        category TEXT NOT NULL,
        secondary_categories TEXT,
        confidence TEXT DEFAULT 'MEDIUM',
        evidence TEXT,
        verification_status TEXT DEFAULT 'VERIFIED',
        exclusion_reason TEXT,
        district TEXT,
        ward_or_area TEXT,
        street_or_address TEXT,
        latitude REAL,
        longitude REAL,
        phone TEXT,
        alternative_phone TEXT,
        whatsapp TEXT,
        email TEXT,
        website TEXT,
        facebook TEXT,
        instagram TEXT,
        description TEXT,
        notes TEXT,
        hotspot_cluster TEXT DEFAULT 'GENERAL_METROPOLITAN',
        source_urls TEXT,
        source_types TEXT,
        duplicate_status TEXT DEFAULT 'UNIQUE',
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    
    # Check if migration needed for existing db
    cur.execute("PRAGMA table_info(master_businesses)")
    cols = [r[1] for r in cur.fetchall()]
    if 'hotspot_cluster' not in cols:
        cur.execute("ALTER TABLE master_businesses ADD COLUMN hotspot_cluster TEXT DEFAULT 'GENERAL_METROPOLITAN'")
    
    # 4. Usage Log
    cur.execute('''
    CREATE TABLE IF NOT EXISTS usage_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        actor_or_api TEXT,
        query TEXT,
        records_returned INTEGER,
        estimated_cost REAL,
        timestamp TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema initialized successfully at", DB_PATH)
