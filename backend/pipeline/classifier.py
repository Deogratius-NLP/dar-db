import os
import re
import json

CONTROLLED_CATEGORIES = [
    'AGROVET',
    'VETERINARY_SHOP',
    'VETERINARY_PHARMACY',
    'ANIMAL_HEALTH_SUPPLIER',
    'ANIMAL_FEED',
    'POULTRY_FEED',
    'LIVESTOCK_SUPPLIES',
    'POULTRY_SUPPLIES',
    'AGRICULTURAL_INPUTS',
    'VETERINARY_SERVICE',
    'WHOLESALER',
    'DISTRIBUTOR',
    'OTHER_RELEVANT',
    'NOT_RELEVANT',
    'NEEDS_REVIEW'
]

EXCLUSION_RULES = [
    (r'\bveta\b', "Vocational Education and Training Authority (VETA)"),
    (r'\btakukuru\b', "Anti-Corruption Bureau (TAKUKURU)"),
    (r'\bhardware\b', "Hardware and construction materials shop"),
    (r'\belectronics\b|\belectronic\b', "Electronics shop"),
    (r'\bclothes\b|\bclothing\b|\bboutique\b', "Clothing / fashion shop"),
    (r'\bmasjid\b|\bmosque\b|\bchurch\b|\bkanisa\b', "Place of worship"),
    (r'\bhotel\b|\blodge\b|\bguesthouse\b|\bapartment\b', "Hospitality / Accommodation / Housing"),
    (r'\bschool\b|\bcollege\b|\buniversity\b', "Educational institution"),
    (r'\bbar\b|\blounge\b|\bpub\b|\bnight\s*club\b', "Bar or entertainment venue"),
    (r'\bhospitali ya rufaa\b|\bdispensary\b(?!.*mifugo)', "Human health dispensary / hospital"),
    (r'\bbank\b|\bfinancial\b|\batm\b', "Financial institution"),
    (r'\bmotor\b|\bcar\b|\bgarage\b|\bauto\b', "Automotive business"),
    (r'\bkukuruka\b', "Word contains non-poultry slang/name"),
    (r'\bmakukula\b', "Word contains non-poultry proper name"),
    (r'\btop\s*\d+\b|\bfind\s+clinics\b|\bgoogle\s*maps\b', "Directory / Aggregator page")
]

# Non-relevant OSM shop types
EXCLUDED_OSM_SHOPS = {
    'electronics', 'clothes', 'place_of_worship', 'furniture', 
    'car', 'car_repair', 'hairdresser', 'beauty', 'laundry', 'tailor'
}

def classify_business_evidence_based(name, description="", tags=None, snippet=""):
    if tags is None:
        tags = {}
        
    combined = f"{name} {description} {snippet} {' '.join(str(v) for v in tags.values())}".lower()
    clean_name = name.lower().strip()
    
    # 1. Check explicit exclusions
    for pat, reason in EXCLUSION_RULES:
        if re.search(pat, clean_name):
            return "NOT_RELEVANT", [], "HIGH", f"Matched exclusion rule '{pat}' in name", "NOT_RELEVANT", reason
            
    osm_shop = str(tags.get('shop', '')).lower()
    osm_amenity = str(tags.get('amenity', '')).lower()
    
    if osm_shop in EXCLUDED_OSM_SHOPS and not any(k in clean_name for k in ['agrovet', 'vet', 'mifugo', 'kuku', 'feed']):
        return "NOT_RELEVANT", [], "HIGH", f"OSM shop type '{osm_shop}' is non-livestock", "NOT_RELEVANT", f"Non-livestock shop ({osm_shop})"
        
    secondaries = set()
    evidence_points = []
    
    # Feature detection
    has_vet = bool(re.search(r'\b(?:vet|veterinary|daktari wa wanyama|madawa ya mifugo|dawa za mifugo|kliniki ya mifugo|animal health)\b', combined))
    has_agro = bool(re.search(r'\b(?:agro|agrovet|pembejeo|kilimo)\b', combined))
    has_feed = bool(re.search(r'\b(?:feed|feeds|chakula cha|vyakula vya|mashudu|pumba|bran|concentrate)\b', combined))
    has_poultry = bool(re.search(r'\b(?:poultry|kuku|chick|chicks|vifaranga|broiler|layer)\b', combined))
    has_pharm = bool(re.search(r'\b(?:pharmacy|chemist|dawa|madawa|vaccine|chanjo)\b', combined))
    has_service = bool(re.search(r'\b(?:clinic|kliniki|consult|hospital|service|treatment|ambulatory)\b', combined))
    has_distributor = bool(re.search(r'\b(?:distributor|supplier|wholesale|jumla|wakala|agent)\b', combined))

    if has_vet:
        evidence_points.append("veterinary keywords/services")
    if has_agro:
        evidence_points.append("agricultural inputs / agrovet")
    if has_feed:
        evidence_points.append("animal feed products")
    if has_poultry:
        evidence_points.append("poultry / chicks / feeds")
    if has_pharm:
        evidence_points.append("pharmaceuticals / vaccines")
    if has_service:
        evidence_points.append("clinical / veterinary services")
    if has_distributor:
        evidence_points.append("wholesale / distribution / agent")

    # OSM tags
    if osm_shop == 'veterinary' or osm_amenity == 'veterinary':
        has_vet = True
        evidence_points.append(f"OSM tag shop/amenity=veterinary")
    if osm_shop == 'animal_feed':
        has_feed = True
        evidence_points.append("OSM tag shop=animal_feed")
    if osm_shop == 'agrarian':
        has_agro = True
        evidence_points.append("OSM tag shop=agrarian")

    primary = "NEEDS_REVIEW"
    confidence = "MEDIUM"
    status = "VERIFIED"
    exclusion = None

    if "agrovet" in clean_name or (has_agro and (has_vet or has_feed or has_poultry)):
        primary = "AGROVET"
        confidence = "HIGH"
        if has_feed:
            secondaries.add("ANIMAL_FEED")
        if has_poultry:
            secondaries.add("POULTRY_SUPPLIES")
        if has_pharm:
            secondaries.add("VETERINARY_PHARMACY")
    elif has_poultry and has_feed:
        primary = "POULTRY_FEED"
        confidence = "HIGH"
        secondaries.add("ANIMAL_FEED")
        secondaries.add("POULTRY_SUPPLIES")
    elif has_feed:
        primary = "ANIMAL_FEED"
        confidence = "HIGH"
        if has_poultry:
            secondaries.add("POULTRY_FEED")
    elif has_poultry and (has_distributor or "chick" in clean_name or "vifaranga" in clean_name):
        primary = "POULTRY_SUPPLIES"
        confidence = "HIGH"
        if has_feed:
            secondaries.add("POULTRY_FEED")
    elif has_service and has_vet:
        primary = "VETERINARY_SERVICE"
        confidence = "HIGH"
        if has_pharm:
            secondaries.add("VETERINARY_PHARMACY")
    elif has_pharm and has_vet:
        primary = "VETERINARY_PHARMACY"
        confidence = "HIGH"
        secondaries.add("ANIMAL_HEALTH_SUPPLIER")
    elif has_vet:
        primary = "VETERINARY_SHOP"
        confidence = "HIGH"
        secondaries.add("ANIMAL_HEALTH_SUPPLIER")
    elif has_distributor and (has_agro or has_feed or has_vet):
        primary = "DISTRIBUTOR"
        confidence = "HIGH"
        if has_feed:
            secondaries.add("ANIMAL_FEED")
    elif has_poultry:
        primary = "POULTRY_SUPPLIES"
        confidence = "MEDIUM"
    elif has_agro:
        primary = "AGRICULTURAL_INPUTS"
        confidence = "MEDIUM"
    elif len(evidence_points) == 0:
        primary = "NEEDS_REVIEW"
        status = "NEEDS_REVIEW"
        confidence = "LOW"
        evidence_points.append("insufficient livestock or veterinary evidence in snippet")
    else:
        primary = "OTHER_RELEVANT"
        confidence = "MEDIUM"

    evidence_str = "; ".join(evidence_points) if evidence_points else "No definitive evidence"
    return primary, list(secondaries), confidence, evidence_str, status, exclusion

def classify_with_gemini_if_available(name, description, snippet, tags=None):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return classify_business_evidence_based(name, description, tags, snippet)

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = f"""
You are an expert Tanzanian business classifier for an animal health and veterinary database.
Business Name: {name}
Description: {description}
Snippet: {snippet}
Tags: {json.dumps(tags or {})}

Classify this business into exactly one Primary Category from:
AGROVET, VETERINARY_SHOP, VETERINARY_PHARMACY, ANIMAL_HEALTH_SUPPLIER, ANIMAL_FEED, POULTRY_FEED, LIVESTOCK_SUPPLIES, POULTRY_SUPPLIES, AGRICULTURAL_INPUTS, VETERINARY_SERVICE, WHOLESALER, DISTRIBUTOR, OTHER_RELEVANT, NOT_RELEVANT, NEEDS_REVIEW.

Provide secondary categories, confidence (HIGH, MEDIUM, LOW), and concise evidence. Do NOT invent facts.

Return JSON only:
{{
  "primary_category": "...",
  "secondary_categories": ["..."],
  "confidence": "HIGH|MEDIUM|LOW",
  "evidence": "...",
  "verification_status": "VERIFIED|NEEDS_REVIEW|NOT_RELEVANT",
  "exclusion_reason": null
}}
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        txt = response.text.strip()
        m = re.search(r'\{.*\}', txt, re.DOTALL)
        if m:
            data = json.loads(m.group(0))
            return (
                data.get("primary_category", "NEEDS_REVIEW"),
                data.get("secondary_categories", []),
                data.get("confidence", "MEDIUM"),
                data.get("evidence", "Gemini AI classification"),
                data.get("verification_status", "VERIFIED"),
                data.get("exclusion_reason")
            )
    except Exception as e:
        pass
        
    return classify_business_evidence_based(name, description, tags, snippet)