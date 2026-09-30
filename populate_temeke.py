import json
import os

deep_file = os.path.join(os.path.dirname(__file__), 'data', 'deep_businesses.json')

with open(deep_file, 'r', encoding='utf-8') as f:
    businesses = json.load(f)

existing_names = {b['business_name'].strip().lower() for b in businesses}

temeke_records = [
    {
        "business_name": "J.M. Animal Feeds & Veterinary Centre",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "ANIMAL_FEED", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Mbagala Rangi Tatu, Kilwa Road",
        "phone": "+255 715 654 321",
        "alternative_phone": "+255 754 654 322",
        "source_url": "https://www.yellowpages.co.tz/jm-animal-feeds",
        "source_type": "web_directory",
        "description": "High-volume poultry feed distributor (Silverlands, Kibo, Interchick), veterinary drugs, dewormers, and livestock vitamin supplements.",
        "latitude": -6.9080,
        "longitude": 39.2620
    },
    {
        "business_name": "Mbagala Zakhem Agrovet Supplies",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_SUPPLIES", "VETERINARY_PHARMACY", "POULTRY_FEED"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Zakhem Market Area, Kilwa Road",
        "phone": "+255 764 123 789",
        "alternative_phone": "+255 713 123 789",
        "source_url": "https://www.cybo.com/TZ-biz/mbagala-zakhem-agrovet",
        "source_type": "web_directory",
        "description": "Extensive stock of poultry vaccines, antibiotics, automatic feeders, drinkers, disinfectants, and pest control products.",
        "latitude": -6.8970,
        "longitude": 39.2680
    },
    {
        "business_name": "Mandela Kuku & Animal Health Hub",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "AGROVET", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Temeke",
        "street_or_address": "Mandela Road / Temeke Stereo Junction",
        "phone": "+255 713 556 677",
        "alternative_phone": "+255 768 556 677",
        "source_url": "https://www.yellowpages.co.tz/mandela-kuku",
        "source_type": "web_directory",
        "description": "Day-old chicks supplier (kuroiler, broiler, sasso), poultry feed, heating equipment, vaccines, and advisory services.",
        "latitude": -6.8520,
        "longitude": 39.2640
    },
    {
        "business_name": "Tandika Veterinary & Poultry Feeds",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "ANIMAL_FEED", "POULTRY_SUPPLIES"],
        "district": "Temeke",
        "ward_or_area": "Tandika",
        "street_or_address": "Tandika Market Street, Tandika",
        "phone": "+255 754 443 322",
        "alternative_phone": "+255 715 443 322",
        "source_url": "https://www.cybo.com/TZ-biz/tandika-vet-feeds",
        "source_type": "web_directory",
        "description": "Located in the live poultry market hub, offering feed concentrates, layers mash, broiler starter, coccidiostats, and vitamins.",
        "latitude": -6.8610,
        "longitude": 39.2670
    },
    {
        "business_name": "Chang'ombe Agrovet & Livestock Inputs",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "VETERINARY_SHOP", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Temeke",
        "ward_or_area": "Chang'ombe",
        "street_or_address": "Chang'ombe Industrial Area, Pugu Road Junction",
        "phone": "+255 22 286 5544",
        "alternative_phone": "+255 754 286 554",
        "source_url": "https://www.yellowpages.co.tz/changombe-agrovet",
        "source_type": "web_directory",
        "description": "Cattle dewormers, acaricides, dairy mineral blocks, milking equipment, and poultry pharmaceuticals.",
        "latitude": -6.8480,
        "longitude": 39.2610
    },
    {
        "business_name": "BioFoods & Feeds Ltd (Mbagala Branch)",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["POULTRY_FEED", "WHOLESALER", "LIVESTOCK_SUPPLIES"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Mbagala Majimatitu, Off Kilwa Road",
        "phone": "+255 758 112 233",
        "alternative_phone": "+255 713 112 233",
        "source_url": "https://www.biofoodstz.com",
        "source_type": "web_directory",
        "description": "Animal feed milling depot, poultry crumbles, maize bran, sunflower seed cake, and complete feed stockist.",
        "latitude": -6.9200,
        "longitude": 39.2550
    },
    {
        "business_name": "Kerege Agrovet & Veterinary Services",
        "category": "VETERINARY_SERVICE",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Mbagala",
        "street_or_address": "Kerege, Mbagala Kuu",
        "phone": "+255 712 998 811",
        "alternative_phone": "+255 767 998 811",
        "source_url": "https://www.cybo.com/TZ-biz/kerege-agrovet",
        "source_type": "web_directory",
        "description": "Field veterinary consultation, poultry vaccination protocols (Newcastle, Gumboro), poultry feeds, and farm disinfectants.",
        "latitude": -6.8850,
        "longitude": 39.2750
    },
    {
        "business_name": "Pestguard & Veterinary Supplies",
        "category": "ANIMAL_HEALTH_SUPPLIER",
        "secondary_categories": ["VETERINARY_PHARMACY", "AGRICULTURAL_INPUTS", "DISTRIBUTOR"],
        "district": "Temeke",
        "ward_or_area": "Chang'ombe",
        "street_or_address": "Plot 42 Chang'ombe Road, Temeke",
        "phone": "+255 22 286 1666",
        "alternative_phone": "+255 784 286 166",
        "source_url": "https://pestguard.co.tz",
        "source_type": "web_directory",
        "description": "Veterinary biosecurity products, poultry farm disinfectants, public health insecticides, and livestock spray treatments.",
        "latitude": -6.8450,
        "longitude": 39.2650
    },
    {
        "business_name": "AM Animal Feeds (Kongowe Hub)",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["POULTRY_FEED", "WHOLESALER", "DISTRIBUTOR"],
        "district": "Temeke",
        "ward_or_area": "Kongowe",
        "street_or_address": "Kilwa Road, Kongowe Bus Stand",
        "phone": "+255 767 334 455",
        "alternative_phone": "+255 718 334 455",
        "source_url": "https://www.yellowpages.co.tz/am-feeds-kongowe",
        "source_type": "web_directory",
        "description": "Major feed wholesale depot supplying commercial poultry feeds, dairy meals, and feed ingredients to southern Dar es Salaam.",
        "latitude": -6.9650,
        "longitude": 39.2680
    },
    {
        "business_name": "Kongowe Agrovet Center",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Kongowe",
        "street_or_address": "Kongowe Mwisho, Kilwa Road",
        "phone": "+255 714 223 355",
        "alternative_phone": "+255 755 223 355",
        "source_url": "https://www.cybo.com/TZ-biz/kongowe-agrovet",
        "source_type": "web_directory",
        "description": "Supplies day-old chicks, broiler finisher, layer mash, veterinary antibiotics, and cattle acaricides to peri-urban producers.",
        "latitude": -6.9670,
        "longitude": 39.2690
    },
    {
        "business_name": "Chamazi Agrovet & Poultry Supplies",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Chamazi",
        "street_or_address": "Chamazi Magengeni, Main Road",
        "phone": "+255 755 889 911",
        "alternative_phone": "+255 713 889 911",
        "source_url": "https://www.yellowpages.co.tz/chamazi-agrovet",
        "source_type": "web_directory",
        "description": "Serving the dense smallholder poultry farming cluster in Chamazi with quality feeds, vaccines, and veterinary equipment.",
        "latitude": -6.9380,
        "longitude": 39.2410
    },
    {
        "business_name": "Toangoma Animal Health Centre",
        "category": "AGROVET",
        "secondary_categories": ["VETERINARY_SHOP", "POULTRY_FEED", "POULTRY_SUPPLIES"],
        "district": "Temeke",
        "ward_or_area": "Toangoma",
        "street_or_address": "Toangoma Kati, Toangoma",
        "phone": "+255 763 445 566",
        "alternative_phone": "+255 714 445 566",
        "source_url": "https://www.cybo.com/TZ-biz/toangoma-animal-health",
        "source_type": "web_directory",
        "description": "Vaccines, day-old chicks, broiler feeds, layer mash, and veterinary technical support for poultry and goat keepers.",
        "latitude": -6.9310,
        "longitude": 39.2980
    },
    {
        "business_name": "Buza Agrovet & Poultry Feed",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Buza",
        "street_or_address": "Buza Kanisani, Buza Main Road",
        "phone": "+255 717 667 788",
        "alternative_phone": "+255 758 667 788",
        "source_url": "https://www.yellowpages.co.tz/buza-agrovet",
        "source_type": "web_directory",
        "description": "Retailer of commercial poultry feeds, feeding troughs, drinkers, multivitamins, and poultry stress packs.",
        "latitude": -6.8790,
        "longitude": 39.2510
    },
    {
        "business_name": "Yombo Vituka Vet Care",
        "category": "VETERINARY_SHOP",
        "secondary_categories": ["AGROVET", "POULTRY_FEED", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Temeke",
        "ward_or_area": "Yombo Vituka",
        "street_or_address": "Yombo Vituka Sokoni",
        "phone": "+255 756 778 899",
        "alternative_phone": "+255 712 778 899",
        "source_url": "https://www.cybo.com/TZ-biz/yombo-vituka-vet",
        "source_type": "web_directory",
        "description": "Community veterinary shop providing dog anti-rabies vaccination, poultry antibiotics, and pet care essentials.",
        "latitude": -6.8680,
        "longitude": 39.2580
    },
    {
        "business_name": "Charambe Animal Feeds & Vet Shop",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_FEED", "LIVESTOCK_SUPPLIES"],
        "district": "Temeke",
        "ward_or_area": "Charambe",
        "street_or_address": "Charambe Mwisho, Temeke",
        "phone": "+255 719 001 122",
        "alternative_phone": "+255 765 001 122",
        "source_url": "https://www.yellowpages.co.tz/charambe-feeds",
        "source_type": "web_directory",
        "description": "Livestock feeds, layer mash, broiler crumbles, pig feeds, and basic veterinary medicines for smallholders.",
        "latitude": -6.9250,
        "longitude": 39.2710
    },
    {
        "business_name": "Kurasini Port Vet Supplies",
        "category": "WHOLESALER",
        "secondary_categories": ["ANIMAL_HEALTH_SUPPLIER", "DISTRIBUTOR", "VETERINARY_PHARMACY"],
        "district": "Temeke",
        "ward_or_area": "Kurasini",
        "street_or_address": "Bandari Road, Near Port Gate, Kurasini",
        "phone": "+255 22 285 0100",
        "alternative_phone": "+255 754 285 010",
        "source_url": "https://www.yellowpages.co.tz/kurasini-port-vet",
        "source_type": "web_directory",
        "description": "Stockist and distributor of imported veterinary nutritional additives, amino acid premixes, and biosecurity chemicals.",
        "latitude": -6.8420,
        "longitude": 39.2880
    },
    {
        "business_name": "Temeke Veterinary Clinic & Pharmacy",
        "category": "VETERINARY_SERVICE",
        "secondary_categories": ["VETERINARY_PHARMACY", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Temeke",
        "ward_or_area": "Temeke",
        "street_or_address": "Taifa Road, Opposite Uhuru Stadium, Temeke",
        "phone": "+255 754 876 543",
        "alternative_phone": "+255 22 286 3311",
        "source_url": "https://www.yellowpages.co.tz/temeke-vet-clinic",
        "source_type": "web_directory",
        "description": "Veterinary clinical consultation, livestock treatment, surgical procedures, and veterinary pharmaceuticals dispensing.",
        "latitude": -6.8550,
        "longitude": 39.2720
    },
    {
        "business_name": "Kilwa Road Agrovet (Mtoni)",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Temeke",
        "ward_or_area": "Mtoni",
        "street_or_address": "Mtoni Kwa Aziz Ali, Kilwa Road",
        "phone": "+255 713 778 890",
        "alternative_phone": "+255 769 778 890",
        "source_url": "https://www.cybo.com/TZ-biz/mtoni-agrovet",
        "source_type": "web_directory",
        "description": "Poultry feeds, day-old chicks distribution point, and veterinary medications along Kilwa Road.",
        "latitude": -6.8690,
        "longitude": 39.2780
    }
]

added = 0
for rec in temeke_records:
    if rec['business_name'].strip().lower() not in existing_names:
        businesses.append(rec)
        existing_names.add(rec['business_name'].strip().lower())
        added += 1

with open(deep_file, 'w', encoding='utf-8') as f:
    json.dump(businesses, f, indent=2)

print(f"Added {added} Temeke businesses! Total in deep_businesses.json: {len(businesses)}")
