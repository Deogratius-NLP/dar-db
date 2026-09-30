import difflib
import json
import math
from backend.pipeline.geo_resolver import haversine_distance_km
from backend.pipeline.normalizer import normalize_business_name_for_dedup, extract_primary_brand_token

def calculate_name_similarity(name1, name2):
    if not name1 or not name2:
        return 0.0
    k1 = normalize_business_name_for_dedup(name1)
    k2 = normalize_business_name_for_dedup(name2)
    if k1 == k2 and len(k1) > 0:
        return 1.0
    return difflib.SequenceMatcher(None, k1, k2).ratio()

def find_duplicate_candidate(new_biz, existing_businesses):
    """
    Compares new_biz against list of existing businesses.
    Returns: (matched_biz, confidence_type)
    """
    new_phone = new_biz.get('phone')
    new_name = new_biz.get('business_name', '')
    new_dedup_key = normalize_business_name_for_dedup(new_name)
    new_brand = extract_primary_brand_token(new_name)
    new_area = (new_biz.get('ward_or_area') or 'UNKNOWN').lower()
    new_lat = new_biz.get('latitude')
    new_lon = new_biz.get('longitude')
    
    for ex in existing_businesses:
        ex_phone = ex.get('phone')
        ex_alt_phone = ex.get('alternative_phone')
        ex_name = ex.get('business_name', '')
        ex_dedup_key = normalize_business_name_for_dedup(ex_name)
        ex_brand = extract_primary_brand_token(ex_name)
        ex_area = (ex.get('ward_or_area') or 'UNKNOWN').lower()
        ex_lat = ex.get('latitude')
        ex_lon = ex.get('longitude')
        
        # 1. Phone number match
        if new_phone and (new_phone == ex_phone or new_phone == ex_alt_phone):
            return ex, 'EXACT_PHONE'
            
        # 2. Exact normalized name + same area (not unknown)
        if new_dedup_key == ex_dedup_key and len(new_dedup_key) > 3:
            if new_area != 'unknown' and new_area == ex_area:
                return ex, 'EXACT_NAME_AREA'
                
        # 3. Same distinct brand token + same area (e.g. "JOACK Agrovet" & "JOACK Company Limited" in Tegeta)
        if new_brand and ex_brand and new_brand == ex_brand and len(new_brand) >= 4:
            if new_area != 'unknown' and new_area == ex_area:
                return ex, 'BRAND_AREA_MATCH'

        # 4. Coordinate proximity (< 150 meters) + fuzzy name similarity > 0.55
        if new_lat and new_lon and ex_lat and ex_lon:
            try:
                dist_km = haversine_distance_km(float(new_lat), float(new_lon), float(ex_lat), float(ex_lon))
                sim = calculate_name_similarity(new_name, ex_name)
                if dist_km < 0.15 and sim >= 0.55:
                    return ex, 'FUZZY_NAME_PROXIMITY'
            except (ValueError, TypeError):
                pass
                
        # 5. High fuzzy name similarity (> 0.85) in same area
        sim = calculate_name_similarity(new_name, ex_name)
        if sim >= 0.85:
            if new_area == ex_area or new_area == 'unknown' or ex_area == 'unknown':
                return ex, 'POSSIBLE_DUPLICATE'

    return None, None

def merge_business_records(target_record, incoming_record):
    merged = dict(target_record)
    
    # 1. Source URLs & Types
    try:
        t_urls = json.loads(merged.get('source_urls') or '[]')
    except Exception:
        t_urls = []
    try:
        t_types = json.loads(merged.get('source_types') or '[]')
    except Exception:
        t_types = []
        
    try:
        in_urls = json.loads(incoming_record.get('source_urls') or '[]')
    except Exception:
        in_urls = []
    try:
        in_types = json.loads(incoming_record.get('source_types') or '[]')
    except Exception:
        in_types = []
        
    merged_urls = list(dict.fromkeys(t_urls + in_urls))
    merged_types = list(dict.fromkeys(t_types + in_types))
    
    merged['source_urls'] = json.dumps(merged_urls, ensure_ascii=False)
    merged['source_types'] = json.dumps(merged_types, ensure_ascii=False)
    
    # 2. Coordinates
    if not merged.get('latitude') and incoming_record.get('latitude'):
        merged['latitude'] = incoming_record['latitude']
        merged['longitude'] = incoming_record['longitude']
        
    # 3. Location
    if merged.get('district') in (None, '', 'UNKNOWN') and incoming_record.get('district') not in (None, '', 'UNKNOWN'):
        merged['district'] = incoming_record['district']
    if merged.get('ward_or_area') in (None, '', 'UNKNOWN') and incoming_record.get('ward_or_area') not in (None, '', 'UNKNOWN'):
        merged['ward_or_area'] = incoming_record['ward_or_area']
        
    # 4. Street / address
    if not merged.get('street_or_address') and incoming_record.get('street_or_address'):
        merged['street_or_address'] = incoming_record['street_or_address']
        
    # 5. Phone numbers
    if not merged.get('phone') and incoming_record.get('phone'):
        merged['phone'] = incoming_record['phone']
    elif merged.get('phone') and incoming_record.get('phone') and merged.get('phone') != incoming_record.get('phone'):
        if not merged.get('alternative_phone'):
            merged['alternative_phone'] = incoming_record['phone']
            
    # 6. Online links
    for field in ['website', 'facebook', 'instagram', 'whatsapp', 'email']:
        if not merged.get(field) and incoming_record.get(field):
            merged[field] = incoming_record[field]
            
    # 7. Merge secondary categories
    try:
        t_sec = json.loads(merged.get('secondary_categories') or '[]')
    except Exception:
        t_sec = []
    try:
        in_sec = json.loads(incoming_record.get('secondary_categories') or '[]')
    except Exception:
        in_sec = []
        
    # Add incoming primary category as secondary if different
    if incoming_record.get('category') and incoming_record.get('category') != merged.get('category'):
        in_sec.append(incoming_record.get('category'))
        
    combined_sec = list(dict.fromkeys(t_sec + in_sec))
    merged['secondary_categories'] = json.dumps(combined_sec)
    
    # 8. Notes
    notes_list = [n for n in [merged.get('notes'), incoming_record.get('notes')] if n]
    merged['notes'] = " | ".join(dict.fromkeys(notes_list))
    merged['duplicate_status'] = 'MERGED'
    
    return merged