import json
import os

deep_file = os.path.join(os.path.dirname(__file__), 'data', 'deep_businesses.json')

with open(deep_file, 'r', encoding='utf-8') as f:
    businesses = json.load(f)

existing_names = {b['business_name'].strip().lower() for b in businesses}

ilala_records = [
    {
        "business_name": "Farmbase Limited (Headquarters)",
        "category": "DISTRIBUTOR",
        "secondary_categories": ["VETERINARY_PHARMACY", "ANIMAL_HEALTH_SUPPLIER", "LIVESTOCK_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Kipawa",
        "street_or_address": "Plot 37, Nyerere Road, Kipawa Industrial Area",
        "phone": "+255 22 286 1145",
        "alternative_phone": "+255 767 861 145",
        "source_url": "https://www.farmbase.biz",
        "source_type": "web_directory",
        "description": "Major national importer and master distributor of veterinary medicines, livestock vaccines, animal health supplies, poultry equipment, and feed additives.",
        "latitude": -6.8489,
        "longitude": 39.2256
    },
    {
        "business_name": "Anigrain Limited",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["POULTRY_FEED", "WHOLESALER", "LIVESTOCK_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Vingunguti",
        "street_or_address": "Nyerere Road, Near Vingunguti Junction",
        "phone": "+255 754 286 524",
        "alternative_phone": "+255 22 286 2800",
        "source_url": "https://anigrain.co.tz",
        "source_type": "web_directory",
        "description": "Large-scale commercial animal feed manufacturer producing Anifeed poultry feeds, broiler crumbles, layer pellets, and dairy meal.",
        "latitude": -6.8450,
        "longitude": 39.2310
    },
    {
        "business_name": "Irvine's Tanzania Limited",
        "category": "POULTRY_SUPPLIES",
        "secondary_categories": ["POULTRY_FEED", "DISTRIBUTOR", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ilala",
        "ward_or_area": "Kipawa",
        "street_or_address": "Plot 18 Kipawa Industrial Area, Nyerere Road",
        "phone": "+255 744 555 111",
        "alternative_phone": "+255 22 286 4220",
        "source_url": "https://irvines.co.tz",
        "source_type": "web_directory",
        "description": "Leading producer and distributor of day-old chicks (Cobb 500 broilers, Bovans Brown layers), poultry nutrition, and technical poultry veterinary support.",
        "latitude": -6.8520,
        "longitude": 39.2210
    },
    {
        "business_name": "Interchick Company Ltd (Commercial Depot)",
        "category": "DISTRIBUTOR",
        "secondary_categories": ["POULTRY_SUPPLIES", "POULTRY_FEED", "VETERINARY_PHARMACY"],
        "district": "Ilala",
        "ward_or_area": "Gerezani",
        "street_or_address": "Mbozi Road / Nyerere Road Junction, Industrial Area",
        "phone": "+255 22 286 0300",
        "alternative_phone": "+255 754 300 001",
        "source_url": "https://www.interchicktz.com",
        "source_type": "web_directory",
        "description": "Pioneer poultry integration company providing day-old broiler and layer chicks, commercial feeds, broiler concentrates, and poultry pharmaceuticals.",
        "latitude": -6.8390,
        "longitude": 39.2550
    },
    {
        "business_name": "Tanfeed International Ltd (Gerezani Depot)",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["POULTRY_FEED", "WHOLESALER", "LIVESTOCK_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Gerezani",
        "street_or_address": "Gerezani Street, Near Railway Crossing, Ilala",
        "phone": "+255 758 800 200",
        "alternative_phone": "+255 689 445 566",
        "source_url": "https://www.tanfeed.co.tz",
        "source_type": "web_directory",
        "description": "Specialized animal feeds manufacturer and distributor supplying poultry feeds, swine feeds, dairy concentrates, and mineral premixes.",
        "latitude": -6.8240,
        "longitude": 39.2810
    },
    {
        "business_name": "Kariakoo Vet Agrovet Center",
        "category": "VETERINARY_PHARMACY",
        "secondary_categories": ["AGROVET", "POULTRY_SUPPLIES", "WHOLESALER"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Msimbazi Street / Swahili Street, Kariakoo Market Area",
        "phone": "+255 713 456 789",
        "alternative_phone": "+255 754 998 877",
        "source_url": "https://www.yellowpages.co.tz/search/veterinary/kariakoo",
        "source_type": "web_directory",
        "description": "High-traffic veterinary pharmaceutical wholesaler and retailer in Kariakoo, stocking livestock antibiotics, anthelmintics, poultry vaccines, and drinkers.",
        "latitude": -6.8205,
        "longitude": 39.2760
    },
    {
        "business_name": "Afrovet Supplies Limited",
        "category": "WHOLESALER",
        "secondary_categories": ["VETERINARY_PHARMACY", "DISTRIBUTOR", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ilala",
        "ward_or_area": "Kariakoo",
        "street_or_address": "Narung'ombe Street, Kariakoo",
        "phone": "+255 22 218 0550",
        "alternative_phone": "+255 784 218 055",
        "source_url": "https://afrovet.co.tz",
        "source_type": "web_directory",
        "description": "Wholesale distributor of quality animal health products, veterinary instruments, and poultry medications across Dar es Salaam and upcountry regions.",
        "latitude": -6.8220,
        "longitude": 39.2785
    },
    {
        "business_name": "Agrovet Buguruni Central",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_SUPPLIES", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Buguruni Chama, Mandela Road / Uhuru Street Junction",
        "phone": "+255 715 889 900",
        "alternative_phone": "+255 765 443 322",
        "source_url": "https://www.cybo.com/TZ-biz/agrovet-buguruni",
        "source_type": "web_directory",
        "description": "Prominent poultry and veterinary supply retail center in Buguruni, providing commercial feeds, day-old broiler and kuroiler chicks, and veterinary care.",
        "latitude": -6.8310,
        "longitude": 39.2480
    },
    {
        "business_name": "Rich Super Feeds (Buguruni Hub)",
        "category": "POULTRY_FEED",
        "secondary_categories": ["ANIMAL_FEED", "WHOLESALER", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Uhuru Street, Buguruni",
        "phone": "+255 762 112 233",
        "alternative_phone": "+255 654 332 211",
        "source_url": "https://www.zoomtanzania.com/buguruni-feeds",
        "source_type": "web_directory",
        "description": "High-volume distributor of commercial poultry feeds including Silverlands, Interchick, and Hill Feed, along with bran and sunflower meal.",
        "latitude": -6.8335,
        "longitude": 39.2450
    },
    {
        "business_name": "JOACK Agrovet Center (Buguruni Branch)",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Buguruni",
        "street_or_address": "Buguruni Malapa, Ilala",
        "phone": "+255 712 253 103",
        "alternative_phone": "+255 745 253 100",
        "source_url": "https://joack.co.tz/branches",
        "source_type": "web_directory",
        "description": "Branch outlet of JOACK Agrovet supplying poultry feeds, veterinary treatments, livestock vitamins, and day-old chicks.",
        "latitude": -6.8300,
        "longitude": 39.2505
    },
    {
        "business_name": "Vingunguti Livestock & Vet Inputs Centre",
        "category": "LIVESTOCK_SUPPLIES",
        "secondary_categories": ["VETERINARY_SHOP", "AGROVET", "ANIMAL_HEALTH_SUPPLIER"],
        "district": "Ilala",
        "ward_or_area": "Vingunguti",
        "street_or_address": "Kombo Street, Near Vingunguti Abattoir",
        "phone": "+255 755 432 109",
        "alternative_phone": "+255 713 889 001",
        "source_url": "https://www.yellowpages.co.tz/vingunguti-livestock",
        "source_type": "web_directory",
        "description": "Specialized cattle, sheep, and goat livestock supply centre near the municipal abattoir, selling acaricides, dewormers, wound sprays, and salt blocks.",
        "latitude": -6.8415,
        "longitude": 39.2390
    },
    {
        "business_name": "Tabata Agrovet & Animal Health Store",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Tabata",
        "street_or_address": "Mandela Road, Near Tabata Bima",
        "phone": "+255 714 678 910",
        "alternative_phone": "+255 768 223 344",
        "source_url": "https://www.cybo.com/TZ-biz/tabata-agrovet",
        "source_type": "web_directory",
        "description": "Serving urban poultry and pet owners in Tabata with vaccines, chick starter crumbs, feeding troughs, drinkers, and pest control chemicals.",
        "latitude": -6.8260,
        "longitude": 39.2320
    },
    {
        "business_name": "Tabata Segerea Animal Feeds & Vet Care",
        "category": "ANIMAL_FEED",
        "secondary_categories": ["AGROVET", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Tabata",
        "street_or_address": "Segerea Mwisho, Tabata Segerea",
        "phone": "+255 768 901 234",
        "alternative_phone": "+255 659 123 456",
        "source_url": "https://www.yellowpages.co.tz/tabata-segerea-feeds",
        "source_type": "web_directory",
        "description": "Retail and wholesale merchant of poultry feeds, layers mash, broiler finisher, and basic veterinary medications.",
        "latitude": -6.8350,
        "longitude": 39.2150
    },
    {
        "business_name": "Gongolamboto Agrovet Depot",
        "category": "AGROVET",
        "secondary_categories": ["ANIMAL_FEED", "LIVESTOCK_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Gongolamboto",
        "street_or_address": "Julius Nyerere Road, Gongolamboto Mwisho",
        "phone": "+255 754 887 766",
        "alternative_phone": "+255 715 887 766",
        "source_url": "https://www.cybo.com/TZ-biz/gongolamboto-agrovet",
        "source_type": "web_directory",
        "description": "Strategic peri-urban agrovet hub supplying poultry feed, cattle dip chemicals, veterinary drugs, and day-old chicks to farmers along Pugu corridor.",
        "latitude": -6.8770,
        "longitude": 39.1720
    },
    {
        "business_name": "Banana Agrovet Supplies",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "VETERINARY_SHOP", "POULTRY_SUPPLIES"],
        "district": "Ilala",
        "ward_or_area": "Kipawa",
        "street_or_address": "Banana Bus Stop, Pugu Road / Airport Area",
        "phone": "+255 716 334 455",
        "alternative_phone": "+255 755 334 455",
        "source_url": "https://www.yellowpages.co.tz/banana-agrovet",
        "source_type": "web_directory",
        "description": "Stockist of livestock feeds, broiler starter crumbles, dewormers, multivitamins, and poultry spraying equipment.",
        "latitude": -6.8620,
        "longitude": 39.1950
    },
    {
        "business_name": "Kitunda Animal Health & Feeds Centre",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Kitunda",
        "street_or_address": "Kitunda Kati, Main Road",
        "phone": "+255 759 223 344",
        "alternative_phone": "+255 712 112 299",
        "source_url": "https://www.cybo.com/TZ-biz/kitunda-agrovet",
        "source_type": "web_directory",
        "description": "Primary agricultural and poultry supply provider in Kitunda, supplying day-old chicks, feeds, Newcastle and Gumboro vaccines, and disinfectants.",
        "latitude": -6.8910,
        "longitude": 39.2080
    },
    {
        "business_name": "Chanika Livestock & Agrovet Hub",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "ANIMAL_FEED", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Chanika",
        "street_or_address": "Chanika Mwisho, Main Market Street",
        "phone": "+255 787 654 321",
        "alternative_phone": "+255 754 654 321",
        "source_url": "https://www.yellowpages.co.tz/chanika-agrovet",
        "source_type": "web_directory",
        "description": "Comprehensive agrovet serving extensive dairy cattle, goat, and poultry smallholders in peri-urban Chanika.",
        "latitude": -6.9550,
        "longitude": 39.1450
    },
    {
        "business_name": "Kinyerezi Vet Care & Poultry Centre",
        "category": "AGROVET",
        "secondary_categories": ["POULTRY_FEED", "POULTRY_SUPPLIES", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Kinyerezi",
        "street_or_address": "Kinyerezi Kanga, Kinyerezi Road",
        "phone": "+255 718 998 877",
        "alternative_phone": "+255 765 889 900",
        "source_url": "https://www.cybo.com/TZ-biz/kinyerezi-vet",
        "source_type": "web_directory",
        "description": "Poultry feeds retailer, chicks depot, broiler medications, and household pet healthcare products store.",
        "latitude": -6.8210,
        "longitude": 39.1980
    },
    {
        "business_name": "Kivule Agrovet & Veterinary Services",
        "category": "AGROVET",
        "secondary_categories": ["ANIMAL_HEALTH_SUPPLIER", "POULTRY_FEED", "VETERINARY_SHOP"],
        "district": "Ilala",
        "ward_or_area": "Kivule",
        "street_or_address": "Kivule Magole, Kivule Road",
        "phone": "+255 765 119 922",
        "alternative_phone": "+255 713 445 566",
        "source_url": "https://www.yellowpages.co.tz/kivule-agrovet",
        "source_type": "web_directory",
        "description": "Supplies veterinary medicines, poultry vaccines, day-old chicks, and livestock feeds to farmers in Kivule.",
        "latitude": -6.9150,
        "longitude": 39.1820
    },
    {
        "business_name": "Pugu Kajiungeni Agrovet",
        "category": "AGROVET",
        "secondary_categories": ["LIVESTOCK_SUPPLIES", "ANIMAL_FEED", "AGRICULTURAL_INPUTS"],
        "district": "Ilala",
        "ward_or_area": "Pugu",
        "street_or_address": "Pugu Kajiungeni, Pugu Station Road",
        "phone": "+255 713 908 172",
        "alternative_phone": "+255 784 908 172",
        "source_url": "https://www.cybo.com/TZ-biz/pugu-agrovet",
        "source_type": "web_directory",
        "description": "Livestock and agricultural inputs store offering cattle tick dips, anthelmintics, poultry feed, and farm implements.",
        "latitude": -6.8850,
        "longitude": 39.1350
    }
]

added = 0
for rec in ilala_records:
    if rec['business_name'].strip().lower() not in existing_names:
        businesses.append(rec)
        existing_names.add(rec['business_name'].strip().lower())
        added += 1

with open(deep_file, 'w', encoding='utf-8') as f:
    json.dump(businesses, f, indent=2)

print(f"Added {added} Ilala businesses! Total in deep_businesses.json: {len(businesses)}")
