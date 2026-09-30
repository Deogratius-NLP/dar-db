import urllib.request
import json

overpass_url = "https://overpass-api.de/api/interpreter"
# Deep Overpass query: Dar es Salaam administrative area
# Query ALL nodes, ways, and relations in Dar es Salaam with any animal, vet, feed, agrovet, poultry, livestock, or agricultural inputs tags or names
query = """[out:json][timeout:120];
area["name"="Dar es Salaam"]->.searchArea;
(
  // 1. Direct veterinary & agrarian tags
  nwr["shop"~"veterinary|agrarian|animal_feed|farm"](area.searchArea);
  nwr["amenity"="veterinary"](area.searchArea);
  
  // 2. All shops and amenities with livestock/veterinary/poultry/feed names or tags
  nwr["shop"](area.searchArea)["name"~"vet|mifugo|kuku|chakula|feed|agro|pembejeo|chick|vifaranga|chanjo|dawa|kilimo|ufugaji|livestock|poultry",i];
  nwr["amenity"](area.searchArea)["name"~"vet|mifugo|kuku|chakula|feed|agro|pembejeo|chick|vifaranga|chanjo|dawa|kilimo|ufugaji|livestock|poultry",i];
  nwr["craft"](area.searchArea)["name"~"vet|mifugo|kuku|chakula|feed|agro|pembejeo|chick|vifaranga|chanjo|dawa|kilimo|ufugaji|livestock|poultry",i];
  nwr["office"](area.searchArea)["name"~"vet|mifugo|kuku|chakula|feed|agro|pembejeo|chick|vifaranga|chanjo|dawa|kilimo|ufugaji|livestock|poultry",i];
  
  // 3. Fallback coordinates bbox for Dar es Salaam
  nwr["shop"~"veterinary|agrarian|animal_feed|farm"](-7.25,39.00,-6.55,39.60);
  nwr["amenity"="veterinary"](-7.25,39.00,-6.55,39.60);
  nwr["name"~"agrovet|veterinary|madawa ya mifugo|chakula cha mifugo|vyakula vya kuku|chakula cha kuku|vifaranga vya kuku|dawa za mifugo|animal feed|poultry feed|livestock",i](-7.25,39.00,-6.55,39.60);
);
out center tags qt;
"""

req = urllib.request.Request(overpass_url, data=query.encode('utf-8'), headers={'User-Agent': 'DarAgrovetDeepSearch/1.0'})
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        elements = data.get('elements', [])
        print(f"Deep OSM returned {len(elements)} elements!")
except Exception as e:
    print("Error:", e)