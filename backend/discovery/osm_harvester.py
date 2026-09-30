import urllib.request
import urllib.parse
import json
import os
import time
from datetime import datetime

OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]

DAR_BBOX = (-7.25, 39.00, -6.55, 39.60)
CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "osm_cache.json")

def build_osm_query(bbox):
    s, w, n, e = bbox
    query = f"""[out:json][timeout:50];
(
  node["shop"="veterinary"]({s},{w},{n},{e});
  node["amenity"="veterinary"]({s},{w},{n},{e});
  node["shop"="agrarian"]({s},{w},{n},{e});
  node["shop"="animal_feed"]({s},{w},{n},{e});
  node["shop"="farm"]({s},{w},{n},{e});
  node["name"~"agrovet|veterinary|vet|mifugo|kuku|chakula cha|chicks|animal health|pembejeo",i]({s},{w},{n},{e});
  
  way["shop"="veterinary"]({s},{w},{n},{e});
  way["amenity"="veterinary"]({s},{w},{n},{e});
  way["shop"="agrarian"]({s},{w},{n},{e});
  way["shop"="animal_feed"]({s},{w},{n},{e});
  way["name"~"agrovet|veterinary|vet|mifugo|kuku|chakula cha|chicks|animal health|pembejeo",i]({s},{w},{n},{e});
);
out center tags qt;
"""
    return query

def fetch_osm_data(bbox=DAR_BBOX, use_cache=True):
    # Check cache first
    if use_cache and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                records = json.load(f)
                if records:
                    print(f"Loaded {len(records)} OSM records from local cache: {CACHE_FILE}", flush=True)
                    return records, None
        except Exception as e:
            print(f"Cache read error: {e}", flush=True)

    query = build_osm_query(bbox)
    data_bytes = query.encode("utf-8")
    headers = {
        "User-Agent": "DarEsSalaamAgrovetResearch/1.0 (contact: info@amsterdamgroup.co.tz)"
    }
    
    last_err = None
    for endpoint in OVERPASS_SERVERS:
        try:
            print(f"Querying Overpass server: {endpoint}...", flush=True)
            req = urllib.request.Request(endpoint, data=data_bytes, headers=headers)
            with urllib.request.urlopen(req, timeout=40) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                elements = result.get("elements", [])
                records = []
                for el in elements:
                    el_type = el.get("type", "node")
                    el_id = el.get("id")
                    tags = el.get("tags", {})
                    lat = el.get("lat") or (el.get("center", {}).get("lat"))
                    lon = el.get("lon") or (el.get("center", {}).get("lon"))
                    
                    records.append({
                        "source_type": "openstreetmap",
                        "source_id": f"osm_{el_type}_{el_id}",
                        "source_url": f"https://www.openstreetmap.org/{el_type}/{el_id}",
                        "raw_payload": json.dumps({
                            "osm_id": el_id,
                            "type": el_type,
                            "lat": lat,
                            "lon": lon,
                            "tags": tags
                        }, ensure_ascii=False),
                        "extracted_at": datetime.utcnow().isoformat()
                    })
                
                # Save to cache
                try:
                    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
                    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                        json.dump(records, f, ensure_ascii=False, indent=2)
                except Exception as e:
                    print(f"Failed to cache OSM data: {e}", flush=True)
                    
                return records, None
        except Exception as e:
            last_err = str(e)
            print(f"Server {endpoint} error: {e}, trying next...", flush=True)
            time.sleep(2)
            continue
            
    return [], last_err

if __name__ == "__main__":
    recs, err = fetch_osm_data()
    print(f"Retrieved {len(recs)} records. Error: {err}")