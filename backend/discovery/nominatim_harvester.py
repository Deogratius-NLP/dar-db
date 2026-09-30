import urllib.request
import urllib.parse
import json
import time
from datetime import datetime

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {
    "User-Agent": "DarEsSalaamAgrovetResearch/1.0 (contact: info@amsterdamgroup.co.tz)"
}

NOMINATIM_QUERIES = [
    # General terms in Dar es Salaam
    "agrovet Dar es Salaam",
    "veterinary Dar es Salaam",
    "animal feed Dar es Salaam",
    "chakula cha kuku Dar es Salaam",
    "vifaranga vya kuku Dar es Salaam",
    "madawa ya mifugo Dar es Salaam",
    "dawa za mifugo Dar es Salaam",
    "pembejeo Dar es Salaam",
    "poultry Dar es Salaam",
    # District specific
    "agrovet Kinondoni",
    "veterinary Kinondoni",
    "animal feed Kinondoni",
    "agrovet Ubungo",
    "veterinary Ubungo",
    "animal feed Ubungo",
    "agrovet Ilala",
    "veterinary Ilala",
    "animal feed Ilala",
    "agrovet Temeke",
    "veterinary Temeke",
    "animal feed Temeke",
    "agrovet Kigamboni",
    "veterinary Kigamboni",
    # Ward / Area specific
    "agrovet Tegeta",
    "agrovet Bunju",
    "agrovet Sinza",
    "agrovet Mwenge",
    "agrovet Kariakoo",
    "agrovet Tabata",
    "agrovet Mbagala",
    "animal feed Kariakoo",
    "animal feed Mbagala",
    "animal feed Tabata"
]

def search_nominatim(query):
    params = {
        "format": "json",
        "q": query,
        "addressdetails": "1",
        "limit": "15"
    }
    url = f"{NOMINATIM_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    records = []
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data:
                lat = item.get('lat')
                lon = item.get('lon')
                display_name = item.get('display_name', '')
                addr = item.get('address', {})
                name = item.get('name') or display_name.split(',')[0].strip()
                osm_id = item.get('osm_id')
                osm_type = item.get('osm_type', 'node')
                
                records.append({
                    "source_type": "nominatim_osm",
                    "source_id": f"nom_{osm_type}_{osm_id}",
                    "source_url": f"https://www.openstreetmap.org/{osm_type}/{osm_id}",
                    "query_used": query,
                    "raw_payload": json.dumps({
                        "name": name,
                        "display_name": display_name,
                        "lat": lat,
                        "lon": lon,
                        "osm_id": osm_id,
                        "osm_type": osm_type,
                        "address": addr,
                        "type": item.get('type')
                    }, ensure_ascii=False),
                    "extracted_at": datetime.utcnow().isoformat()
                })
    except Exception as e:
        print(f"Error querying Nominatim for '{query}': {e}", flush=True)
        
    return records

def harvest_all_nominatim():
    print(f"Executing Nominatim search across {len(NOMINATIM_QUERIES)} targeted queries...", flush=True)
    all_records = []
    for idx, q in enumerate(NOMINATIM_QUERIES, 1):
        print(f"  [{idx}/{len(NOMINATIM_QUERIES)}] Nominatim: '{q}'...", flush=True)
        recs = search_nominatim(q)
        print(f"    -> Found {len(recs)} results.", flush=True)
        all_records.extend(recs)
        time.sleep(1.0) # Respect Nominatim rate limit (max 1 req/sec)
    print(f"Nominatim harvesting completed. Total records gathered: {len(all_records)}", flush=True)
    return all_records

if __name__ == "__main__":
    recs = harvest_all_nominatim()
    print("Sample 5 records:")
    for r in recs[:5]:
        p = json.loads(r['raw_payload'])
        print("-", p['name'], f"({p['lat']}, {p['lon']})", "|", p['display_name'][:80])