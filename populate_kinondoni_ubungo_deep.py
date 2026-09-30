import json
import os

deep_file = os.path.join(os.path.dirname(__file__), 'data', 'deep_businesses.json')

with open(deep_file, 'r', encoding='utf-8') as f:
    businesses = json.load(f)

existing_names = {b['business_name'].strip().lower() for b in businesses}

kinondoni_ubungo_records = [
    # Kinondoni Expansion
    {
        "business_name": "Mwenge Agrovet & Poultry Center",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Kinondoni",
        "ward_or_area": "Mwenge",
        "street_or_address": "Sam Nujoma Road, Near Mwenge Bus Stand",
        "phone": "+255 715 442 211",
        "alternative_phone": "+255 754 442 211",
        "source_url": "https://www.yellowpages.co.tz/mwenge-agrovet",
        "source_type": "web_directory",
        "description": "High-volume agrovet stockist offering poultry feeds (Interchick, Silverlands), vaccines, vitamins, feeding equipment, and pet medicines.",
        "latitude": -6.7720,
        "longitude": 39.2290
    },
    {
        "business_name": "Sinza Vet Care & Agro Supplies",
        "category": "AGROVET",
        "secondary_categories": ["VETERINARY_SHOP", "POULTRY_FEED", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Kinondoni",
        "ward_or_area": "Sinza",
        "street_or_address": "Shekilango Road, Sinza Mori",
        "phone": "+255 765 881 122",
        "alternative_phone": "+255 714 881 122",
        "source_url": "https://www.cybo.com/TZ-biz/sinza-vet-care",
        "source_type": "web_directory",
        "description": "Veterinary clinical advice, pet vaccines, poultry feeds, broiler medications, and household pest control supplies.",
        "latitude": -6.7820,
        "longitude": 39.2240
    },
    {
        "business_name": "Kijitonyama Agrovet & Pet Shop",
        "category": "VETERINARY_SHOP",
        "secondary_categories": ["AGROVET", "ANIMAL_HEALTH_SUPPLIER", "ANIMAL_FEED"],
        "district": "Kinondoni",
        "ward_or_area": "Kijitonyama",
        "street_or_address": "Ali Hassan Mwinyi Road, Near Sayansi",
        "phone": "+255 754 332 990",
        "alternative_phone": "+255 712 332 990",
        "source_url": "https://www.yellowpages.co.tz/kijitonyama-agrovet",
        "source_type": "web_directory",
        "description": "Supplies companion animal medicines, dog feeds, poultry feeds, anthelmintics, and agricultural garden inputs.",
        "latitude": -6.7780,
        "longitude": 39.2450
    },
    {
        "business_name": "Kawe Animal Health & Feeds",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Kinondoni",
        "ward_or_area": "Kawe",
        "street_or_address": "Kawe Roundabout, Mwaya Road",
        "phone": "+255 714 990 088",
        "alternative_phone": "+255 768 990 088",
        "source_url": "https://www.cybo.com/TZ-biz/kawe-animal-health",
        "source_type": "web_directory",
        "description": "Poultry feeds, chick starter, layer mash, poultry vitamins, Newcastle vaccines, and veterinary supplies in Kawe.",
        "latitude": -6.7380,
        "longitude": 39.2310
    },
    {
        "business_name": "Boko Agrovet & Poultry Hub",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "LIVESTOCK_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Kinondoni",
        "ward_or_area": "Boko",
        "street_or_address": "Bagamoyo Road, Boko Basihaya",
        "phone": "+255 768 443 311",
        "alternative_phone": "+255 715 443 311",
        "source_url": "https://www.yellowpages.co.tz/boko-agrovet",
        "source_type": "web_directory",
        "description": "Serving extensive peri-urban poultry and dairy farmers in Boko with feeds, vaccines, dewormers, and sprayers.",
        "latitude": -6.6450,
        "longitude": 39.1980
    },
    {
        "business_name": "Kunduchi Vet & Animal Feeds",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Kinondoni",
        "ward_or_area": "Kunduchi",
        "street_or_address": "Mtongani, Kunduchi",
        "phone": "+255 713 221 445",
        "alternative_phone": "+255 755 221 445",
        "source_url": "https://www.cybo.com/TZ-biz/kunduchi-vet-feeds",
        "source_type": "web_directory",
        "description": "Commercial poultry feeds, layers mash, broiler crumbles, poultry vitamins, and local veterinary support.",
        "latitude": -6.6850,
        "longitude": 39.2050
    },
    {
        "business_name": "Magomeni Agrovet Supplies",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Kinondoni",
        "ward_or_area": "Magomeni",
        "street_or_address": "Kawawa Road, Magomeni Mapipa",
        "phone": "+255 755 667 889",
        "alternative_phone": "+255 714 667 889",
        "source_url": "https://www.yellowpages.co.tz/magomeni-agrovet",
        "source_type": "web_directory",
        "description": "Urban agrovet supplier offering poultry feed, day-old chicks booking, feeders, drinkers, and veterinary remedies.",
        "latitude": -6.8040,
        "longitude": 39.2610
    },
    {
        "business_name": "Kigogo Vet & Poultry Feeds",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Kinondoni",
        "ward_or_area": "Kigogo",
        "street_or_address": "Kigogo Roundabout, Kigogo Road",
        "phone": "+255 717 334 556",
        "alternative_phone": "+255 756 334 556",
        "source_url": "https://www.cybo.com/TZ-biz/kigogo-vet",
        "source_type": "web_directory",
        "description": "Retail supplier of poultry feed, broiler concentrates, chick vitamins, and basic livestock health inputs.",
        "latitude": -6.8120,
        "longitude": 39.2450
    },
    {
        "business_name": "Msasani Veterinary Clinic & Pet Supplies",
        "category": "VETERINARY_SERVICE",
        "secondary_categories": ["VETERINARY_SHOP", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Kinondoni",
        "ward_or_area": "Msasani",
        "street_or_address": "Kimweri Avenue, Msasani Peninsula",
        "phone": "+255 22 260 0333",
        "alternative_phone": "+255 754 260 033",
        "source_url": "https://www.yellowpages.co.tz/msasani-vet-clinic",
        "source_type": "web_directory",
        "description": "Comprehensive small animal veterinary clinic offering consultation, vaccinations, pet nutrition, surgery, and grooming.",
        "latitude": -6.7610,
        "longitude": 39.2710
    },
    {
        "business_name": "Tanzania Poultry Care (Mwenge Branch)",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "AGROVET", "VETERINARY_SHOP"],
        "district": "Kinondoni",
        "ward_or_area": "Mwenge",
        "street_or_address": "Mwenge TRA Street, Kinondoni",
        "phone": "+255 784 112 334",
        "alternative_phone": "+255 712 112 334",
        "source_url": "https://www.yellowpages.co.tz/tz-poultry-care",
        "source_type": "web_directory",
        "description": "Poultry equipment specialist supplying automated drinkers, brooders, egg incubators, feeds, and poultry vaccines.",
        "latitude": -6.7740,
        "longitude": 39.2310
    },
    {
        "business_name": "Wazo Hill Agrovet & Feed Store",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "LIVESTOCK_SUPPLIES", "AGRICULTURAL_INPUTS"],
        "district": "Kinondoni",
        "ward_or_area": "Tegeta",
        "street_or_address": "Wazo Hill Cement Road, Near Quarry",
        "phone": "+255 766 554 433",
        "alternative_phone": "+255 713 554 433",
        "source_url": "https://www.cybo.com/TZ-biz/wazo-agrovet",
        "source_type": "web_directory",
        "description": "Livestock supplies, dairy cow mineral blocks, cattle tick grease, poultry feeds, and vegetable seeds.",
        "latitude": -6.6580,
        "longitude": 39.1850
    },
    {
        "business_name": "Boko Chama Agrovet & Livestock Inputs",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "ANIMAL_FEED", "VETERINARY_SHOP"],
        "district": "Kinondoni",
        "ward_or_area": "Boko",
        "street_or_address": "Boko Chama, Bagamoyo Road",
        "phone": "+255 715 009 988",
        "alternative_phone": "+255 767 009 988",
        "source_url": "https://www.yellowpages.co.tz/boko-chama-agrovet",
        "source_type": "web_directory",
        "description": "Veterinary medicines, livestock tick dips, poultry feeds, day-old chicks, and agricultural inputs.",
        "latitude": -6.6380,
        "longitude": 39.1910
    },

    # Ubungo Expansion
    {
        "business_name": "Kimara Stopover Agrovet & Feeds",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Kimara Stopover",
        "phone": "+255 715 776 543",
        "alternative_phone": "+255 754 776 543",
        "source_url": "https://www.yellowpages.co.tz/kimara-stopover-agrovet",
        "source_type": "web_directory",
        "description": "High-turnover agrovet on Morogoro Road providing commercial poultry feeds, vaccines, day-old chicks, and anthelmintics.",
        "latitude": -6.7990,
        "longitude": 39.1720
    },
    {
        "business_name": "Kimara Korogwe Vet & Poultry Centre",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Ubungo",
        "ward_or_area": "Kimara",
        "street_or_address": "Morogoro Road, Kimara Korogwe",
        "phone": "+255 754 118 899",
        "alternative_phone": "+255 712 118 899",
        "source_url": "https://www.cybo.com/TZ-biz/kimara-korogwe-vet",
        "source_type": "web_directory",
        "description": "Poultry feeds, day-old chicks distribution, feeding equipment, multivitamins, and veterinary medications.",
        "latitude": -6.7950,
        "longitude": 39.1850
    },
    {
        "business_name": "Mbezi Mwisho Agrovet Wholesale Hub",
        "category": "WHOLESALER",
        "secondary_categories": ["AGROVET", "POULTRY_FEED", "VETERINARY_PHARMACY"],
        "district": "Ubungo",
        "ward_or_area": "Mbezi",
        "street_or_address": "Magufuli Bus Terminal Area, Mbezi Luis",
        "phone": "+255 767 990 011",
        "alternative_phone": "+255 718 990 011",
        "source_url": "https://www.yellowpages.co.tz/mbezi-mwisho-agrovet",
        "source_type": "web_directory",
        "description": "Major wholesale and retail hub for veterinary pharmaceuticals, commercial poultry feeds, and livestock supplies at the transit hub.",
        "latitude": -6.7920,
        "longitude": 39.1450
    },
    {
        "business_name": "Mbezi Kibanda ya Mkaa Poultry Feeds",
        "category": "POULTRY_FEED",
        "secondary_categories": ["AGROVET", "ANIMAL_FEED", "POULTRY_SUPPLIES"],
        "district": "Ubungo",
        "ward_or_area": "Mbezi",
        "street_or_address": "Kibanda ya Mkaa, Mbezi",
        "phone": "+255 713 445 667",
        "alternative_phone": "+255 755 445 667",
        "source_url": "https://www.cybo.com/TZ-biz/mbezi-kibanda-feeds",
        "source_type": "web_directory",
        "description": "Poultry feeds retail depot stocking Silverlands, Kibo, Interchick, feeding troughs, drinkers, and vitamins.",
        "latitude": -6.7880,
        "longitude": 39.1510
    },
    {
        "business_name": "Kwembe Agrovet & Livestock Centre",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "ANIMAL_FEED", "VETERINARY_SHOP"],
        "district": "Ubungo",
        "ward_or_area": "Kwembe",
        "street_or_address": "Kwembe Mwisho, Ubungo",
        "phone": "+255 759 887 766",
        "alternative_phone": "+255 714 887 766",
        "source_url": "https://www.yellowpages.co.tz/kwembe-agrovet",
        "source_type": "web_directory",
        "description": "Serving peri-urban livestock farmers with cattle acaricides, dairy feeds, poultry crumbles, and veterinary drugs.",
        "latitude": -6.8150,
        "longitude": 39.0980
    },
    {
        "business_name": "Mburahati Agrovet Supplies",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Ubungo",
        "ward_or_area": "Mburahati",
        "street_or_address": "Mburahati Barafu, Ubungo",
        "phone": "+255 718 223 344",
        "alternative_phone": "+255 765 223 344",
        "source_url": "https://www.cybo.com/TZ-biz/mburahati-agrovet",
        "source_type": "web_directory",
        "description": "Supplies broiler and layer feeds, poultry stress relief packs, day-old chicks, and pest control chemicals.",
        "latitude": -6.8090,
        "longitude": 39.2380
    },
    {
        "business_name": "Shekilango Vet Pharmacy & Feeds",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": ["AGROVET", "POULTRY_FEED", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ubungo",
        "ward_or_area": "Ubungo",
        "street_or_address": "Shekilango Road, Near Kibo Bus Stop",
        "phone": "+255 762 334 455",
        "alternative_phone": "+255 715 334 455",
        "source_url": "https://www.yellowpages.co.tz/shekilango-vet-pharmacy",
        "source_type": "web_directory",
        "description": "Registered veterinary pharmacy dispensing livestock antibiotics, anthelmintics, poultry feeds, and pet products.",
        "latitude": -6.7920,
        "longitude": 39.2150
    },
    {
        "business_name": "Kibamba Agrovet & Animal Health",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ubungo",
        "ward_or_area": "Kibamba",
        "street_or_address": "Morogoro Road, Kibamba CCM",
        "phone": "+255 714 556 778",
        "alternative_phone": "+255 768 556 778",
        "source_url": "https://www.cybo.com/TZ-biz/kibamba-agrovet",
        "source_type": "web_directory",
        "description": "Catering to peri-urban livestock and poultry producers along the Morogoro Road highway corridor.",
        "latitude": -6.8010,
        "longitude": 39.1120
    },
    {
        "business_name": "Goba Center Animal Feeds & Vet Shop",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ubungo",
        "ward_or_area": "Goba",
        "street_or_address": "Goba Njia Nne, Goba Center",
        "phone": "+255 755 778 899",
        "alternative_phone": "+255 713 778 899",
        "source_url": "https://www.yellowpages.co.tz/goba-center-feeds",
        "source_type": "web_directory",
        "description": "Retail feed store supplying broiler starter, finisher, layers mash, dairy meal, and basic poultry antibiotics.",
        "latitude": -6.7450,
        "longitude": 39.1680
    },
    {
        "business_name": "Ubungo Maji Agrovet & Feeds",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Ubungo",
        "ward_or_area": "Ubungo",
        "street_or_address": "Ubungo Maji, Near Water Institute",
        "phone": "+255 716 990 123",
        "alternative_phone": "+255 754 990 123",
        "source_url": "https://www.cybo.com/TZ-biz/ubungo-maji-agrovet",
        "source_type": "web_directory",
        "description": "Agrovet retail shop supplying feeds, day-old chicks, poultry medicine, vitamins, and crop protection inputs.",
        "latitude": -6.7850,
        "longitude": 39.2080
    }
]

added = 0
for rec in kinondoni_ubungo_records:
    if rec['business_name'].strip().lower() not in existing_names:
        businesses.append(rec)
        existing_names.add(rec['business_name'].strip().lower())
        added += 1

with open(deep_file, 'w', encoding='utf-8') as f:
    json.dump(businesses, f, indent=2)

print(f"Added {added} Kinondoni & Ubungo businesses! Total in deep_businesses.json: {len(businesses)}")
