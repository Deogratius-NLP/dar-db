import urllib.request
import json
import time

mirrors = [
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter"
]

remaining_bboxes = {
    "Ilala": (-7.05, 39.05, -6.78, 39.32),
    "Temeke": (-7.15, 39.15, -6.82, 39.35),
    "Kigamboni": (-7.25, 39.28, -6.80, 39.60)
}

for d_name, (s, w, n, e) in remaining_bboxes.items():
    query = f"""[out:json][timeout:35];
(
  node["shop"~"veterinary|pet|agrarian|animal_feed|farm"]({s},{w},{n},{e});
  node["amenity"="veterinary"]({s},{w},{n},{e});
  node["shop"]({s},{w},{n},{e})["name"~"agro|vet|mifugo|kuku|chakula|feed|pembejeo|chick|vifaranga|dawa za mifugo",i];
  way["shop"~"veterinary|pet|agrarian|animal_feed|farm"]({s},{w},{n},{e});
  way["amenity"="veterinary"]({s},{w},{n},{e});
  way["shop"]({s},{w},{n},{e})["name"~"agro|vet|mifugo|kuku|chakula|feed|pembejeo|chick|vifaranga|dawa za mifugo",i];
);
out center tags qt;
"""
    success = False
    for m in mirrors:
        try:
            req = urllib.request.Request(m, data=query.encode('utf-8'), headers={'User-Agent': 'DarDeepAgro/1.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                elems = data.get('elements', [])
                print(f"District {d_name} ({m}): {len(elems)} elements!")
                success = True
                break
        except Exception as e:
            print(f"Error {m}: {e}")
            time.sleep(2)
    time.sleep(3)