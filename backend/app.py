import os
import sqlite3
import json
import csv
import io
from fastapi import FastAPI, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dar_agrovet.db")
EXCEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "Dar_Es_Salaam_Agrovet_Database.xlsx")
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

app = FastAPI(title="Dar es Salaam Agrovet Database API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query_businesses(search=None, district=None, area=None, category=None, status="VERIFIED", source=None, cluster=None):
    conn = get_db()
    cur = conn.cursor()
    
    sql = "SELECT * FROM master_businesses WHERE 1=1"
    params = []
    
    if status and status != 'ALL':
        sql += " AND verification_status = ?"
        params.append(status)
        
    if district and district != 'ALL':
        sql += " AND district = ?"
        params.append(district)
        
    if area and area != 'ALL':
        sql += " AND ward_or_area = ?"
        params.append(area)

    if cluster and cluster != 'ALL':
        sql += " AND hotspot_cluster = ?"
        params.append(cluster)
        
    if category and category != 'ALL':
        sql += " AND (category = ? OR secondary_categories LIKE ?)"
        params.append(category)
        params.append(f"%{category}%")
        
    if source and source != 'ALL':
        sql += " AND source_types LIKE ?"
        params.append(f"%{source}%")
        
    if search:
        search_pattern = f"%{str(search).strip()}%"
        sql += " AND (business_name LIKE ? OR street_or_address LIKE ? OR phone LIKE ? OR description LIKE ?)"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
        
    sql += " ORDER BY district, ward_or_area, business_name"
    cur.execute(sql, params)
    rows = cur.fetchall()
    
    results = []
    for r in rows:
        item = dict(r)
        try:
            item['secondary_categories'] = json.loads(item.get('secondary_categories') or '[]')
        except Exception:
            item['secondary_categories'] = []
        try:
            item['source_urls'] = json.loads(item.get('source_urls') or '[]')
        except Exception:
            item['source_urls'] = []
        try:
            item['source_types'] = json.loads(item.get('source_types') or '[]')
        except Exception:
            item['source_types'] = []
            
        lat = item.get('latitude')
        lon = item.get('longitude')
        item['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else None
        results.append(item)
        
    conn.close()
    return results

@app.get("/api/stats")
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE verification_status = 'VERIFIED'")
    total_verified = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE category = 'AGROVET' AND verification_status = 'VERIFIED'")
    total_agrovet = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE category IN ('VETERINARY_SHOP', 'VETERINARY_PHARMACY', 'VETERINARY_SERVICE') AND verification_status = 'VERIFIED'")
    total_vet = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE category IN ('ANIMAL_FEED', 'POULTRY_FEED', 'POULTRY_SUPPLIES') AND verification_status = 'VERIFIED'")
    total_feed = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE verification_status = 'NEEDS_REVIEW'")
    total_review = cur.fetchone()[0]
    
    cur.execute('''
        SELECT district, COUNT(*) as count 
        FROM master_businesses 
        WHERE verification_status = 'VERIFIED' 
        GROUP BY district ORDER BY count DESC
    ''')
    by_district = {r['district']: r['count'] for r in cur.fetchall()}
    
    cur.execute('''
        SELECT category, COUNT(*) as count 
        FROM master_businesses 
        WHERE verification_status = 'VERIFIED' 
        GROUP BY category ORDER BY count DESC
    ''')
    by_category = {r['category']: r['count'] for r in cur.fetchall()}

    cur.execute('''
        SELECT hotspot_cluster, COUNT(*) as count 
        FROM master_businesses 
        WHERE verification_status = 'VERIFIED' 
        GROUP BY hotspot_cluster ORDER BY count DESC
    ''')
    by_cluster = {r['hotspot_cluster'] or 'GENERAL_METROPOLITAN': r['count'] for r in cur.fetchall()}
    
    conn.close()
    return {
        "total_verified": total_verified,
        "total_agrovet": total_agrovet,
        "total_veterinary": total_vet,
        "total_feed_poultry": total_feed,
        "total_needs_review": total_review,
        "by_district": by_district,
        "by_category": by_category,
        "by_cluster": by_cluster
    }

@app.get("/api/clusters")
def get_clusters():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT hotspot_cluster, district, COUNT(*) as count 
        FROM master_businesses 
        WHERE verification_status = 'VERIFIED' 
        GROUP BY hotspot_cluster 
        ORDER BY 
            CASE WHEN hotspot_cluster = 'GENERAL_METROPOLITAN' OR hotspot_cluster IS NULL THEN 1 ELSE 0 END,
            count DESC
    ''')
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@app.get("/api/districts-and-areas")
def get_districts_and_areas():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT DISTINCT district, ward_or_area 
        FROM master_businesses 
        WHERE ward_or_area IS NOT NULL AND ward_or_area != ''
        ORDER BY district, ward_or_area
    ''')
    rows = cur.fetchall()
    districts = {}
    for r in rows:
        d = r['district'] or 'UNKNOWN'
        a = r['ward_or_area']
        if d not in districts:
            districts[d] = []
        if a not in districts[d]:
            districts[d].append(a)
    conn.close()
    return districts

@app.get("/api/businesses")
def get_businesses(
    search: str = None,
    district: str = None,
    area: str = None,
    cluster: str = None,
    category: str = None,
    status: str = "VERIFIED",
    source: str = None
):
    items = query_businesses(search, district, area, category, status, source, cluster)
    return {"total": len(items), "items": items}

@app.get("/api/export/excel")
def download_excel():
    updated_path = os.path.join(os.path.dirname(EXCEL_PATH), "Dar_Es_Salaam_Agrovet_Database_Updated.xlsx")
    target = updated_path if os.path.exists(updated_path) else EXCEL_PATH
    if not os.path.exists(target):
        from backend.exporter.excel_exporter import export_to_excel
        target = export_to_excel(DB_PATH, EXCEL_PATH)
    return FileResponse(
        path=target,
        filename="Dar_Es_Salaam_Agrovet_Database.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.get("/api/export/csv")
def download_csv(
    search: str = None,
    district: str = None,
    area: str = None,
    cluster: str = None,
    category: str = None,
    status: str = "VERIFIED"
):
    items = query_businesses(search, district, area, category, status, cluster=cluster)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "ID", "Business Name", "Category", "Secondary Categories", 
        "District", "Ward / Area", "Hotspot Cluster", "Address", "Phone", "Alternative Phone",
        "Latitude", "Longitude", "Google Maps URL", "Confidence", "Evidence", "Sources"
    ])
    
    for b in items:
        writer.writerow([
            b.get("id"),
            b.get("business_name"),
            b.get("category"),
            ", ".join(b.get("secondary_categories") or []),
            b.get("district"),
            b.get("ward_or_area"),
            b.get("hotspot_cluster"),
            b.get("street_or_address"),
            b.get("phone"),
            b.get("alternative_phone"),
            b.get("latitude"),
            b.get("longitude"),
            b.get("google_maps_url"),
            b.get("confidence"),
            b.get("evidence"),
            ", ".join(b.get("source_types") or [])
        ])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=dar_es_salaam_agrovets_filtered.csv"}
    )

@app.get("/api/health")
def health_check():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE verification_status = 'VERIFIED'")
    cnt = cur.fetchone()[0]
    conn.close()
    return {
        "status": "ok",
        "service": "Dar es Salaam Agrovet Database API",
        "version": "1.0.0",
        "verified_businesses": cnt
    }

# Mount static frontend
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=True)