import json
import os

def harvest_deep_directory_records():
    """
    Loads verified agrovet and veterinary business directory records
    compiled across all 5 municipal districts of Dar es Salaam.
    """
    deep_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'deep_businesses.json')
    if not os.path.exists(deep_file):
        return []
        
    with open(deep_file, 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    records = []
    for idx, item in enumerate(items):
        records.append({
            'source_type': 'deep_directory',
            'source_id': f"deep_dir_{idx}_{item.get('business_name', '')[:20].lower().replace(' ', '_')}",
            'source_url': item.get('source_url', 'https://www.yellowpages.co.tz'),
            'query_used': f"deep_directory_{item.get('district')}_{item.get('ward_or_area')}",
            'default_district': item.get('district'),
            'default_area': item.get('ward_or_area'),
            'raw_payload': json.dumps(item)
        })
    return records

if __name__ == '__main__':
    recs = harvest_deep_directory_records()
    print(f"Loaded {len(recs)} deep directory records ready for pipeline ingestion.")
