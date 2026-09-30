import argparse
import json
import os
import sys
import time
from datetime import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)

from backend.database import get_connection, init_db
from backend.discovery.search_matrix import generate_search_tasks, DISTRICTS_AND_AREAS
from backend.discovery.osm_harvester import fetch_osm_data, DAR_BBOX
from backend.discovery.nominatim_harvester import harvest_all_nominatim
from backend.discovery.web_harvester import search_duckduckgo_html
from backend.discovery.deep_directory_harvester import harvest_deep_directory_records
from backend.discovery.cluster_harvester import harvest_cluster_deep_records, resolve_hotspot_cluster
from backend.pipeline.normalizer import (
    clean_business_name,
    normalize_business_name_for_dedup,
    extract_phone_numbers,
    extract_email,
    extract_social_links,
    is_directory_or_aggregator
)
from backend.pipeline.geo_resolver import resolve_geographic_location
from backend.pipeline.classifier import classify_with_gemini_if_available, CONTROLLED_CATEGORIES
from backend.pipeline.deduplicator import find_duplicate_candidate, merge_business_records

def process_and_save_record(conn, item, search_task_id=None):
    cur = conn.cursor()
    
    # 1. Save Raw Record
    cur.execute('''
        INSERT INTO raw_records (source_type, source_id, source_url, query_used, search_task_id, raw_payload, extracted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        item.get('source_type'),
        item.get('source_id'),
        item.get('source_url'),
        item.get('query_used'),
        search_task_id,
        item.get('raw_payload'),
        item.get('extracted_at', datetime.utcnow().isoformat())
    ))
    
    # 2. Extract fields
    raw_p = json.loads(item.get('raw_payload') or '{}')
    source_type = item.get('source_type')
    
    name = ""
    description = ""
    snippet = ""
    tags = {}
    lat = None
    lon = None
    street_or_address = ""
    phones = []
    website = ""
    fb = ""
    insta = ""
    email = ""
    
    if source_type == 'openstreetmap':
        tags = raw_p.get('tags', {})
        name = tags.get('name') or tags.get('operator') or tags.get('description') or tags.get('shop') or ''
        description = tags.get('description') or ''
        lat = raw_p.get('lat')
        lon = raw_p.get('lon')
        street = tags.get('addr:street', '')
        suburb = tags.get('addr:suburb') or tags.get('addr:ward') or tags.get('addr:district', '')
        street_or_address = f"{street} {suburb}".strip()
        p = tags.get('phone') or tags.get('contact:phone') or tags.get('contact:mobile')
        if p:
            phones = extract_phone_numbers(p)
        website = tags.get('website') or tags.get('contact:website') or ''
        fb = tags.get('contact:facebook') or ''
        email = tags.get('email') or tags.get('contact:email') or ''
        
    elif source_type == 'nominatim_osm':
        name = raw_p.get('name', '')
        display_name = raw_p.get('display_name', '')
        lat = raw_p.get('lat')
        lon = raw_p.get('lon')
        addr = raw_p.get('address', {})
        road = addr.get('road', '')
        suburb = addr.get('suburb') or addr.get('neighbourhood') or addr.get('city_district', '')
        street_or_address = f"{road} {suburb}".strip() or display_name[:150]
        snippet = display_name
        
    elif source_type == 'web_directory':
        title = raw_p.get('title', '')
        snippet = raw_p.get('snippet', '')
        
        if is_directory_or_aggregator(title):
            return None, "SKIPPED_AGGREGATOR"
            
        title_phones = extract_phone_numbers(title)
        phones.extend(title_phones)
        
        name = clean_business_name(title)
        combined_text = f"{title} {snippet}"
        phones.extend(extract_phone_numbers(combined_text))
        email = extract_email(combined_text)
        website, fb, insta = extract_social_links(combined_text, item.get('source_url', ''))
        street_or_address = snippet[:150]
        
    elif source_type in ('deep_directory', 'verified_directory', 'hotspot_cluster_harvest', 'value_chain_brand'):
        name = raw_p.get('business_name', '')
        description = raw_p.get('description', '')
        snippet = description
        lat = raw_p.get('latitude')
        lon = raw_p.get('longitude')
        street_or_address = raw_p.get('street_or_address', '')
        p1 = raw_p.get('phone')
        p2 = raw_p.get('alternative_phone')
        if p1:
            phones.extend(extract_phone_numbers(p1))
        if p2:
            phones.extend(extract_phone_numbers(p2))
        email = raw_p.get('email', '')
        website = raw_p.get('website', '')
        fb = raw_p.get('facebook', '')
        insta = raw_p.get('instagram', '')
        
    if not name or len(name.strip()) < 2:
        return None, "SKIPPED_EMPTY_NAME"
        
    clean_name = clean_business_name(name)
    if is_directory_or_aggregator(clean_name):
        return None, "SKIPPED_AGGREGATOR"
        
    normalized_name = normalize_business_name_for_dedup(clean_name)
    
    unique_phones = []
    for ph in phones:
        if ph not in unique_phones:
            unique_phones.append(ph)
            
    primary_phone = unique_phones[0] if len(unique_phones) > 0 else None
    alt_phone = unique_phones[1] if len(unique_phones) > 1 else None
    
    # 3. Geographic resolution
    default_dist = item.get('default_district') or raw_p.get('district')
    default_area = item.get('default_area') or raw_p.get('ward_or_area')
    district, ward_or_area = resolve_geographic_location(
        text=f"{clean_name} {street_or_address} {snippet}",
        lat=lat,
        lon=lon,
        default_district=default_dist,
        default_area=default_area
    )
    
    # 4. Classification
    if source_type in ('deep_directory', 'verified_directory', 'hotspot_cluster_harvest', 'value_chain_brand') and raw_p.get('category'):
        primary_cat = raw_p.get('category')
        sec_cats = raw_p.get('secondary_categories', [])
        conf = 0.98
        evidence = f"Verified commercial directory/hotspot listing ({item.get('source_url', 'direct_verified')})"
        ver_status = 'VERIFIED'
        excl_reason = None
    else:
        primary_cat, sec_cats, conf, evidence, ver_status, excl_reason = classify_with_gemini_if_available(
            name=clean_name,
            description=description,
            snippet=snippet,
            tags=tags
        )
        
    hotspot_cluster = item.get('hotspot_cluster') or raw_p.get('hotspot_cluster')
    if not hotspot_cluster or hotspot_cluster == 'GENERAL_METROPOLITAN':
        hotspot_cluster = resolve_hotspot_cluster(district, ward_or_area, street_or_address, lat, lon)
    
    new_record = {
        'business_name': clean_name,
        'normalized_business_name': normalized_name,
        'category': primary_cat,
        'secondary_categories': json.dumps(sec_cats),
        'confidence': conf,
        'evidence': evidence,
        'verification_status': ver_status,
        'exclusion_reason': excl_reason,
        'district': district,
        'ward_or_area': ward_or_area,
        'street_or_address': street_or_address,
        'latitude': lat,
        'longitude': lon,
        'phone': primary_phone,
        'alternative_phone': alt_phone,
        'whatsapp': primary_phone if primary_phone else None,
        'email': email or None,
        'website': website or None,
        'facebook': fb or None,
        'instagram': insta or None,
        'description': description or snippet[:250],
        'notes': f"Discovered via {source_type}",
        'hotspot_cluster': hotspot_cluster,
        'source_urls': json.dumps([item.get('source_url')] if item.get('source_url') else []),
        'source_types': json.dumps([source_type]),
        'duplicate_status': 'UNIQUE',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    # 5. Deduplication against master_businesses
    cur.execute('''
        SELECT id, business_name, normalized_business_name, ward_or_area, district, 
               latitude, longitude, phone, alternative_phone, hotspot_cluster, source_urls, source_types, notes
        FROM master_businesses
    ''')
    existing_rows = [dict(r) for r in cur.fetchall()]
    
    match, match_type = find_duplicate_candidate(new_record, existing_rows)
    
    if match:
        merged = merge_business_records(match, new_record)
        cur.execute('''
            UPDATE master_businesses
            SET latitude = COALESCE(latitude, ?),
                longitude = COALESCE(longitude, ?),
                district = CASE WHEN district = 'UNKNOWN' THEN ? ELSE district END,
                ward_or_area = CASE WHEN ward_or_area = 'UNKNOWN' THEN ? ELSE ward_or_area END,
                street_or_address = CASE WHEN street_or_address IS NULL OR street_or_address = '' THEN ? ELSE street_or_address END,
                phone = COALESCE(phone, ?),
                alternative_phone = COALESCE(alternative_phone, ?),
                website = COALESCE(website, ?),
                facebook = COALESCE(facebook, ?),
                instagram = COALESCE(instagram, ?),
                secondary_categories = ?,
                notes = ?,
                hotspot_cluster = CASE WHEN hotspot_cluster = 'GENERAL_METROPOLITAN' OR hotspot_cluster IS NULL THEN ? ELSE hotspot_cluster END,
                source_urls = ?,
                source_types = ?,
                duplicate_status = 'MERGED',
                updated_at = ?
            WHERE id = ?
        ''', (
            merged.get('latitude'),
            merged.get('longitude'),
            merged.get('district'),
            merged.get('ward_or_area'),
            merged.get('street_or_address'),
            merged.get('phone'),
            merged.get('alternative_phone'),
            merged.get('website'),
            merged.get('facebook'),
            merged.get('instagram'),
            merged.get('secondary_categories'),
            merged.get('notes'),
            new_record.get('hotspot_cluster'),
            merged.get('source_urls'),
            merged.get('source_types'),
            datetime.utcnow().isoformat(),
            match['id']
        ))
        conn.commit()
        return match['id'], 'MERGED'
    else:
        cur.execute('''
            INSERT INTO master_businesses (
                business_name, normalized_business_name, category, secondary_categories,
                confidence, evidence, verification_status, exclusion_reason,
                district, ward_or_area, street_or_address, latitude, longitude,
                phone, alternative_phone, whatsapp, email, website, facebook, instagram,
                description, notes, hotspot_cluster, source_urls, source_types, duplicate_status,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            new_record['business_name'],
            new_record['normalized_business_name'],
            new_record['category'],
            new_record['secondary_categories'],
            new_record['confidence'],
            new_record['evidence'],
            new_record['verification_status'],
            new_record['exclusion_reason'],
            new_record['district'],
            new_record['ward_or_area'],
            new_record['street_or_address'],
            new_record['latitude'],
            new_record['longitude'],
            new_record['phone'],
            new_record['alternative_phone'],
            new_record['whatsapp'],
            new_record['email'],
            new_record['website'],
            new_record['facebook'],
            new_record['instagram'],
            new_record['description'],
            new_record['notes'],
            new_record['hotspot_cluster'],
            new_record['source_urls'],
            new_record['source_types'],
            new_record['duplicate_status'],
            new_record['created_at'],
            new_record['updated_at']
        ))
        conn.commit()
        return cur.lastrowid, 'INSERTED'

def run_full_pipeline():
    """
    STAGE 4: Full Metropolitan Dar es Salaam Collection.
    Integrates OpenStreetMap Overpass + Nominatim Geocoding + Targeted Web Directories.
    """
    print("=" * 60, flush=True)
    print("STARTING STAGE 4: FULL METROPOLITAN DAR ES SALAAM COLLECTION", flush=True)
    print("=" * 60, flush=True)
    
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM master_businesses")
    cur.execute("DELETE FROM raw_records")
    conn.commit()
    
    # 1. OpenStreetMap Overpass
    print("\n--- 1. INGESTING OPENSTREETMAP OVERPASS DATASET ---", flush=True)
    recs, err = fetch_osm_data(DAR_BBOX, use_cache=True)
    print(f"Ingesting {len(recs)} total OSM elements from cache...", flush=True)
    for r in recs:
        process_and_save_record(conn, r, search_task_id="osm_dar_full")
    cur.execute('''
        INSERT INTO usage_log (source, actor_or_api, query, records_returned, estimated_cost, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('OpenStreetMap', 'Overpass API', 'DAR_METROPOLITAN_BBOX', len(recs), 0.0, datetime.utcnow().isoformat()))
    conn.commit()
    
    # 2. Nominatim Systematic Search
    print("\n--- 2. INGESTING NOMINATIM GEOGRAPHIC POIs ---", flush=True)
    nom_recs = harvest_all_nominatim()
    for nr in nom_recs:
        process_and_save_record(conn, nr, search_task_id="nominatim_search")
    cur.execute('''
        INSERT INTO usage_log (source, actor_or_api, query, records_returned, estimated_cost, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Nominatim/OSM', 'Nominatim Search API', 'DAR_NOMINATIM_MATRIX', len(nom_recs), 0.0, datetime.utcnow().isoformat()))
    conn.commit()
    
    # 3. Deep Verified Directory Harvest (99+ Businesses across all 5 Districts)
    print("\n--- 3. INGESTING DEEP VERIFIED DIRECTORY DATASET ---", flush=True)
    deep_recs = harvest_deep_directory_records()
    print(f"Ingesting {len(deep_recs)} verified agrovet & veterinary directory listings...", flush=True)
    for dr in deep_recs:
        process_and_save_record(conn, dr, search_task_id="deep_directory_expansion")
    cur.execute('''
        INSERT INTO usage_log (source, actor_or_api, query, records_returned, estimated_cost, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Commercial Directories & Registries', 'Deep Directory Harvester', 'DAR_ALL_DISTRICTS_DEEP', len(deep_recs), 0.0, datetime.utcnow().isoformat()))
    conn.commit()

    # 4. Targeted High-Density Cluster Discovery (48+ businesses across 8 hotspots)
    print("\n--- 4. INGESTING TARGETED HIGH-DENSITY CLUSTER DISCOVERY ---", flush=True)
    cluster_recs = harvest_cluster_deep_records()
    print(f"Ingesting {len(cluster_recs)} verified businesses across top 8 high-density clusters...", flush=True)
    for cr in cluster_recs:
        process_and_save_record(conn, cr, search_task_id="hotspot_cluster_expansion")
    cur.execute('''
        INSERT INTO usage_log (source, actor_or_api, query, records_returned, estimated_cost, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Hotspot Cluster Discovery', 'Cluster Harvester', 'DAR_TOP_8_HOTSPOTS_DEEP', len(cluster_recs), 0.0, datetime.utcnow().isoformat()))
    conn.commit()

    # Backfill & resolve hotspot clusters across all master businesses
    print("\nResolving hotspot clusters across all master businesses...", flush=True)
    cur.execute("SELECT id, district, ward_or_area, street_or_address, latitude, longitude, hotspot_cluster FROM master_businesses")
    all_mb = cur.fetchall()
    for row in all_mb:
        resolved_c = resolve_hotspot_cluster(row['district'], row['ward_or_area'], row['street_or_address'], row['latitude'], row['longitude'])
        if resolved_c != row['hotspot_cluster']:
            cur.execute("UPDATE master_businesses SET hotspot_cluster = ? WHERE id = ?", (resolved_c, row['id']))
    conn.commit()

    print("\n============================================================", flush=True)
    print("FULL METROPOLITAN RESEARCH PIPELINE COMPLETED SUCCESSFULLY!", flush=True)
    print("============================================================", flush=True)
    print_database_stats(conn)
    conn.close()

def run_cluster_pipeline_only():
    """Ingests only the targeted high-density cluster harvest into current database."""
    print("=" * 60, flush=True)
    print("STARTING TARGETED HIGH-DENSITY CLUSTER HARVEST", flush=True)
    print("=" * 60, flush=True)
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    
    cluster_recs = harvest_cluster_deep_records()
    print(f"Ingesting {len(cluster_recs)} verified businesses across top 8 high-density clusters...", flush=True)
    for cr in cluster_recs:
        process_and_save_record(conn, cr, search_task_id="hotspot_cluster_expansion")
    cur.execute('''
        INSERT INTO usage_log (source, actor_or_api, query, records_returned, estimated_cost, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ('Hotspot Cluster Discovery', 'Cluster Harvester', 'DAR_TOP_8_HOTSPOTS_DEEP', len(cluster_recs), 0.0, datetime.utcnow().isoformat()))
    conn.commit()

    # Backfill
    print("Resolving hotspot clusters across all master businesses...", flush=True)
    cur.execute("SELECT id, district, ward_or_area, street_or_address, latitude, longitude, hotspot_cluster FROM master_businesses")
    for row in cur.fetchall():
        resolved_c = resolve_hotspot_cluster(row['district'], row['ward_or_area'], row['street_or_address'], row['latitude'], row['longitude'])
        if resolved_c != row['hotspot_cluster']:
            cur.execute("UPDATE master_businesses SET hotspot_cluster = ? WHERE id = ?", (resolved_c, row['id']))
    conn.commit()
    print_database_stats(conn)
    conn.close()

def print_database_stats(conn=None):
    close_at_end = False
    if conn is None:
        conn = get_connection()
        close_at_end = True
        
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM master_businesses")
    total = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE verification_status = 'VERIFIED'")
    verified = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE verification_status = 'NEEDS_REVIEW'")
    needs_review = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE verification_status = 'NOT_RELEVANT'")
    not_relevant = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE duplicate_status = 'MERGED'")
    merged = cur.fetchone()[0]

    print("\nDATABASE SUMMARY METRICS:", flush=True)
    print(f"  Total Records:          {total}", flush=True)
    print(f"  Verified / Relevant:    {verified}", flush=True)
    print(f"  Needs Review:           {needs_review}", flush=True)
    print(f"  Not Relevant (Excluded):{not_relevant}", flush=True)
    print(f"  Merged Duplicates:      {merged}", flush=True)
    
    print("\nBREAKDOWN BY DISTRICT (Verified):", flush=True)
    cur.execute("SELECT district, COUNT(*) FROM master_businesses WHERE verification_status = 'VERIFIED' GROUP BY district ORDER BY COUNT(*) DESC")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}", flush=True)
        
    print("\nBREAKDOWN BY HOTSPOT CLUSTER (Verified):", flush=True)
    cur.execute("SELECT hotspot_cluster, COUNT(*) FROM master_businesses WHERE verification_status = 'VERIFIED' GROUP BY hotspot_cluster ORDER BY COUNT(*) DESC")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}", flush=True)

    print("\nBREAKDOWN BY CATEGORY (Verified):", flush=True)
    cur.execute("SELECT category, COUNT(*) FROM master_businesses WHERE verification_status = 'VERIFIED' GROUP BY category ORDER BY COUNT(*) DESC")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}", flush=True)
        
    if close_at_end:
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dar es Salaam Agrovet Research Pipeline Runner")
    parser.add_argument('--stage', choices=['pilot', 'full', 'cluster'], default='full', help="Pipeline stage to execute")
    parser.add_argument('--stats', action='store_true', help="Print current database metrics")
    args = parser.parse_args()
    
    if args.stats:
        print_database_stats()
    elif args.stage == 'cluster':
        run_cluster_pipeline_only()
    elif args.stage == 'full':
        run_full_pipeline()