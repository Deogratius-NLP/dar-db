import math
import re

DISTRICT_MAPPING = {
    # Kinondoni
    'tegeta': ('Kinondoni', 'Tegeta', -6.6667, 39.2167),
    'bunju': ('Kinondoni', 'Bunju', -6.6167, 39.1500),
    'kawe': ('Kinondoni', 'Kawe', -6.7333, 39.2333),
    'mikocheni': ('Kinondoni', 'Mikocheni', -6.7667, 39.2500),
    'masaki': ('Kinondoni', 'Masaki', -6.7450, 39.2800),
    'oyster bay': ('Kinondoni', 'Oyster Bay', -6.7700, 39.2750),
    'kijitonyama': ('Kinondoni', 'Kijitonyama', -6.7800, 39.2450),
    'mwenge': ('Kinondoni', 'Mwenge', -6.7720, 39.2280),
    'kinondoni': ('Kinondoni', 'Kinondoni', -6.7900, 39.2600),
    'kunduchi': ('Kinondoni', 'Kunduchi', -6.6800, 39.2100),
    'wazo': ('Kinondoni', 'Wazo', -6.6500, 39.1800),
    'boko': ('Kinondoni', 'Boko', -6.6300, 39.1700),
    'magomeni': ('Kinondoni', 'Magomeni', -6.8050, 39.2600),
    'tandale': ('Kinondoni', 'Tandale', -6.7950, 39.2400),
    'mwananyamala': ('Kinondoni', 'Mwananyamala', -6.7880, 39.2520),

    # Ubungo
    'sinza': ('Ubungo', 'Sinza', -6.7800, 39.2200),
    'ubungo': ('Ubungo', 'Ubungo', -6.7900, 39.2100),
    'kimara': ('Ubungo', 'Kimara', -6.7950, 39.1600),
    'mbezi': ('Ubungo', 'Mbezi', -6.7200, 39.1900),
    'mbezi beach': ('Kinondoni', 'Mbezi Beach', -6.7100, 39.2200),
    'mbezi juu': ('Ubungo', 'Mbezi Juu', -6.7120, 39.2020),
    'goba': ('Ubungo', 'Goba', -6.7250, 39.1450),
    'kibamba': ('Ubungo', 'Kibamba', -6.8000, 39.1000),
    'manzese': ('Ubungo', 'Manzese', -6.7980, 39.2350),
    'mabibo': ('Ubungo', 'Mabibo', -6.8100, 39.2250),
    'kinyerezi': ('Ilala', 'Kinyerezi', -6.8500, 39.1800), # border ward, officially Ilala

    # Ilala
    'kariakoo': ('Ilala', 'Kariakoo', -6.8200, 39.2780),
    'tabata': ('Ilala', 'Tabata', -6.8350, 39.2300),
    'buguruni': ('Ilala', 'Buguruni', -6.8300, 39.2500),
    'segerea': ('Ilala', 'Segerea', -6.8500, 39.2050),
    'vingunguti': ('Ilala', 'Vingunguti', -6.8400, 39.2400),
    'ilala': ('Ilala', 'Ilala', -6.8250, 39.2650),
    'kisutu': ('Ilala', 'Kisutu', -6.8150, 39.2850),
    'upanga': ('Ilala', 'Upanga', -6.8080, 39.2800),
    'kivukoni': ('Ilala', 'Kivukoni', -6.8150, 39.2950),
    'gongolamboto': ('Ilala', 'Gongolamboto', -6.8800, 39.1500),
    'ukonga': ('Ilala', 'Ukonga', -6.8650, 39.1800),
    'chanika': ('Ilala', 'Chanika', -6.9500, 39.1200),
    'pugu': ('Ilala', 'Pugu', -6.8900, 39.1050),

    # Temeke
    'mbagala': ('Temeke', 'Mbagala', -6.8900, 39.2600),
    'temeke': ('Temeke', 'Temeke', -6.8550, 39.2700),
    'changombe': ('Temeke', 'Chang''ombe', -6.8450, 39.2700),
    'tandika': ('Temeke', 'Tandika', -6.8600, 39.2650),
    'kurasini': ('Temeke', 'Kurasini', -6.8480, 39.2850),
    'yombo': ('Temeke', 'Yombo Vituka', -6.8700, 39.2450),
    'chamazi': ('Temeke', 'Chamazi', -6.9400, 39.2700),
    'toangoma': ('Temeke', 'Toangoma', -6.9200, 39.3100),

    # Kigamboni
    'kigamboni': ('Kigamboni', 'Kigamboni', -6.8300, 39.3100),
    'ferry': ('Kigamboni', 'Ferry', -6.8220, 39.3000),
    'vijibweni': ('Kigamboni', 'Vijibweni', -6.8500, 39.3200),
    'kibada': ('Kigamboni', 'Kibada', -6.8800, 39.3400),
    'gezaulole': ('Kigamboni', 'Gezaulole', -6.8900, 39.3800),
    'somangila': ('Kigamboni', 'Somangila', -6.9300, 39.4200)
}

def haversine_distance_km(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def resolve_geographic_location(text="", lat=None, lon=None, default_district=None, default_area=None):
    """
    Resolves district and area based on text hints and/or coordinates.
    Returns: (district, ward_or_area)
    """
    found_district = None
    found_area = None
    
    # 1. Text-based detection
    if text:
        clean_text = text.lower()
        # Sort area keys by descending length so "mbezi beach" matches before "mbezi"
        sorted_areas = sorted(DISTRICT_MAPPING.keys(), key=lambda x: len(x), reverse=True)
        for area_key in sorted_areas:
            if re.search(r'\b' + re.escape(area_key) + r'\b', clean_text):
                dist, standard_area, _, _ = DISTRICT_MAPPING[area_key]
                found_district = dist
                found_area = standard_area
                break
                
        # If no area found, check direct district names
        if not found_district:
            for d in ['Kinondoni', 'Ubungo', 'Ilala', 'Temeke', 'Kigamboni']:
                if re.search(r'\b' + re.escape(d.lower()) + r'\b', clean_text):
                    found_district = d
                    break
                    
    # 2. Coordinate-based proximity if coordinates available
    if (not found_district or not found_area) and lat and lon:
        try:
            f_lat = float(lat)
            f_lon = float(lon)
            # Find nearest known centroid within 5.0 km
            closest = None
            min_dist = 5.0 # km
            for key, (dist, std_area, c_lat, c_lon) in DISTRICT_MAPPING.items():
                d = haversine_distance_km(f_lat, f_lon, c_lat, c_lon)
                if d < min_dist:
                    min_dist = d
                    closest = (dist, std_area)
            if closest:
                found_district = closest[0]
                found_area = closest[1]
        except (ValueError, TypeError):
            pass

    # Fallback to query defaults if provided and still unknown
    if not found_district and default_district and default_district != 'All':
        found_district = default_district
    if not found_area and default_area and default_area != 'All':
        found_area = default_area
        
    return (found_district or "UNKNOWN", found_area or "UNKNOWN")

if __name__ == "__main__":
    print(resolve_geographic_location(text="Motisha Agrovet - Tegeta Wazo Barabara ya Bagamoyo"))
    print(resolve_geographic_location(lat=-6.780, lon=39.220))
    print(resolve_geographic_location(text="Kariakoo Market animal feed distributor"))
    print(resolve_geographic_location(text="Random shop without location info"))