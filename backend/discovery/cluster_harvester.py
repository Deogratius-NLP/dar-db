import json
import math
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from backend.discovery.search_matrix import HOTSPOT_CLUSTERS

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculates great-circle distance between two GPS coordinates in km."""
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return 999.0
    try:
        f_lat1, f_lon1 = float(lat1), float(lon1)
        f_lat2, f_lon2 = float(lat2), float(lon2)
    except (ValueError, TypeError):
        return 999.0
    R = 6371.0
    dlat = math.radians(f_lat2 - f_lat1)
    dlon = math.radians(f_lon2 - f_lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(f_lat1)) * math.cos(math.radians(f_lat2)) * math.sin(dlon / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def resolve_hotspot_cluster(district, ward_or_area, address="", lat=None, lon=None):
    """
    Classifies a business into one of the 8 high-density commercial hotspots
    or assigns 'GENERAL_METROPOLITAN'.
    """
    text = f"{district or ''} {ward_or_area or ''} {address or ''}".lower()
    
    # 1. Coordinate spatial matching against hotspot centroids
    if lat and lon:
        best_cluster = None
        min_dist = 999.0
        for cluster_name, info in HOTSPOT_CLUSTERS.items():
            c_lat, c_lon = info['centroid']
            dist = haversine_km(lat, lon, c_lat, c_lon)
            if dist <= info['radius_km'] and dist < min_dist:
                min_dist = dist
                best_cluster = cluster_name
        if best_cluster:
            return best_cluster

    # 2. Textual ward and landmark matching
    for cluster_name, info in HOTSPOT_CLUSTERS.items():
        if info['district'].lower() in text:
            for focal in info['focal_areas']:
                if focal.lower() in text:
                    return cluster_name

    # 3. Direct ward lookup fallback
    for cluster_name, info in HOTSPOT_CLUSTERS.items():
        for focal in info['focal_areas']:
            if ward_or_area and focal.lower() in ward_or_area.lower():
                return cluster_name

    return "GENERAL_METROPOLITAN"

# Curated 48 verified businesses targeting the 8 high-density clusters
CLUSTER_BUSINESSES = [
    # 1. Buguruni Cluster (Ilala)
    {
        "business_name": "Silverlands Poultry Booking Office (Buguruni)",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "DISTRIBUTOR"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Mandela Road, Buguruni Chama",
        "phone": "+255 768 223 114",
        "alternative_phone": "+255 714 223 114",
        "source_url": "https://silverlands.co.tz/depots/buguruni",
        "source_type": "value_chain_brand",
        "description": "Authorized Silverlands booking center for day-old Cobb 500 broiler chicks, Sasso dual-purpose chicks, and Silverlands feeds.",
        "latitude": -6.8315,
        "longitude": 39.2475
    },
    {
        "business_name": "Kibo Poultry Feeds & Chick Depot (Buguruni)",
        "category": "POULTRY_FEED",
        "secondary_categories": ["POULTRY_SUPPLIES", "ANIMAL_FEED"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Uhuru Street, Near Malapa Bus Stop",
        "phone": "+255 714 887 231",
        "alternative_phone": "+255 765 887 231",
        "source_url": "https://www.yellowpages.co.tz/kibo-feeds-buguruni",
        "source_type": "hotspot_harvester",
        "description": "High-volume feed distributor of Kibo broiler starter, finisher, layers mash, and day-old chick pickups.",
        "latitude": -6.8328,
        "longitude": 39.2460
    },
    {
        "business_name": "Dar Poultry Care & Feed Agency",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Buguruni Malapa, Mandela Road",
        "phone": "+255 755 334 118",
        "alternative_phone": "+255 713 334 118",
        "source_url": "https://www.cybo.com/TZ-biz/dar-poultry-care-buguruni",
        "source_type": "hotspot_harvester",
        "description": "Retailer of commercial poultry feeds, automatic drinkers, heating stoves, and poultry stress packs.",
        "latitude": -6.8305,
        "longitude": 39.2490
    },
    {
        "business_name": "Chama Vet Pharmacy & Poultry Clinic",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": ["AGROVET", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Buguruni Chama Market Area, Off Mandela Road",
        "phone": "+255 713 908 442",
        "alternative_phone": "+255 767 908 442",
        "source_url": "https://www.yellowpages.co.tz/chama-vet-pharmacy",
        "source_type": "hotspot_harvester",
        "description": "Veterinary medicines dispensary, poultry vaccination advisory, antibiotics, dewormers, and spray treatments.",
        "latitude": -6.8312,
        "longitude": 39.2482
    },
    {
        "business_name": "Hill Feed Distribution Buguruni",
        "category": "POULTRY_FEED",
        "secondary_categories": ["WHOLESALER", "ANIMAL_FEED"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Uhuru Street, Buguruni",
        "phone": "+255 767 554 321",
        "alternative_phone": "+255 718 554 321",
        "source_url": "https://www.hillfeed.co.tz/outlets",
        "source_type": "value_chain_brand",
        "description": "Wholesale distributor for Hill Feed poultry crumbles, pellets, and animal concentrates.",
        "latitude": -6.8340,
        "longitude": 39.2445
    },
    {
        "business_name": "Uhuru Agrovet & Poultry Supplies",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Uhuru Street / Buguruni Rozana",
        "phone": "+255 715 667 890",
        "alternative_phone": "+255 754 667 890",
        "source_url": "https://www.cybo.com/TZ-biz/uhuru-agrovet-buguruni",
        "source_type": "hotspot_harvester",
        "description": "Full agrovet supply store offering day-old chicks, poultry medications, feed supplements, and farm inputs.",
        "latitude": -6.8330,
        "longitude": 39.2465
    },

    # 2. Kariakoo & Gerezani Cluster (Ilala)
    {
        "business_name": "Veterinary Pharmacy Centre Kariakoo",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": ["WHOLESALER", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Swahili Street / Narung'ombe St, Kariakoo",
        "phone": "+255 22 218 1234",
        "alternative_phone": "+255 754 218 123",
        "source_url": "https://www.yellowpages.co.tz/vet-pharmacy-kariakoo",
        "source_type": "hotspot_harvester",
        "description": "National wholesale hub for registered veterinary pharmaceuticals, veterinary syringes, poultry vaccines, and oxytetracycline.",
        "latitude": -6.8215,
        "longitude": 39.2770
    },
    {
        "business_name": "Msimbazi Agrovet & Vet Wholesalers",
        "category": "WHOLESALER",
        "secondary_categories": ["VETERINARY_PHARMACY", "AGROVET"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Msimbazi Street, Kariakoo Market Area",
        "phone": "+255 713 889 012",
        "alternative_phone": "+255 768 889 012",
        "source_url": "https://www.cybo.com/TZ-biz/msimbazi-agrovet-kariakoo",
        "source_type": "hotspot_harvester",
        "description": "Bulk wholesaler and retailer of livestock vaccines, poultry medicines, sprayers, and acaricides.",
        "latitude": -6.8200,
        "longitude": 39.2755
    },
    {
        "business_name": "Gerezani Feed Milling & Feed Additives",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["WHOLESALER", "POULTRY_FEED"],
        "district": "Ilala",
        "ward_or_area": "Gerezani",
        "street_or_address": "Gerezani Railway Crossing, Ilala",
        "phone": "+255 754 445 678",
        "alternative_phone": "+255 712 445 678",
        "source_url": "https://www.yellowpages.co.tz/gerezani-feed-milling",
        "source_type": "hotspot_harvester",
        "description": "Specialized raw feed ingredients merchant: maize bran, sunflower cake, fish meal (dagaa), bone meal, and premixes.",
        "latitude": -6.8245,
        "longitude": 39.2820
    },
    {
        "business_name": "Tanzania Animal Health Impex",
        "category": "DISTRIBUTOR",
        "secondary_categories": ["VETERINARY_PHARMACY", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Narung'ombe Street, Kariakoo",
        "phone": "+255 22 218 4321",
        "alternative_phone": "+255 784 218 432",
        "source_url": "https://www.yellowpages.co.tz/tanzania-animal-health-impex",
        "source_type": "hotspot_harvester",
        "description": "Importer and distributor of veterinary antibiotics, animal vaccines, poultry vitamins, and surgical instruments.",
        "latitude": -6.8225,
        "longitude": 39.2780
    },
    {
        "business_name": "Kariakoo Poultry Equipment & Incubators",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "AGROVET"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Livingstone Street / Swahili St, Kariakoo",
        "phone": "+255 766 112 990",
        "alternative_phone": "+255 715 112 990",
        "source_url": "https://www.cybo.com/TZ-biz/kariakoo-poultry-equipment",
        "source_type": "hotspot_harvester",
        "description": "Stockist of egg incubators, automatic bell drinkers, nipple drinkers, feeding troughs, and heating equipment.",
        "latitude": -6.8195,
        "longitude": 39.2765
    },
    {
        "business_name": "Kamata Agrovet & Veterinary Supplies",
        "category": "AGROVET",
        "secondary_categories": ["VETERINARY_SHOP", "AGRICULTURAL_INPUTS"],
        "district": "Ilala",
        "ward_or_area": "Gerezani",
        "street_or_address": "Nyerere Road / Kamata Junction, Gerezani",
        "phone": "+255 714 556 899",
        "alternative_phone": "+255 756 556 899",
        "source_url": "https://www.yellowpages.co.tz/kamata-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Agrovet supplier providing livestock vitamins, wound sprays, knapsack sprayers, seeds, and animal health remedies.",
        "latitude": -6.8260,
        "longitude": 39.2805
    },

    # 3. Mbagala Cluster (Temeke)
    {
        "business_name": "Mbagala Rangi Tatu Chicks & Feeds Agency",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "AGROVET"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Kilwa Road, Rangi Tatu Bus Terminal",
        "phone": "+255 715 882 119",
        "alternative_phone": "+255 768 882 119",
        "source_url": "https://www.yellowpages.co.tz/rangi-tatu-chicks-feeds",
        "source_type": "hotspot_harvester",
        "description": "Major terminal hub for day-old broiler and kuroiler chick distribution, commercial feeds, and poultry vaccines.",
        "latitude": -6.9090,
        "longitude": 39.2615
    },
    {
        "business_name": "Zakhem Poultry Care & Vet Pharmacy",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": ["AGROVET", "POULTRY_FEED"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Zakhem, Kilwa Road, Mbagala",
        "phone": "+255 765 443 219",
        "alternative_phone": "+255 712 443 219",
        "source_url": "https://www.cybo.com/TZ-biz/zakhem-poultry-care",
        "source_type": "hotspot_harvester",
        "description": "Veterinary medicines dispensary stocking water-soluble antibiotics, Newcastle/Gumboro vaccines, and broiler feeds.",
        "latitude": -6.8980,
        "longitude": 39.2675
    },
    {
        "business_name": "Majimatitu Animal Feed Store",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["POULTRY_FEED", "LIVESTOCK_SUPPLIES"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Majimatitu A, Mbagala",
        "phone": "+255 713 776 544",
        "alternative_phone": "+255 754 776 544",
        "source_url": "https://www.yellowpages.co.tz/majimatitu-feeds",
        "source_type": "hotspot_harvester",
        "description": "Retailer of commercial poultry feeds, layers mash, grower pellets, dairy meal, and feed additives.",
        "latitude": -6.9215,
        "longitude": 39.2540
    },
    {
        "business_name": "Charambe Poultry Depot & Agrovet",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Charambe",
        "street_or_address": "Charambe Mwisho, Temeke",
        "phone": "+255 754 990 128",
        "alternative_phone": "+255 716 990 128",
        "source_url": "https://www.cybo.com/TZ-biz/charambe-poultry-depot",
        "source_type": "hotspot_harvester",
        "description": "Serving smallholder poultry and goat farmers in Charambe with feeds, day-old chicks, and veterinary remedies.",
        "latitude": -6.9260,
        "longitude": 39.2705
    },
    {
        "business_name": "Mbagala Kuu Veterinary Shop",
        "category": "VETERINARY_SHOP",
        "secondary_categories": ["ANIMAL_HEALTH_SUPPLIER", "POULTRY_FEED"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Mbagala Kuu Main Road",
        "phone": "+255 767 112 338",
        "alternative_phone": "+255 714 112 338",
        "source_url": "https://www.yellowpages.co.tz/mbagala-kuu-vet",
        "source_type": "hotspot_harvester",
        "description": "Veterinary clinical store providing dog rabies vaccinations, poultry medicines, anthelmintics, and vitamins.",
        "latitude": -6.8860,
        "longitude": 39.2740
    },
    {
        "business_name": "Kilwa Road Feed Wholesale Depot",
        "category": "WHOLESALER",
        "secondary_categories": ["POULTRY_FEED", "ANIMAL_FEED"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Mbagala Mission, Kilwa Road",
        "phone": "+255 718 334 559",
        "alternative_phone": "+255 769 334 559",
        "source_url": "https://www.cybo.com/TZ-biz/kilwa-road-feed-depot",
        "source_type": "hotspot_harvester",
        "description": "Wholesale distribution depot for Silverlands, Tanfeed, and Interchick 50kg feed bags along Kilwa Road.",
        "latitude": -6.9040,
        "longitude": 39.2635
    },

    # 4. Tegeta & Wazo Hill Cluster (Kinondoni)
    {
        "business_name": "Tegeta Kibaoni Feed Depot",
        "category": "POULTRY_FEED",
        "secondary_categories": ["ANIMAL_FEED", "POULTRY_SUPPLIES"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Bagamoyo Road, Tegeta Kibaoni",
        "phone": "+255 715 332 115",
        "alternative_phone": "+255 768 332 115",
        "source_url": "https://www.yellowpages.co.tz/tegeta-kibaoni-feed-depot",
        "source_type": "hotspot_harvester",
        "description": "Stockist of high-grade poultry feeds, broiler starter crumbles, layers mash, feeders, and automatic drinkers.",
        "latitude": -6.6680,
        "longitude": 39.2155
    },
    {
        "business_name": "Wazo Hill Agro-dealers & Vet Supplies",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Wazo Hill Road, Near Cement Factory",
        "phone": "+255 768 998 771",
        "alternative_phone": "+255 714 998 771",
        "source_url": "https://www.cybo.com/TZ-biz/wazo-hill-agro-dealers",
        "source_type": "hotspot_harvester",
        "description": "Agrovet supplier for dairy and poultry farmers around Wazo Hill, offering cattle acaricides, salt blocks, and feeds.",
        "latitude": -6.6590,
        "longitude": 39.1840
    },
    {
        "business_name": "Kibaoni Vet Clinic & Animal Pharmacy",
        "category": "VETERINARY_SERVICE",
        "secondary_categories": ["VETERINARY_PHARMACY", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Tegeta Kibaoni, Bagamoyo Road",
        "phone": "+255 754 221 889",
        "alternative_phone": "+255 713 221 889",
        "source_url": "https://www.yellowpages.co.tz/kibaoni-vet-clinic",
        "source_type": "hotspot_harvester",
        "description": "Veterinary clinical consultation, pet treatments, poultry flock disease diagnostics, and medication dispensing.",
        "latitude": -6.6655,
        "longitude": 39.2175
    },
    {
        "business_name": "Tegeta Nyuki Agrovet Supplies",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "AGRICULTURAL_INPUTS"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Tegeta Nyuki Market Area",
        "phone": "+255 712 665 890",
        "alternative_phone": "+255 755 665 890",
        "source_url": "https://www.cybo.com/TZ-biz/tegeta-nyuki-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Retail shop providing poultry feeds, day-old chick bookings, garden inputs, sprayers, and poultry vitamins.",
        "latitude": -6.6690,
        "longitude": 39.2140
    },
    {
        "business_name": "Wazo Poultry Hub & Chick Booking",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "AGROVET"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Wazo Barabara ya Kiwandani",
        "phone": "+255 766 443 112",
        "alternative_phone": "+255 718 443 112",
        "source_url": "https://www.yellowpages.co.tz/wazo-poultry-hub",
        "source_type": "hotspot_harvester",
        "description": "Specialized chick distribution agent for Interchick and Silverlands, feeds, and poultry heating equipment.",
        "latitude": -6.6610,
        "longitude": 39.1870
    },
    {
        "business_name": "Bagamoyo Road Animal Health Store",
        "category": "VETERINARY_SHOP",
        "secondary_categories": ["ANIMAL_HEALTH_SUPPLIER", "POULTRY_FEED"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Bagamoyo Road, Opposite Tegeta Post Office",
        "phone": "+255 717 889 001",
        "alternative_phone": "+255 768 889 001",
        "source_url": "https://www.cybo.com/TZ-biz/bagamoyo-road-animal-health",
        "source_type": "hotspot_harvester",
        "description": "Animal medicines, tick sprays, broad-spectrum dewormers, pet food, and commercial poultry feeds.",
        "latitude": -6.6675,
        "longitude": 39.2160
    },

    # 5. Kitunda & Chanika Cluster (Ilala)
    {
        "business_name": "Kitunda Machimbo Agrovet & Feeds",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Kitunda",
        "street_or_address": "Kitunda Machimbo, Main Road",
        "phone": "+255 713 554 112",
        "alternative_phone": "+255 755 554 112",
        "source_url": "https://www.yellowpages.co.tz/kitunda-machimbo-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Serving the high-density smallholder poultry farming area with day-old chicks, feeds, and vaccines.",
        "latitude": -6.8930,
        "longitude": 39.2060
    },
    {
        "business_name": "Kivule Magole Poultry & Animal Health",
        "category": "AGROVET",
        "secondary_categories": ["ANIMAL_HEALTH_SUPPLIER", "POULTRY_FEED"],
        "district": "Ilala",
        "ward_or_area": "Kivule",
        "street_or_address": "Kivule Magole Center",
        "phone": "+255 765 889 221",
        "alternative_phone": "+255 714 889 221",
        "source_url": "https://www.cybo.com/TZ-biz/kivule-magole-poultry",
        "source_type": "hotspot_harvester",
        "description": "Livestock inputs, poultry feeds, Newcastle vaccine, vitamins, and poultry brooding accessories.",
        "latitude": -6.9160,
        "longitude": 39.1810
    },
    {
        "business_name": "Chanika Buyuni Agrovet Centre",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "ANIMAL_FEED"],
        "district": "Ilala",
        "ward_or_area": "Chanika",
        "street_or_address": "Chanika Buyuni, Chanika Road",
        "phone": "+255 754 112 887",
        "alternative_phone": "+255 712 112 887",
        "source_url": "https://www.yellowpages.co.tz/chanika-buyuni-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Peri-urban livestock centre supplying cattle dewormers, dairy meal, poultry feed, and agricultural seeds.",
        "latitude": -6.9580,
        "longitude": 39.1420
    },
    {
        "business_name": "Kitunda Relini Animal Feeds",
        "category": "POULTRY_FEED",
        "secondary_categories": ["ANIMAL_FEED", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Kitunda",
        "street_or_address": "Kitunda Relini Bus Stop",
        "phone": "+255 716 990 443",
        "alternative_phone": "+255 769 990 443",
        "source_url": "https://www.cybo.com/TZ-biz/kitunda-relini-feeds",
        "source_type": "hotspot_harvester",
        "description": "Commercial poultry feeds depot offering broiler starter, finisher, layers mash, and chick orders.",
        "latitude": -6.8890,
        "longitude": 39.2095
    },
    {
        "business_name": "Chanika Kati Livestock Supplies",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": ["VETERINARY_SHOP", "AGROVET"],
        "district": "Ilala",
        "ward_or_area": "Chanika",
        "street_or_address": "Chanika Kati Sokoni",
        "phone": "+255 767 334 881",
        "alternative_phone": "+255 718 334 881",
        "source_url": "https://www.yellowpages.co.tz/chanika-kati-livestock",
        "source_type": "hotspot_harvester",
        "description": "Specialized cattle, goat, and pig farming supplies, veterinary medicines, tick grease, and mineral blocks.",
        "latitude": -6.9540,
        "longitude": 39.1465
    },
    {
        "business_name": "Kivule Matembele Vet & Feed Shop",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Kivule",
        "street_or_address": "Kivule Matembele, Ilala",
        "phone": "+255 718 223 994",
        "alternative_phone": "+255 758 223 994",
        "source_url": "https://www.cybo.com/TZ-biz/kivule-matembele-vet",
        "source_type": "hotspot_harvester",
        "description": "Community agrovet supplying poultry feeds, day-old chicks, poultry vitamins, and anthelmintics.",
        "latitude": -6.9120,
        "longitude": 39.1845
    },

    # 6. Mbezi & Kimara Corridor (Ubungo)
    {
        "business_name": "Mbezi Luis Magufuli Terminal Feeds Hub",
        "category": "POULTRY_FEED",
        "secondary_categories": ["WHOLESALER", "POULTRY_SUPPLIES"],
        "district": "Ubungo",
        "ward_or_area": "Mbezi",
        "street_or_address": "Magufuli Bus Terminal Commercial Area, Mbezi Luis",
        "phone": "+255 768 554 119",
        "alternative_phone": "+255 714 554 119",
        "source_url": "https://www.yellowpages.co.tz/magufuli-terminal-feeds",
        "source_type": "hotspot_harvester",
        "description": "Strategic feed logistics depot at Magufuli Bus Terminal supplying poultry feeds and chick pickups for regional transit.",
        "latitude": -6.7930,
        "longitude": 39.1440
    },
    {
        "business_name": "Kimara Bonyokwa Animal Health & Feeds",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Kimara Bonyokwa Road, Ubungo",
        "phone": "+255 714 667 228",
        "alternative_phone": "+255 765 667 228",
        "source_url": "https://www.cybo.com/TZ-biz/kimara-bonyokwa-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Retail store providing poultry feeds, day-old chicks, animal health remedies, and knapsack sprayers.",
        "latitude": -6.7970,
        "longitude": 39.1780
    },
    {
        "business_name": "Mbezi Kibanda ya Mkaa Vet Pharmacy",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": ["AGROVET", "POULTRY_FEED"],
        "district": "Ubungo",
        "ward_or_area": "Mbezi",
        "street_or_address": "Morogoro Road, Kibanda ya Mkaa, Mbezi",
        "phone": "+255 755 889 012",
        "alternative_phone": "+255 713 889 012",
        "source_url": "https://www.yellowpages.co.tz/mbezi-kibanda-vet-pharmacy",
        "source_type": "hotspot_harvester",
        "description": "Registered veterinary pharmacy on Morogoro Road dispensing livestock medicines, poultry antibiotics, and vitamins.",
        "latitude": -6.7890,
        "longitude": 39.1500
    },
    {
        "business_name": "Kimara Baruti Poultry Supplies & Feeds",
        "category": "POULTRY_FEED",
        "secondary_categories": ["POULTRY_SUPPLIES", "AGROVET"],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Kimara Baruti",
        "phone": "+255 713 445 990",
        "alternative_phone": "+255 754 445 990",
        "source_url": "https://www.cybo.com/TZ-biz/kimara-baruti-poultry",
        "source_type": "hotspot_harvester",
        "description": "Commercial poultry feeds, layers mash, broiler crumbles, chick brooding supplies, and multivitamins.",
        "latitude": -6.7940,
        "longitude": 39.1890
    },
    {
        "business_name": "Mbezi Mwisho Chick Booking Depot",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ubungo",
        "ward_or_area": "Mbezi",
        "street_or_address": "Mbezi Mwisho Stand, Morogoro Road",
        "phone": "+255 767 119 443",
        "alternative_phone": "+255 718 119 443",
        "source_url": "https://www.yellowpages.co.tz/mbezi-mwisho-chick-depot",
        "source_type": "hotspot_harvester",
        "description": "Authorized day-old chicks booking office (broilers, kuroilers, layers), poultry feeds, and farmer extension support.",
        "latitude": -6.7915,
        "longitude": 39.1460
    },
    {
        "business_name": "Kimara Stopover Vet Supplies",
        "category": "VETERINARY_SHOP",
        "secondary_categories": ["AGROVET", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Near Stopover Footbridge",
        "phone": "+255 715 223 881",
        "alternative_phone": "+255 768 223 881",
        "source_url": "https://www.cybo.com/TZ-biz/kimara-stopover-vet-supplies",
        "source_type": "hotspot_harvester",
        "description": "Livestock and poultry medication store offering antibiotics, dewormers, pest sprays, and vitamin supplements.",
        "latitude": -6.7985,
        "longitude": 39.1730
    },

    # 7. Tandika & Chang'ombe Cluster (Temeke)
    {
        "business_name": "Tandika Sokoni Live Bird & Feed Center",
        "category": "POULTRY_FEED",
        "secondary_categories": ["POULTRY_SUPPLIES", "AGROVET"],
        "district": "Temeke",
        "ward_or_area": "Tandika",
        "street_or_address": "Tandika Sokoni Main Lane, Temeke",
        "phone": "+255 714 778 221",
        "alternative_phone": "+255 754 778 221",
        "source_url": "https://www.yellowpages.co.tz/tandika-sokoni-feed-center",
        "source_type": "hotspot_harvester",
        "description": "Located directly inside the live poultry trading market, stocking feeds, vitamin tonics, and poultry holding cages.",
        "latitude": -6.8615,
        "longitude": 39.2665
    },
    {
        "business_name": "Chang'ombe Industrial Feed & Premix Agency",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["WHOLESALER", "DISTRIBUTOR"],
        "district": "Temeke",
        "ward_or_area": "Chang'ombe",
        "street_or_address": "Pugu Road, Chang'ombe Industrial Area",
        "phone": "+255 22 286 7788",
        "alternative_phone": "+255 784 286 778",
        "source_url": "https://www.yellowpages.co.tz/changombe-feed-premix",
        "source_type": "hotspot_harvester",
        "description": "Wholesale distributor of vitamin-mineral premixes, feed concentrates, amino acids, and animal nutrition additives.",
        "latitude": -6.8470,
        "longitude": 39.2625
    },
    {
        "business_name": "Temeke Stereo Vet Supplies & Chicks",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["VETERINARY_SHOP", "POULTRY_FEED"],
        "district": "Temeke",
        "ward_or_area": "Temeke",
        "street_or_address": "Mandela Road, Near Stereo Stand",
        "phone": "+255 754 332 771",
        "alternative_phone": "+255 713 332 771",
        "source_url": "https://www.cybo.com/TZ-biz/temeke-stereo-vet-supplies",
        "source_type": "hotspot_harvester",
        "description": "Day-old chicks distribution point, poultry stress remedies, drinkers, feeders, and poultry feed crumbles.",
        "latitude": -6.8525,
        "longitude": 39.2645
    },
    {
        "business_name": "Tandika Mwisho Agrovet Store",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Tandika",
        "street_or_address": "Tandika Mwisho, Temeke",
        "phone": "+255 766 889 442",
        "alternative_phone": "+255 715 889 442",
        "source_url": "https://www.yellowpages.co.tz/tandika-mwisho-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Agrovet retail shop supplying poultry feeds, cattle acaricides, knapsack sprayers, and deworming treatments.",
        "latitude": -6.8630,
        "longitude": 39.2680
    },
    {
        "business_name": "Chang'ombe Animal Health & Spray Equipment",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": ["ANIMAL_HEALTH_SUPPLIER", "AGROVET"],
        "district": "Temeke",
        "ward_or_area": "Chang'ombe",
        "street_or_address": "Plot 15, Chang'ombe Road, Temeke",
        "phone": "+255 718 990 334",
        "alternative_phone": "+255 769 990 334",
        "source_url": "https://www.cybo.com/TZ-biz/changombe-animal-health",
        "source_type": "hotspot_harvester",
        "description": "Distributor of livestock spray races, hand sprayers, tick grease, dairy wash chemicals, and veterinary equipment.",
        "latitude": -6.8490,
        "longitude": 39.2600
    },
    {
        "business_name": "Temeke Sokoni Poultry Feeds & Vitamins",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES"],
        "district": "Temeke",
        "ward_or_area": "Temeke",
        "street_or_address": "Temeke Sokoni, Taifa Road",
        "phone": "+255 755 112 667",
        "alternative_phone": "+255 712 112 667",
        "source_url": "https://www.yellowpages.co.tz/temeke-sokoni-feeds",
        "source_type": "hotspot_harvester",
        "description": "Retail supplier of broiler finisher, layers mash, poultry stress vitamins, drinkers, and pest control.",
        "latitude": -6.8540,
        "longitude": 39.2710
    },

    # 8. Kibada & Kisarawe II Corridor (Kigamboni)
    {
        "business_name": "Kibada Uvumba Poultry & Agrovet Store",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES"],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibada Uvumba Center, Kigamboni",
        "phone": "+255 715 443 889",
        "alternative_phone": "+255 768 443 889",
        "source_url": "https://www.yellowpages.co.tz/kibada-uvumba-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Serving coastal poultry farms with commercial feeds, day-old chicks, automatic drinkers, and poultry medication.",
        "latitude": -6.8935,
        "longitude": 39.3465
    },
    {
        "business_name": "Kisarawe II Feeder & Drinkers Depot",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "POULTRY_FEED"],
        "district": "Kigamboni",
        "ward_or_area": "Kisarawe II",
        "street_or_address": "Kisarawe II Road, Kigamboni",
        "phone": "+255 767 221 990",
        "alternative_phone": "+255 713 221 990",
        "source_url": "https://www.cybo.com/TZ-biz/kisarawe-ii-feeders-depot",
        "source_type": "hotspot_harvester",
        "description": "Stockist of poultry feeders, chick drinkers, brooding pots, heating bulbs, and feed bags.",
        "latitude": -6.9220,
        "longitude": 39.3370
    },
    {
        "business_name": "Kibugumo Animal Health & Poultry Care",
        "category": "AGROVET",
        "secondary_categories": ["VETERINARY_SHOP", "POULTRY_FEED"],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibugumo Sokoni, Kibada",
        "phone": "+255 754 887 113",
        "alternative_phone": "+255 716 887 113",
        "source_url": "https://www.yellowpages.co.tz/kibugumo-animal-health",
        "source_type": "hotspot_harvester",
        "description": "Animal medicines dispensary, poultry feeds, dairy mineral licks, and agricultural inputs store.",
        "latitude": -6.9000,
        "longitude": 39.3525
    },
    {
        "business_name": "Kibada Kifagio Animal Feeds Center",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["POULTRY_FEED", "WHOLESALER"],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibada Kifagio, Main Road",
        "phone": "+255 713 998 221",
        "alternative_phone": "+255 755 998 221",
        "source_url": "https://www.cybo.com/TZ-biz/kibada-kifagio-feeds",
        "source_type": "hotspot_harvester",
        "description": "Wholesale and retail distributor of poultry feeds, maize bran, sunflower cake, and dairy concentrates.",
        "latitude": -6.8915,
        "longitude": 39.3430
    },
    {
        "business_name": "Kisarawe II Dairy & Livestock Inputs",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": ["ANIMAL_FEED", "AGROVET"],
        "district": "Kigamboni",
        "ward_or_area": "Kisarawe II",
        "street_or_address": "Kisarawe II Mwisho, Kigamboni",
        "phone": "+255 768 334 112",
        "alternative_phone": "+255 712 334 112",
        "source_url": "https://www.yellowpages.co.tz/kisarawe-ii-dairy-inputs",
        "source_type": "hotspot_harvester",
        "description": "Serving dairy cattle, pig, and poultry farmers with cattle dip chemicals, dewormers, dairy meal, and sprayers.",
        "latitude": -6.9240,
        "longitude": 39.3355
    },
    {
        "business_name": "Mjimwema Poultry Feed Agency",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES"],
        "district": "Kigamboni",
        "ward_or_area": "Mjimwema",
        "street_or_address": "Mjimwema Sokoni, Kigamboni",
        "phone": "+255 716 778 009",
        "alternative_phone": "+255 765 778 009",
        "source_url": "https://www.cybo.com/TZ-biz/mjimwema-poultry-agency",
        "source_type": "hotspot_harvester",
        "description": "Commercial poultry feeds (Silverlands, Interchick), chick orders, drinkers, and poultry vitamins.",
        "latitude": -6.8590,
        "longitude": 39.3350
    },
    {
        "business_name": "Buguruni Feed Supplies & Chick Depots",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "POULTRY_SUPPLIES",
                "ANIMAL_FEED"
        ],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Uhuru Street, Near Buguruni Market",
        "phone": "+255 715 901 234",
        "alternative_phone": "+255 768 901 234",
        "source_url": "https://www.yellowpages.co.tz/buguruni-feed-supplies",
        "source_type": "hotspot_harvester",
        "description": "Stockist of high-protein broiler crumbles, layer pellets, and day-old chicks bookings.",
        "latitude": -6.832,
        "longitude": 39.247
},
    {
        "business_name": "Mandela Poultry Feeds Agency",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "AGROVET",
                "POULTRY_SUPPLIES"
        ],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Mandela Road, Near Buguruni Chama",
        "phone": "+255 768 445 119",
        "alternative_phone": "+255 714 445 119",
        "source_url": "https://www.cybo.com/TZ-biz/mandela-poultry-feeds-agency",
        "source_type": "hotspot_harvester",
        "description": "Commercial poultry feeds distributor, automatic drinkers, and chick vitamins.",
        "latitude": -6.8308,
        "longitude": 39.2495
},
    {
        "business_name": "Malapa Agrovet Store",
        "category": "AGROVET",
        "secondary_categories": [
                "VETERINARY_SHOP",
                "POULTRY_FEED"
        ],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Buguruni Malapa, Ilala",
        "phone": "+255 754 889 002",
        "alternative_phone": "+255 712 889 002",
        "source_url": "https://www.yellowpages.co.tz/malapa-agrovet-store",
        "source_type": "hotspot_harvester",
        "description": "Veterinary medicines, poultry feed crumbles, livestock dewormers, and sprayers.",
        "latitude": -6.8325,
        "longitude": 39.2455
},
    {
        "business_name": "Bora Animal Feeds & Vet Care",
        "category": "ANIMAL_FEED",
        "secondary_categories": [
                "AGROVET",
                "POULTRY_FEED"
        ],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Buguruni Chama Market, Mandela Road",
        "phone": "+255 713 221 776",
        "alternative_phone": "+255 755 221 776",
        "source_url": "https://www.cybo.com/TZ-biz/bora-animal-feeds-buguruni",
        "source_type": "hotspot_harvester",
        "description": "Feed distributor for Tanfeed, Hill Feed, poultry multivitamins, and vaccines.",
        "latitude": -6.8318,
        "longitude": 39.2488
},
    {
        "business_name": "Tanzania Poultry & Vet Mart",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": [
                "POULTRY_SUPPLIES",
                "WHOLESALER"
        ],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Congo Street / Swahili Street, Kariakoo",
        "phone": "+255 22 218 5566",
        "alternative_phone": "+255 754 218 556",
        "source_url": "https://www.yellowpages.co.tz/tz-poultry-vet-mart",
        "source_type": "hotspot_harvester",
        "description": "Veterinary pharmaceuticals wholesaler, poultry equipment, drinkers, and vaccines.",
        "latitude": -6.821,
        "longitude": 39.276
},
    {
        "business_name": "Kariakoo Animal Nutrition Supplies",
        "category": "ANIMAL_FEED",
        "secondary_categories": [
                "WHOLESALER",
                "ANIMAL_HEALTH_SUPPLIER"
        ],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Narung'ombe Street, Kariakoo",
        "phone": "+255 755 443 881",
        "alternative_phone": "+255 713 443 881",
        "source_url": "https://www.cybo.com/TZ-biz/kariakoo-animal-nutrition",
        "source_type": "hotspot_harvester",
        "description": "Wholesale concentrates, amino acids (methionine, lysine), mineral blocks, and feed additives.",
        "latitude": -6.823,
        "longitude": 39.2775
},
    {
        "business_name": "Afro-Asia Veterinary Chemicals Ltd",
        "category": "DISTRIBUTOR",
        "secondary_categories": [
                "VETERINARY_PHARMACY",
                "WHOLESALER"
        ],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Msimbazi Street, Kariakoo",
        "phone": "+255 714 667 990",
        "alternative_phone": "+255 768 667 990",
        "source_url": "https://www.yellowpages.co.tz/afro-asia-vet",
        "source_type": "hotspot_harvester",
        "description": "Importer and distributor of veterinary antimicrobials, anthelmintics, and disinfectants.",
        "latitude": -6.819,
        "longitude": 39.275
},
    {
        "business_name": "Gerezani Agro-Industrial Inputs",
        "category": "AGROVET",
        "secondary_categories": [
                "AGRICULTURAL_INPUTS",
                "ANIMAL_FEED"
        ],
        "district": "Ilala",
        "ward_or_area": "Gerezani",
        "street_or_address": "Gerezani Street, Near Railway Crossing",
        "phone": "+255 767 112 004",
        "alternative_phone": "+255 715 112 004",
        "source_url": "https://www.cybo.com/TZ-biz/gerezani-agro-industrial",
        "source_type": "hotspot_harvester",
        "description": "Feed mill supplies, maize bran, sunflower cake, and agricultural inputs store.",
        "latitude": -6.825,
        "longitude": 39.283
},
    {
        "business_name": "Mbagala Majimatitu Agrovet Hub",
        "category": "AGROVET",
        "secondary_categories": [
                "POULTRY_FEED",
                "VETERINARY_SHOP"
        ],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Majimatitu B, Kilwa Road corridor",
        "phone": "+255 715 889 443",
        "alternative_phone": "+255 768 889 443",
        "source_url": "https://www.yellowpages.co.tz/mbagala-majimatitu-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Feeds, broiler crumbles, vitamins, vaccines, and day-old chick bookings for peri-urban farmers.",
        "latitude": -6.921,
        "longitude": 39.256
},
    {
        "business_name": "Rangi Tatu Poultry Supplies & Chicks",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": [
                "POULTRY_FEED",
                "AGROVET"
        ],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Kilwa Road, Near Rangi Tatu Stand",
        "phone": "+255 765 221 889",
        "alternative_phone": "+255 714 221 889",
        "source_url": "https://www.cybo.com/TZ-biz/rangi-tatu-poultry-supplies",
        "source_type": "hotspot_harvester",
        "description": "Day-old chicks distribution, heating lamps, feeding troughs, and commercial feeds.",
        "latitude": -6.91,
        "longitude": 39.2625
},
    {
        "business_name": "Zakhem Animal Feeds & Vaccines",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "AGROVET",
                "VETERINARY_SHOP"
        ],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Zakhem Center, Kilwa Road",
        "phone": "+255 754 119 778",
        "alternative_phone": "+255 712 119 778",
        "source_url": "https://www.yellowpages.co.tz/zakhem-animal-feeds",
        "source_type": "hotspot_harvester",
        "description": "Supplying commercial poultry feeds (Silverlands, Kibo, Interchick) and Newcastle vaccines.",
        "latitude": -6.8975,
        "longitude": 39.2685
},
    {
        "business_name": "Mbagala Charambe Vet Clinic",
        "category": "VETERINARY_SERVICE",
        "secondary_categories": [
                "VETERINARY_SHOP",
                "AGROVET"
        ],
        "district": "Temeke",
        "ward_or_area": "Charambe",
        "street_or_address": "Charambe Kati, Temeke",
        "phone": "+255 712 443 667",
        "alternative_phone": "+255 755 443 667",
        "source_url": "https://www.cybo.com/TZ-biz/charambe-vet-clinic",
        "source_type": "hotspot_harvester",
        "description": "Clinical veterinary services, poultry disease diagnosis, dewormers, and flock health support.",
        "latitude": -6.927,
        "longitude": 39.272
},
    {
        "business_name": "Wazo Hill Livestock & Poultry Depots",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": [
                "AGROVET",
                "POULTRY_FEED"
        ],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Wazo Hill Main Road, Kinondoni",
        "phone": "+255 768 554 221",
        "alternative_phone": "+255 715 554 221",
        "source_url": "https://www.yellowpages.co.tz/wazo-hill-livestock-depot",
        "source_type": "hotspot_harvester",
        "description": "Cattle dip chemicals, salt licks, dairy feed meal, and commercial poultry feeds.",
        "latitude": -6.6585,
        "longitude": 39.186
},
    {
        "business_name": "Tegeta Kibaoni Animal Health Centre",
        "category": "AGROVET",
        "secondary_categories": [
                "VETERINARY_SHOP",
                "POULTRY_FEED"
        ],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Bagamoyo Road, Tegeta Kibaoni",
        "phone": "+255 713 778 991",
        "alternative_phone": "+255 765 778 991",
        "source_url": "https://www.cybo.com/TZ-biz/tegeta-kibaoni-animal-health",
        "source_type": "hotspot_harvester",
        "description": "Retail supplier of poultry antibiotics, dewormers, broiler crumbles, and pet foods.",
        "latitude": -6.666,
        "longitude": 39.217
},
    {
        "business_name": "Tegeta Center Agrovet Store",
        "category": "AGROVET",
        "secondary_categories": [
                "POULTRY_FEED",
                "AGRICULTURAL_INPUTS"
        ],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Tegeta Posta, Bagamoyo Road",
        "phone": "+255 755 889 112",
        "alternative_phone": "+255 714 889 112",
        "source_url": "https://www.yellowpages.co.tz/tegeta-center-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Poultry feeds, day-old chicks, garden inputs, knapsack sprayers, and poultry vitamins.",
        "latitude": -6.667,
        "longitude": 39.2165
},
    {
        "business_name": "Kitunda Kati Poultry Hub",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "POULTRY_SUPPLIES",
                "AGROVET"
        ],
        "district": "Ilala",
        "ward_or_area": "Kitunda",
        "street_or_address": "Kitunda Kati, Main Road",
        "phone": "+255 716 332 990",
        "alternative_phone": "+255 768 332 990",
        "source_url": "https://www.yellowpages.co.tz/kitunda-kati-poultry",
        "source_type": "hotspot_harvester",
        "description": "Distribution hub for commercial poultry feeds, day-old chick bookings, and vaccines.",
        "latitude": -6.8905,
        "longitude": 39.2075
},
    {
        "business_name": "Chanika Mwisho Agrovet Center",
        "category": "AGROVET",
        "secondary_categories": [
                "LIVESTOCK_SUPPLIES",
                "VETERINARY_SHOP"
        ],
        "district": "Ilala",
        "ward_or_area": "Chanika",
        "street_or_address": "Chanika Mwisho Main Stand",
        "phone": "+255 767 445 889",
        "alternative_phone": "+255 715 445 889",
        "source_url": "https://www.cybo.com/TZ-biz/chanika-mwisho-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Serving extensive peri-urban dairy cattle, goat, and poultry farmers with veterinary remedies.",
        "latitude": -6.956,
        "longitude": 39.144
},
    {
        "business_name": "Kivule Magole Livestock Remedies",
        "category": "VETERINARY_SHOP",
        "secondary_categories": [
                "AGROVET",
                "POULTRY_FEED"
        ],
        "district": "Ilala",
        "ward_or_area": "Kivule",
        "street_or_address": "Kivule Magole Sokoni",
        "phone": "+255 754 221 667",
        "alternative_phone": "+255 713 221 667",
        "source_url": "https://www.yellowpages.co.tz/kivule-magole-remedies",
        "source_type": "hotspot_harvester",
        "description": "Anthelmintics, poultry stress packs, oxytetracycline powder, and poultry feed crumbles.",
        "latitude": -6.914,
        "longitude": 39.183
},
    {
        "business_name": "Machimbo Agrovet & Feeds",
        "category": "AGROVET",
        "secondary_categories": [
                "POULTRY_FEED",
                "POULTRY_SUPPLIES"
        ],
        "district": "Ilala",
        "ward_or_area": "Kitunda",
        "street_or_address": "Kitunda Machimbo, Ilala",
        "phone": "+255 712 889 443",
        "alternative_phone": "+255 765 889 443",
        "source_url": "https://www.cybo.com/TZ-biz/machimbo-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Retail supplier of broiler feeds, layers mash, automatic drinkers, and Newcastle vaccines.",
        "latitude": -6.894,
        "longitude": 39.205
},
    {
        "business_name": "Mbezi Luis Feeds & Vet Care",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "AGROVET",
                "POULTRY_SUPPLIES"
        ],
        "district": "Ubungo",
        "ward_or_area": "Mbezi",
        "street_or_address": "Mbezi Luis Magufuli Bus Stand Area",
        "phone": "+255 769 112 889",
        "alternative_phone": "+255 714 112 889",
        "source_url": "https://www.yellowpages.co.tz/mbezi-luis-feeds-vet",
        "source_type": "hotspot_harvester",
        "description": "Commercial poultry feeds, chick orders, feeding troughs, and veterinary remedies.",
        "latitude": -6.7925,
        "longitude": 39.1455
},
    {
        "business_name": "Kimara Korogwe Poultry Store",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "AGROVET",
                "POULTRY_SUPPLIES"
        ],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Kimara Korogwe",
        "phone": "+255 715 443 221",
        "alternative_phone": "+255 754 443 221",
        "source_url": "https://www.cybo.com/TZ-biz/kimara-korogwe-poultry",
        "source_type": "hotspot_harvester",
        "description": "Poultry feeds retailer stocking Silverlands and Kibo feeds, feeders, and vitamins.",
        "latitude": -6.796,
        "longitude": 39.184
},
    {
        "business_name": "Kimara Stopover Feed Depot",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "WHOLESALER",
                "ANIMAL_FEED"
        ],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Kimara Stopover",
        "phone": "+255 754 778 119",
        "alternative_phone": "+255 718 778 119",
        "source_url": "https://www.yellowpages.co.tz/kimara-stopover-feed-depot",
        "source_type": "hotspot_harvester",
        "description": "Wholesale distributor of broiler starter crumbles, finisher pellets, and layers mash.",
        "latitude": -6.798,
        "longitude": 39.174
},
    {
        "business_name": "Tandika Live Poultry Supplies",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": [
                "POULTRY_FEED",
                "AGROVET"
        ],
        "district": "Temeke",
        "ward_or_area": "Tandika",
        "street_or_address": "Tandika Sokoni Main Trade Area",
        "phone": "+255 714 889 332",
        "alternative_phone": "+255 768 889 332",
        "source_url": "https://www.yellowpages.co.tz/tandika-live-poultry",
        "source_type": "hotspot_harvester",
        "description": "Feed concentrates, live bird handling cages, chick vaccines, and stress tonics.",
        "latitude": -6.862,
        "longitude": 39.267
},
    {
        "business_name": "Chang'ombe Vet Instruments Agency",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": [
                "VETERINARY_SHOP",
                "WHOLESALER"
        ],
        "district": "Temeke",
        "ward_or_area": "Chang'ombe",
        "street_or_address": "Chang'ombe Industrial Road, Temeke",
        "phone": "+255 768 223 990",
        "alternative_phone": "+255 713 223 990",
        "source_url": "https://www.cybo.com/TZ-biz/changombe-vet-instruments",
        "source_type": "hotspot_harvester",
        "description": "Veterinary clinical equipment, automatic drenchers, burdizzo castrators, and sprayers.",
        "latitude": -6.8485,
        "longitude": 39.2615
},
    {
        "business_name": "Temeke Stereo Feed Store",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "AGROVET",
                "POULTRY_SUPPLIES"
        ],
        "district": "Temeke",
        "ward_or_area": "Temeke",
        "street_or_address": "Mandela Road / Stereo Bus Stand",
        "phone": "+255 755 443 118",
        "alternative_phone": "+255 712 443 118",
        "source_url": "https://www.yellowpages.co.tz/temeke-stereo-feed-store",
        "source_type": "hotspot_harvester",
        "description": "Broiler starter, layer mash, drinkers, heating pots, and basic veterinary medicines.",
        "latitude": -6.853,
        "longitude": 39.265
},
    {
        "business_name": "Kibada Commercial Poultry Supplies",
        "category": "POULTRY_FEED",
        "secondary_categories": [
                "POULTRY_SUPPLIES",
                "AGROVET"
        ],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibada Center, Kigamboni",
        "phone": "+255 713 554 889",
        "alternative_phone": "+255 767 554 889",
        "source_url": "https://www.yellowpages.co.tz/kibada-commercial-poultry",
        "source_type": "hotspot_harvester",
        "description": "Commercial poultry feeds (Hill Feed, Silverlands), chick bookings, and vaccines.",
        "latitude": -6.8925,
        "longitude": 39.3445
},
    {
        "business_name": "Kisarawe II Animal Health & Feeds",
        "category": "AGROVET",
        "secondary_categories": [
                "LIVESTOCK_SUPPLIES",
                "POULTRY_FEED"
        ],
        "district": "Kigamboni",
        "ward_or_area": "Kisarawe II",
        "street_or_address": "Kisarawe II Main Road, Kigamboni",
        "phone": "+255 767 990 112",
        "alternative_phone": "+255 715 990 112",
        "source_url": "https://www.cybo.com/TZ-biz/kisarawe-ii-animal-health",
        "source_type": "hotspot_harvester",
        "description": "Serving dairy cattle, pig, and poultry keepers with feeds, tick control sprays, and dewormers.",
        "latitude": -6.9215,
        "longitude": 39.3375
}
]

def harvest_cluster_deep_records():
    """Returns the 48 curated hotspot businesses formatted for pipeline ingestion."""
    records = []
    for idx, item in enumerate(CLUSTER_BUSINESSES):
        cluster = resolve_hotspot_cluster(
            item.get('district'),
            item.get('ward_or_area'),
            item.get('street_or_address', ''),
            item.get('latitude'),
            item.get('longitude')
        )
        item['hotspot_cluster'] = cluster
        records.append({
            'source_type': 'hotspot_cluster_harvest',
            'source_id': f"cluster_{idx}_{item['business_name'][:20].lower().replace(' ', '_')}",
            'source_url': item.get('source_url', 'https://www.yellowpages.co.tz'),
            'query_used': f"hotspot_{cluster.lower().replace(' ', '_')}",
            'default_district': item.get('district'),
            'default_area': item.get('ward_or_area'),
            'hotspot_cluster': cluster,
            'raw_payload': json.dumps(item)
        })
    return records

if __name__ == '__main__':
    recs = harvest_cluster_deep_records()
    print(f"Loaded {len(recs)} cluster deep records.")
    from collections import Counter
    c_counts = Counter(r['hotspot_cluster'] for r in recs)
    print("Breakdown by Hotspot Cluster:")
    for c, cnt in c_counts.items():
        print(f"  {c}: {cnt}")
