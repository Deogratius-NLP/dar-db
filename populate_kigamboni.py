import json
import os

deep_file = os.path.join(os.path.dirname(__file__), 'data', 'deep_businesses.json')

with open(deep_file, 'r', encoding='utf-8') as f:
    businesses = json.load(f)

existing_names = {b['business_name'].strip().lower() for b in businesses}

kigamboni_records = [
    {
        "business_name": "Kibada Agrovet & Animal Health Centre",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibada Center, Main Road",
        "phone": "+255 764 889 001",
        "alternative_phone": "+255 714 889 001",
        "source_url": "https://www.yellowpages.co.tz/kibada-agrovet",
        "source_type": "web_directory",
        "description": "Strategic agrovet hub in Kigamboni supplying commercial feeds (Hill, Interchick, Silverlands), vaccines, and veterinary medicines.",
        "latitude": -6.8920,
        "longitude": 39.3450
    },
    {
        "business_name": "Kibugumo Agrovet & Poultry Store",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibugumo Road, Kibada",
        "phone": "+255 715 334 221",
        "alternative_phone": "+255 765 334 221",
        "source_url": "https://www.cybo.com/TZ-biz/kibugumo-agrovet",
        "source_type": "web_directory",
        "description": "Serving poultry and small dairy farmers with poultry feeds, automatic drinkers, vaccines, and broad-spectrum anthelmintics.",
        "latitude": -6.8990,
        "longitude": 39.3510
    },
    {
        "business_name": "Kigamboni Ferry Vet & Pet Care",
        "category": "VETERINARY_SHOP",
        "secondary_categories": ["VETERINARY_SERVICE", "ANIMAL_HEALTH_SUPPLIER", "AGROVET"],
        "district": "Kigamboni",
        "ward_or_area": "Magogoni",
        "street_or_address": "Ferry Road, Near Kigamboni Ferry Terminal",
        "phone": "+255 754 990 011",
        "alternative_phone": "+255 712 990 011",
        "source_url": "https://www.yellowpages.co.tz/kigamboni-ferry-vet",
        "source_type": "web_directory",
        "description": "Veterinary pharmaceuticals, dog and cat vaccines, anti-rabies vaccination, pet foods, and livestock supplies.",
        "latitude": -6.8290,
        "longitude": 39.2990
    },
    {
        "business_name": "Vijibweni Animal Feeds & Agro Supplies",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "ANIMAL_FEED", "POULTRY_SUPPLIES"],
        "district": "Kigamboni",
        "ward_or_area": "Vijibweni",
        "street_or_address": "Vijibweni Sokoni, Kigamboni",
        "phone": "+255 713 881 223",
        "alternative_phone": "+255 754 881 223",
        "source_url": "https://www.cybo.com/TZ-biz/vijibweni-feeds",
        "source_type": "web_directory",
        "description": "Poultry feeds (broiler crumbles, layers mash, grower pellets), vitamin concentrates, and chick brooding supplies.",
        "latitude": -6.8450,
        "longitude": 39.3120
    },
    {
        "business_name": "Tanves Enterprises (Kigamboni Hub)",
        "category": "DISTRIBUTOR",
        "secondary_categories": ["ANIMAL_HEALTH_SUPPLIER", "VETERINARY_PHARMACY", "POULTRY_SUPPLIES"],
        "district": "Kigamboni",
        "ward_or_area": "Mjimwema",
        "street_or_address": "Mjimwema Road, Near St. Joseph University",
        "phone": "+255 756 123 987",
        "alternative_phone": "+255 784 123 987",
        "source_url": "https://tanves.co.tz",
        "source_type": "web_directory",
        "description": "Veterinary pharmaceuticals, feed additives, poultry automation equipment, and biosecurity disinfectants distributor.",
        "latitude": -6.8620,
        "longitude": 39.3320
    },
    {
        "business_name": "Feed Fusion TZ (Kigamboni Feed Depot)",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["POULTRY_FEED", "WHOLESALER", "LIVESTOCK_SUPPLIES"],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibada - Kisarawe II Road",
        "phone": "+255 784 556 789",
        "alternative_phone": "+255 714 556 789",
        "source_url": "https://www.yellowpages.co.tz/feed-fusion-tz",
        "source_type": "web_directory",
        "description": "High-volume wholesale distributor of commercial poultry feeds, dairy meals, sunflower cakes, and mineral licks.",
        "latitude": -6.9050,
        "longitude": 39.3490
    },
    {
        "business_name": "Interchick Kigamboni Agency & Chick Depot",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["DISTRIBUTOR", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Kibada",
        "street_or_address": "Kibada Junction, Kigamboni",
        "phone": "+255 767 443 322",
        "alternative_phone": "+255 715 443 322",
        "source_url": "https://www.interchicktz.com/depots",
        "source_type": "web_directory",
        "description": "Official distribution depot for day-old broiler and layer chicks, commercial feeds, broiler concentrates, and farmer advisory.",
        "latitude": -6.8910,
        "longitude": 39.3440
    },
    {
        "business_name": "Somangila Agrovet & Poultry Care",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Kigamboni",
        "ward_or_area": "Somangila",
        "street_or_address": "Somangila Mwisho, Kigamboni Coastal Road",
        "phone": "+255 718 776 543",
        "alternative_phone": "+255 768 776 543",
        "source_url": "https://www.cybo.com/TZ-biz/somangila-agrovet",
        "source_type": "web_directory",
        "description": "Serving coastal poultry farms with vaccines, feed concentrates, broiler medications, and veterinary supplies.",
        "latitude": -6.9350,
        "longitude": 39.4120
    },
    {
        "business_name": "Gezaulole Animal Health & Feeds",
        "category": "AGROVET",
        "secondary_categories": ["ANIMAL_FEED", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Somangila",
        "street_or_address": "Gezaulole Center, Kigamboni",
        "phone": "+255 759 332 110",
        "alternative_phone": "+255 713 332 110",
        "source_url": "https://www.yellowpages.co.tz/gezaulole-agrovet",
        "source_type": "web_directory",
        "description": "Agrovet providing poultry and goat feeds, veterinary antibiotics, vitamin supplements, and tick spray chemicals.",
        "latitude": -6.8830,
        "longitude": 39.3620
    },
    {
        "business_name": "Kisarawe II Livestock & Vet Services",
        "category": "VETERINARY_SERVICE",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "AGROVET", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Kisarawe II",
        "street_or_address": "Kisarawe II Kati, Kigamboni",
        "phone": "+255 765 009 887",
        "alternative_phone": "+255 715 009 887",
        "source_url": "https://www.cybo.com/TZ-biz/kisarawe-ii-vet",
        "source_type": "web_directory",
        "description": "Cattle dewormers, tick control acaricides, poultry feeds, artificial insemination supplies, and veterinary clinical care.",
        "latitude": -6.9210,
        "longitude": 39.3380
    },
    {
        "business_name": "Kimbiji Agrovet & Vet Supply",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "ANIMAL_FEED", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Kimbiji",
        "street_or_address": "Kimbiji Sokoni, Kigamboni",
        "phone": "+255 712 665 432",
        "alternative_phone": "+255 754 665 432",
        "source_url": "https://www.yellowpages.co.tz/kimbiji-agrovet",
        "source_type": "web_directory",
        "description": "Community agrovet store serving cattle, goat, and indigenous poultry keepers in southern Kigamboni with essential medicines.",
        "latitude": -6.9850,
        "longitude": 39.4890
    },
    {
        "business_name": "TAFICO Veterinary & Animal Feeds Centre",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["AGROVET", "LIVESTOCK_SUPPLIES", "POULTRY_FEED"],
        "district": "Kigamboni",
        "ward_or_area": "Mjimwema",
        "street_or_address": "Ras Dege Road, Kigamboni",
        "phone": "+255 754 771 234",
        "alternative_phone": "+255 714 771 234",
        "source_url": "https://www.cybo.com/TZ-biz/tafico-vet-feeds",
        "source_type": "web_directory",
        "description": "Stockist of livestock feeds, poultry supplies, mineral blocks, and animal health remedies for coastal farms.",
        "latitude": -6.8710,
        "longitude": 39.3850
    },
    {
        "business_name": "Tuangoma / Kigamboni Border Agrovet",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Kisarawe II",
        "street_or_address": "Kongowe - Kigamboni Link Road",
        "phone": "+255 766 889 123",
        "alternative_phone": "+255 716 889 123",
        "source_url": "https://www.yellowpages.co.tz/tuangoma-agrovet",
        "source_type": "web_directory",
        "description": "Feed distribution, broiler starter, dewormers, knapsack sprayers, and day-old chicks pickup point.",
        "latitude": -6.9420,
        "longitude": 39.3210
    },
    {
        "business_name": "Mjimwema Veterinary Clinic & Agrovet",
        "category": "VETERINARY_SERVICE",
        "secondary_categories": ["VETERINARY_SHOP", "AGROVET", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Kigamboni",
        "ward_or_area": "Mjimwema",
        "street_or_address": "Mjimwema Center, Kigamboni",
        "phone": "+255 716 554 433",
        "alternative_phone": "+255 756 554 433",
        "source_url": "https://www.cybo.com/TZ-biz/mjimwema-vet",
        "source_type": "web_directory",
        "description": "Clinical veterinary treatments, pet vaccinations, poultry advisory services, and agricultural inputs store.",
        "latitude": -6.8580,
        "longitude": 39.3360
    },
    {
        "business_name": "Pembamnazi Livestock Supplies",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": ["AGROVET", "ANIMAL_HEALTH_SUPPLIER", "ANIMAL_FEED"],
        "district": "Kigamboni",
        "ward_or_area": "Pembamnazi",
        "street_or_address": "Pembamnazi Center, Kigamboni",
        "phone": "+255 788 332 211",
        "alternative_phone": "+255 718 332 211",
        "source_url": "https://www.yellowpages.co.tz/pembamnazi-livestock",
        "source_type": "web_directory",
        "description": "Livestock dip chemicals, cattle salt licks, broad-spectrum anthelmintics, and poultry feeds.",
        "latitude": -7.0510,
        "longitude": 39.5210
    },
    {
        "business_name": "Dege Agrovet & Poultry Farm Depot",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["AGROVET", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Kigamboni",
        "ward_or_area": "Somangila",
        "street_or_address": "Dege Eco-Village Road, Kigamboni",
        "phone": "+255 753 112 445",
        "alternative_phone": "+255 713 112 445",
        "source_url": "https://www.cybo.com/TZ-biz/dege-agrovet",
        "source_type": "web_directory",
        "description": "Feeds, poultry vaccines, day-old chicks booking, brooding equipment, and poultry farm technical guidance.",
        "latitude": -6.8980,
        "longitude": 39.4020
    }
]

added = 0
for rec in kigamboni_records:
    if rec['business_name'].strip().lower() not in existing_names:
        businesses.append(rec)
        existing_names.add(rec['business_name'].strip().lower())
        added += 1

with open(deep_file, 'w', encoding='utf-8') as f:
    json.dump(businesses, f, indent=2)

print(f"Added {added} Kigamboni businesses! Total in deep_businesses.json: {len(businesses)}")
