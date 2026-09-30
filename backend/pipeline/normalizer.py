import re

AGGREGATOR_PATTERNS = [
    r'^top\s*\d+\b',
    r'^best\s+\w+\s+in\s+dar\b',
    r'^find\s+(?:clinics|doctors|vets|businesses|shops)\b',
    r'^google\s*maps?$',
    r'^yellow\s*pages?$',
    r'^list\s+of\b',
    r'^reviews\s+for\b',
    r'^(?:tegeta|bunju|sinza|dar es salaam|kariakoo|kinondoni|ubungo|ilala|temeke|kigamboni)\s*,\s*(?:bagamoyo|morogoro|ali hassan|sam nujoma|nyerere)'
]

def is_directory_or_aggregator(title):
    if not title:
        return True
    t = title.lower().strip()
    for pat in AGGREGATOR_PATTERNS:
        if re.search(pat, t):
            return True
    return False

def clean_business_name(raw_name):
    if not raw_name:
        return ""
    name = raw_name.strip()
    
    # 1. Strip phone numbers at end of title e.g. " | 0712 000 610" or " - 0712..."
    name = re.sub(r'\s*[|\-–]\s*(?:\+?255|0)\s*\d{2,4}[\s\d-]{5,}\s*$', '', name)
    
    # 2. Strip common directory suffixes
    suffixes = [
        r'\s*-\s*Cybo.*$',
        r'\s*-\s*Facebook.*$',
        r'\s*-\s*Instagram.*$',
        r'\s*\|\s*Go Africa Online.*$',
        r'\s*-\s*Yellow Pages.*$',
        r'\s*\|\s*Brabys.*$',
        r'\s*-\s*Pharmacies\s*-\s*Go Africa Online.*$',
        r'\s*-\s*Find Local Businesses.*$',
        r'\s*-\s*FindHealthClinics.*$',
        r'\s*-\s*Medpages.*$',
        r'\s*-\s*B2BHint.*$',
        r'\s*\(202\d\).*$',
        r'\s*-\s*Supplier\s+.*$',
        r'^\s*About\s+',
        r'^\s*Contact Us\s*\|\s*',
        r'^\s*Welcome to\s+'
    ]
    for pattern in suffixes:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
    # 3. Clean trailing punctuation
    name = re.sub(r'[\.\s,|-]+$', '', name).strip()
    
    # 4. Remove location suffixes if separated by dash e.g. "Motisha Agrovet - Tegeta..."
    parts = re.split(r'\s*[-|–]\s*(?:Tegeta|Bunju|Sinza|Dar es Salaam|Ubungo|Kinondoni|Ilala|Temeke|Kigamboni)', name, flags=re.IGNORECASE)
    if parts and len(parts[0].strip()) > 2:
        name = parts[0].strip()
        
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def normalize_business_name_for_dedup(name):
    if not name:
        return ""
    clean = re.sub(r'[^a-zA-Z0-9]', '', name.lower())
    for word in ['limited', 'ltd', 'company', 'co', 'center', 'centre', 'shop', 'point', 'tz', 'tanzania', 'clinic', 'veterinary', 'agrovet']:
        clean = re.sub(r'^' + word, '', clean)
        clean = re.sub(word + r'$', '', clean)
    return clean

def extract_primary_brand_token(name):
    """Extracts distinctive brand token (e.g. 'joack', 'motisha', 'falcon', 'interchick') for robust local deduplication."""
    if not name:
        return ""
    words = re.findall(r'[a-zA-Z]{3,}', name.lower())
    stop_words = {'agrovet', 'center', 'centre', 'company', 'limited', 'ltd', 'shop', 'point', 'veterinary', 'vet', 'animal', 'feed', 'feeds', 'poultry', 'clinic', 'services', 'dar', 'salaam', 'tanzania'}
    brand_tokens = [w for w in words if w not in stop_words]
    return brand_tokens[0] if brand_tokens else ""

def extract_phone_numbers(text):
    if not text:
        return []
        
    found = []
    
    # Check for split Go Africa Online pattern: "25 56 57 10 63 63" -> +255 657 106 363
    go_matches = re.finditer(r'25\s*5\s*([67]\d)\s*(\d{2})\s*(\d{2})\s*(\d{2})', text)
    for m in go_matches:
        d = "255" + m.group(1) + m.group(2) + m.group(3) + m.group(4)
        formatted = f"+{d[:3]} {d[3:6]} {d[6:9]} {d[9:]}"
        if formatted not in found:
            found.append(formatted)
            
    patterns = [
        r'(?:\+?255|0)\s*([67]\d{1})\s*(\d{3})\s*(\d{4})',
        r'(?:\+?255|0)\s*([67]\d{2})\s*(\d{3})\s*(\d{3})',
        r'(?:\+?255|0)\s*([67]\d{8})',
        r'(?:\+?255|0)\s*(22\s*\d{3}\s*\d{4})',
        r'(?:\+?255|0)\s*(22\d{7})',
    ]
    
    for pat in patterns:
        for match in re.finditer(pat, text):
            raw_match = match.group(0)
            digits = re.sub(r'\D', '', raw_match)
            if digits.startswith('0') and len(digits) == 10:
                digits = '255' + digits[1:]
            elif digits.startswith('255') and len(digits) == 12:
                pass
            elif len(digits) == 9 and digits.startswith(('6', '7')):
                digits = '255' + digits
            else:
                continue
                
            if len(digits) == 12:
                formatted = f"+{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"
                if formatted not in found:
                    found.append(formatted)
                
    return found

def extract_email(text):
    if not text:
        return ""
    m = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    return m.group(0).lower() if m else ""

def extract_social_links(text, source_url=""):
    fb = ""
    insta = ""
    website = ""
    
    combined = f"{text} {source_url}"
    
    fb_m = re.search(r'(https?://(?:www\.)?facebook\.com/[a-zA-Z0-9._-]+)', combined)
    if fb_m:
        fb = fb_m.group(1)
        
    in_m = re.search(r'(https?://(?:www\.)?instagram\.com/[a-zA-Z0-9._-]+)', combined)
    if in_m:
        insta = in_m.group(1)
        
    web_m = re.search(r'(https?://(?!www\.facebook|facebook|www\.instagram|instagram|www\.cybo|cybo|www\.goafricaonline|goafricaonline|www\.yellowpages|yellowpages|www\.brabys|brabys|www\.openstreetmap|openstreetmap|medpages|b2bhint)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)', combined)
    if web_m:
        website = web_m.group(1)
        
    return website, fb, insta