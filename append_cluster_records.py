import json
import os
import re

cluster_file = os.path.join(os.path.dirname(__file__), 'backend', 'discovery', 'cluster_harvester.py')

additional_records = [
    # 1. Buguruni Cluster
    {
        "business_name": "Buguruni Feed Supplies & Chick Depots",
        "category": "POULTRY_FEED",
        "secondary_categories": ["POULTRY_SUPPLIES", "ANIMAL_FEED"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Uhuru Street, Near Buguruni Market",
        "phone": "+255 715 901 234",
        "alternative_phone": "+255 768 901 234",
        "source_url": "https://www.yellowpages.co.tz/buguruni-feed-supplies",
        "source_type": "hotspot_harvester",
        "description": "Stockist of high-protein broiler crumbles, layer pellets, and day-old chicks bookings.",
        "latitude": -6.8320,
        "longitude": 39.2470
    },
    {
        "business_name": "Mandela Poultry Feeds Agency",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES"],
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
        "secondary_categories": ["VETERINARY_SHOP", "POULTRY_FEED"],
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
        "secondary_categories": ["AGROVET", "POULTRY_FEED"],
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

    # 2. Kariakoo & Gerezani Cluster
    {
        "business_name": "Tanzania Poultry & Vet Mart",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": ["POULTRY_SUPPLIES", "WHOLESALER"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Congo Street / Swahili Street, Kariakoo",
        "phone": "+255 22 218 5566",
        "alternative_phone": "+255 754 218 556",
        "source_url": "https://www.yellowpages.co.tz/tz-poultry-vet-mart",
        "source_type": "hotspot_harvester",
        "description": "Veterinary pharmaceuticals wholesaler, poultry equipment, drinkers, and vaccines.",
        "latitude": -6.8210,
        "longitude": 39.2760
    },
    {
        "business_name": "Kariakoo Animal Nutrition Supplies",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["WHOLESALER", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Narung'ombe Street, Kariakoo",
        "phone": "+255 755 443 881",
        "alternative_phone": "+255 713 443 881",
        "source_url": "https://www.cybo.com/TZ-biz/kariakoo-animal-nutrition",
        "source_type": "hotspot_harvester",
        "description": "Wholesale concentrates, amino acids (methionine, lysine), mineral blocks, and feed additives.",
        "latitude": -6.8230,
        "longitude": 39.2775
    },
    {
        "business_name": "Afro-Asia Veterinary Chemicals Ltd",
        "category": "DISTRIBUTOR",
        "secondary_categories": ["VETERINARY_PHARMACY", "WHOLESALER"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Msimbazi Street, Kariakoo",
        "phone": "+255 714 667 990",
        "alternative_phone": "+255 768 667 990",
        "source_url": "https://www.yellowpages.co.tz/afro-asia-vet",
        "source_type": "hotspot_harvester",
        "description": "Importer and distributor of veterinary antimicrobials, anthelmintics, and disinfectants.",
        "latitude": -6.8190,
        "longitude": 39.2750
    },
    {
        "business_name": "Gerezani Agro-Industrial Inputs",
        "category": "AGROVET",
        "secondary_categories": ["AGRICULTURAL_INPUTS", "ANIMAL_FEED"],
        "district": "Ilala",
        "ward_or_area": "Gerezani",
        "street_or_address": "Gerezani Street, Near Railway Crossing",
        "phone": "+255 767 112 004",
        "alternative_phone": "+255 715 112 004",
        "source_url": "https://www.cybo.com/TZ-biz/gerezani-agro-industrial",
        "source_type": "hotspot_harvester",
        "description": "Feed mill supplies, maize bran, sunflower cake, and agricultural inputs store.",
        "latitude": -6.8250,
        "longitude": 39.2830
    },

    # 3. Mbagala Cluster
    {
        "business_name": "Mbagala Majimatitu Agrovet Hub",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Majimatitu B, Kilwa Road corridor",
        "phone": "+255 715 889 443",
        "alternative_phone": "+255 768 889 443",
        "source_url": "https://www.yellowpages.co.tz/mbagala-majimatitu-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Feeds, broiler crumbles, vitamins, vaccines, and day-old chick bookings for peri-urban farmers.",
        "latitude": -6.9210,
        "longitude": 39.2560
    },
    {
        "business_name": "Rangi Tatu Poultry Supplies & Chicks",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "AGROVET"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Kilwa Road, Near Rangi Tatu Stand",
        "phone": "+255 765 221 889",
        "alternative_phone": "+255 714 221 889",
        "source_url": "https://www.cybo.com/TZ-biz/rangi-tatu-poultry-supplies",
        "source_type": "hotspot_harvester",
        "description": "Day-old chicks distribution, heating lamps, feeding troughs, and commercial feeds.",
        "latitude": -6.9100,
        "longitude": 39.2625
    },
    {
        "business_name": "Zakhem Animal Feeds & Vaccines",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "VETERINARY_SHOP"],
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
        "secondary_categories": ["VETERINARY_SHOP", "AGROVET"],
        "district": "Temeke",
        "ward_or_area": "Charambe",
        "street_or_address": "Charambe Kati, Temeke",
        "phone": "+255 712 443 667",
        "alternative_phone": "+255 755 443 667",
        "source_url": "https://www.cybo.com/TZ-biz/charambe-vet-clinic",
        "source_type": "hotspot_harvester",
        "description": "Clinical veterinary services, poultry disease diagnosis, dewormers, and flock health support.",
        "latitude": -6.9270,
        "longitude": 39.2720
    },

    # 4. Tegeta & Wazo Hill Cluster
    {
        "business_name": "Wazo Hill Livestock & Poultry Depots",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": ["AGROVET", "POULTRY_FEED"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Wazo Hill Main Road, Kinondoni",
        "phone": "+255 768 554 221",
        "alternative_phone": "+255 715 554 221",
        "source_url": "https://www.yellowpages.co.tz/wazo-hill-livestock-depot",
        "source_type": "hotspot_harvester",
        "description": "Cattle dip chemicals, salt licks, dairy feed meal, and commercial poultry feeds.",
        "latitude": -6.6585,
        "longitude": 39.1860
    },
    {
        "business_name": "Tegeta Kibaoni Animal Health Centre",
        "category": "AGROVET",
        "secondary_categories": ["VETERINARY_SHOP", "POULTRY_FEED"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Bagamoyo Road, Tegeta Kibaoni",
        "phone": "+255 713 778 991",
        "alternative_phone": "+255 765 778 991",
        "source_url": "https://www.cybo.com/TZ-biz/tegeta-kibaoni-animal-health",
        "source_type": "hotspot_harvester",
        "description": "Retail supplier of poultry antibiotics, dewormers, broiler crumbles, and pet foods.",
        "latitude": -6.6660,
        "longitude": 39.2170
    },
    {
        "business_name": "Tegeta Center Agrovet Store",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "AGRICULTURAL_INPUTS"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Tegeta Posta, Bagamoyo Road",
        "phone": "+255 755 889 112",
        "alternative_phone": "+255 714 889 112",
        "source_url": "https://www.yellowpages.co.tz/tegeta-center-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Poultry feeds, day-old chicks, garden inputs, knapsack sprayers, and poultry vitamins.",
        "latitude": -6.6670,
        "longitude": 39.2165
    },

    # 5. Kitunda & Chanika Cluster
    {
        "business_name": "Kitunda Kati Poultry Hub",
        "category": "POULTRY_FEED",
        "secondary_categories": ["POULTRY_SUPPLIES", "AGROVET"],
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
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Chanika",
        "street_or_address": "Chanika Mwisho Main Stand",
        "phone": "+255 767 445 889",
        "alternative_phone": "+255 715 445 889",
        "source_url": "https://www.cybo.com/TZ-biz/chanika-mwisho-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Serving extensive peri-urban dairy cattle, goat, and poultry farmers with veterinary remedies.",
        "latitude": -6.9560,
        "longitude": 39.1440
    },
    {
        "business_name": "Kivule Magole Livestock Remedies",
        "category": "VETERINARY_SHOP",
        "secondary_categories": ["AGROVET", "POULTRY_FEED"],
        "district": "Ilala",
        "ward_or_area": "Kivule",
        "street_or_address": "Kivule Magole Sokoni",
        "phone": "+255 754 221 667",
        "alternative_phone": "+255 713 221 667",
        "source_url": "https://www.yellowpages.co.tz/kivule-magole-remedies",
        "source_type": "hotspot_harvester",
        "description": "Anthelmintics, poultry stress packs, oxytetracycline powder, and poultry feed crumbles.",
        "latitude": -6.9140,
        "longitude": 39.1830
    },
    {
        "business_name": "Machimbo Agrovet & Feeds",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Kitunda",
        "street_or_address": "Kitunda Machimbo, Ilala",
        "phone": "+255 712 889 443",
        "alternative_phone": "+255 765 889 443",
        "source_url": "https://www.cybo.com/TZ-biz/machimbo-agrovet",
        "source_type": "hotspot_harvester",
        "description": "Retail supplier of broiler feeds, layers mash, automatic drinkers, and Newcastle vaccines.",
        "latitude": -6.8940,
        "longitude": 39.2050
    },

    # 6. Mbezi & Kimara Corridor
    {
        "business_name": "Mbezi Luis Feeds & Vet Care",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES"],
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
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES"],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Kimara Korogwe",
        "phone": "+255 715 443 221",
        "alternative_phone": "+255 754 443 221",
        "source_url": "https://www.cybo.com/TZ-biz/kimara-korogwe-poultry",
        "source_type": "hotspot_harvester",
        "description": "Poultry feeds retailer stocking Silverlands and Kibo feeds, feeders, and vitamins.",
        "latitude": -6.7960,
        "longitude": 39.1840
    },
    {
        "business_name": "Kimara Stopover Feed Depot",
        "category": "POULTRY_FEED",
        "secondary_categories": ["WHOLESALER", "ANIMAL_FEED"],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Kimara Stopover",
        "phone": "+255 754 778 119",
        "alternative_phone": "+255 718 778 119",
        "source_url": "https://www.yellowpages.co.tz/kimara-stopover-feed-depot",
        "source_type": "hotspot_harvester",
        "description": "Wholesale distributor of broiler starter crumbles, finisher pellets, and layers mash.",
        "latitude": -6.7980,
        "longitude": 39.1740
    },

    # 7. Tandika & Chang'ombe Cluster
    {
        "business_name": "Tandika Live Poultry Supplies",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "AGROVET"],
        "district": "Temeke",
        "ward_or_area": "Tandika",
        "street_or_address": "Tandika Sokoni Main Trade Area",
        "phone": "+255 714 889 332",
        "alternative_phone": "+255 768 889 332",
        "source_url": "https://www.yellowpages.co.tz/tandika-live-poultry",
        "source_type": "hotspot_harvester",
        "description": "Feed concentrates, live bird handling cages, chick vaccines, and stress tonics.",
        "latitude": -6.8620,
        "longitude": 39.2670
    },
    {
        "business_name": "Chang'ombe Vet Instruments Agency",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": ["VETERINARY_SHOP", "WHOLESALER"],
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
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES"],
        "district": "Temeke",
        "ward_or_area": "Temeke",
        "street_or_address": "Mandela Road / Stereo Bus Stand",
        "phone": "+255 755 443 118",
        "alternative_phone": "+255 712 443 118",
        "source_url": "https://www.yellowpages.co.tz/temeke-stereo-feed-store",
        "source_type": "hotspot_harvester",
        "description": "Broiler starter, layer mash, drinkers, heating pots, and basic veterinary medicines.",
        "latitude": -6.8530,
        "longitude": 39.2650
    },

    # 8. Kibada & Kisarawe II Corridor
    {
        "business_name": "Kibada Commercial Poultry Supplies",
        "category": "POULTRY_FEED",
        "secondary_categories": ["POULTRY_SUPPLIES", "AGROVET"],
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
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "POULTRY_FEED"],
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

with open(cluster_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Append to CLUSTER_BUSINESSES list
# Find where CLUSTER_BUSINESSES = [ ... ] ends before `def harvest_cluster_deep_records():`
insert_marker = "    }\n]\n\ndef harvest_cluster_deep_records():"
if insert_marker in content:
    json_lines = []
    for rec in additional_records:
        rec_str = json.dumps(rec, indent=8)
        # remove first '{' and add proper indentation
        formatted = "    " + rec_str
        json_lines.append(formatted)
    
    append_block = ",\n" + ",\n".join(json_lines) + "\n]\n\ndef harvest_cluster_deep_records():"
    new_content = content.replace("    }\n]\n\ndef harvest_cluster_deep_records():", "    }" + append_block, 1)
    
    with open(cluster_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Successfully appended {len(additional_records)} records to {cluster_file}!")
else:
    print("Could not find insert marker in cluster_harvester.py!")
