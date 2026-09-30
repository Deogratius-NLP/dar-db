import uuid

DISTRICTS_AND_AREAS = {
    'Kinondoni': [
        'Tegeta', 'Bunju', 'Kawe', 'Mikocheni', 'Masaki', 'Oyster Bay', 
        'Kijitonyama', 'Mwenge', 'Kinondoni', 'Kunduchi', 'Wazo', 'Boko', 
        'Magomeni', 'Tandale', 'Ndugumbi', 'Kigogo', 'Mwananyamala', 'Hananasif'
    ],
    'Ubungo': [
        'Sinza', 'Ubungo', 'Kimara', 'Mbezi', 'Mbezi Beach', 'Goba', 
        'Kibamba', 'Manzese', 'Mabibo', 'Makuburi', 'Kinyerezi', 'Kwembe', 
        'Msigani', 'Saranga'
    ],
    'Ilala': [
        'Kariakoo', 'Tabata', 'Buguruni', 'Segerea', 'Vingunguti', 'Ilala', 
        'Kivukoni', 'Upanga', 'Kisutu', 'Gerezani', 'Jangwani', 'Mchafukoge', 
        'Kipawa', 'Ukonga', 'Gongolamboto', 'Chanika', 'Pugu', 'Kitunda', 'Kivule'
    ],
    'Temeke': [
        'Mbagala', 'Temeke', 'Chang\'ombe', 'Keko', 'Kurasini', 'Tandika', 
        'Sandali', 'Yombo Vituka', 'Miburani', 'Toangoma', 'Chamazi', 
        'Kiburugwa', 'Charambe', 'Kongowe', 'Buza'
    ],
    'Kigamboni': [
        'Kigamboni', 'Ferry', 'Vijibweni', 'Kibada', 'Kisarawe II', 
        'Somangila', 'Pembamnazi', 'Kimbiji', 'Tungi', 'Gezaulole', 'Mjimwema'
    ]
}

# The Top 8 High-Density Commercial Hotspots ("Stranded Clusters")
HOTSPOT_CLUSTERS = {
    'Buguruni Cluster': {
        'district': 'Ilala',
        'focal_areas': ['Buguruni', 'Buguruni Chama', 'Buguruni Malapa', 'Mandela Road'],
        'specialty': 'Primary live day-old chick trade hub & retail poultry feed depot centre',
        'centroid': (-6.8310, 39.2480),
        'radius_km': 1.5
    },
    'Kariakoo & Gerezani Cluster': {
        'district': 'Ilala',
        'focal_areas': ['Kariakoo', 'Gerezani', 'Msimbazi', 'Swahili', 'Narung\'ombe'],
        'specialty': 'National wholesale clearinghouse for veterinary pharmaceuticals, vaccines & sprayers',
        'centroid': (-6.8220, 39.2780),
        'radius_km': 1.5
    },
    'Mbagala Cluster': {
        'district': 'Temeke',
        'focal_areas': ['Mbagala Rangi Tatu', 'Mbagala Zakhem', 'Majimatitu', 'Charambe'],
        'specialty': 'Massive peri-urban poultry feed depot cluster & high-volume retail agrovets',
        'centroid': (-6.9020, 39.2650),
        'radius_km': 2.5
    },
    'Tegeta & Wazo Hill Cluster': {
        'district': 'Kinondoni',
        'focal_areas': ['Tegeta', 'Wazo Hill', 'Tegeta Kibaoni', 'Bagamoyo Road'],
        'specialty': 'Northern arterial gateway hub for poultry feeds, veterinary clinics & inputs',
        'centroid': (-6.6667, 39.2167),
        'radius_km': 2.5
    },
    'Kitunda & Chanika Cluster': {
        'district': 'Ilala',
        'focal_areas': ['Kitunda', 'Chanika', 'Kivule', 'Machimbo'],
        'specialty': 'Highest-density peri-urban poultry & livestock farming belt in Dar es Salaam',
        'centroid': (-6.9200, 39.1800),
        'radius_km': 4.0
    },
    'Mbezi & Kimara Corridor': {
        'district': 'Ubungo',
        'focal_areas': ['Mbezi Luis', 'Magufuli Terminal', 'Kibanda ya Mkaa', 'Kimara Stopover', 'Korogwe'],
        'specialty': 'Upcountry transit corridor & high-turnover feeds, chicks & veterinary drugs',
        'centroid': (-6.7950, 39.1600),
        'radius_km': 3.5
    },
    'Tandika & Chang\'ombe Cluster': {
        'district': 'Temeke',
        'focal_areas': ['Tandika', 'Chang\'ombe', 'Temeke Stereo', 'Pugu Road Junction'],
        'specialty': 'Tandika live bird market & Chang\'ombe industrial feed milling/equipment sector',
        'centroid': (-6.8550, 39.2650),
        'radius_km': 2.0
    },
    'Kibada & Kisarawe II Corridor': {
        'district': 'Kigamboni',
        'focal_areas': ['Kibada', 'Kibugumo', 'Kisarawe II', 'Mjimwema'],
        'specialty': 'Fastest-growing coastal commercial poultry corridor & feed distribution hub',
        'centroid': (-6.8950, 39.3450),
        'radius_km': 3.5
    }
}

# Swahili Trade Vernacular Query Terminology
SWAHILI_TRADE_TERMS = [
    ('POULTRY_FEED', 'vyakula vya kuku'),
    ('POULTRY_FEED', 'chakula cha kuku'),
    ('ANIMAL_FEED', 'chakula cha mifugo'),
    ('POULTRY_SUPPLIES', 'vifaranga vya kuku'),
    ('POULTRY_SUPPLIES', 'vifaranga vya broiler na layer'),
    ('VETERINARY_SHOP', 'madawa ya mifugo'),
    ('VETERINARY_SHOP', 'dawa za mifugo'),
    ('ANIMAL_HEALTH_SUPPLIER', 'chanjo za kuku'),
    ('AGROVET', 'pembejeo za kilimo na mifugo'),
    ('LIVESTOCK_SUPPLIES', 'dawa ya kuogesha ng\'ombe'),
    ('POULTRY_SUPPLIES', 'vifaa vya ufugaji wa kuku'),
    ('ANIMAL_FEED', 'pumba na mashudu ya alizeti'),
    ('AGROVET', 'duka la pembejeo')
]

# Value Chain Reverse-Engineering Brands & Integrators
VALUE_CHAIN_BRANDS = [
    ('POULTRY_FEED', 'Interchick'),
    ('POULTRY_FEED', 'Silverlands'),
    ('ANIMAL_FEED', 'Anifeed Anigrain'),
    ('ANIMAL_FEED', 'Tanfeed'),
    ('POULTRY_FEED', 'Hill Feed'),
    ('POULTRY_FEED', 'FeedPro EMAX'),
    ('POULTRY_FEED', 'Kibo Feeds'),
    ('POULTRY_SUPPLIES', 'Irvine\'s'),
    ('DISTRIBUTOR', 'Farmbase'),
    ('ANIMAL_HEALTH_SUPPLIER', 'Ultravetis'),
    ('WHOLESALER', 'Afrovet'),
    ('DISTRIBUTOR', 'Ashish Life Science')
]

SEARCH_TERMS = [
    ('AGROVET', 'agrovet'),
    ('AGROVET', 'duka la pembejeo'),
    ('VETERINARY_SHOP', 'veterinary shop'),
    ('VETERINARY_SHOP', 'madawa ya mifugo'),
    ('VETERINARY_PHARMACY', 'veterinary pharmacy'),
    ('ANIMAL_FEED', 'animal feed'),
    ('POULTRY_FEED', 'chakula cha kuku'),
    ('POULTRY_FEED', 'vyakula vya kuku'),
    ('POULTRY_SUPPLIES', 'vifaranga vya kuku'),
    ('ANIMAL_HEALTH_SUPPLIER', 'animal health'),
    ('ANIMAL_HEALTH_SUPPLIER', 'chanjo za kuku'),
    ('LIVESTOCK_SUPPLIES', 'vifaa vya mifugo')
]

def generate_cluster_search_tasks():
    """Generates targeted Swahili & brand queries for the top 8 hotspots."""
    tasks = []
    for cluster_name, info in HOTSPOT_CLUSTERS.items():
        district = info['district']
        for area in info['focal_areas']:
            # 1. Swahili Trade Terms
            for cat, term in SWAHILI_TRADE_TERMS[:6]:
                slug = term.replace(' ', '_').replace('\'', '')
                tasks.append({
                    'search_task_id': f'hotspot_{cluster_name[:6]}_{area}_{slug}',
                    'category': cat,
                    'district': district,
                    'area': area,
                    'cluster': cluster_name,
                    'search_term': f'{term} {area} Dar es Salaam',
                    'source': 'hotspot_matrix',
                    'status': 'PENDING'
                })
            # 2. Value-Chain Brands
            for cat, brand in VALUE_CHAIN_BRANDS[:4]:
                brand_slug = brand.replace(' ', '_').replace('/', '_')
                tasks.append({
                    'search_task_id': f'brand_{cluster_name[:6]}_{area}_{brand_slug}',
                    'category': cat,
                    'district': district,
                    'area': area,
                    'cluster': cluster_name,
                    'search_term': f'{brand} {area} Dar es Salaam',
                    'source': 'value_chain_brand',
                    'status': 'PENDING'
                })
    return tasks

def generate_search_tasks(pilot_only=False, pilot_areas=None):
    if pilot_areas is None:
        pilot_areas = ['Tegeta', 'Bunju', 'Sinza']
        
    tasks = []
    
    if pilot_only:
        for district, areas in DISTRICTS_AND_AREAS.items():
            for area in areas:
                if area in pilot_areas:
                    for cat, term in SEARCH_TERMS:
                        slug = term.replace(' ', '_')
                        task_id = f'pilot_{district}_{area}_{cat}_{slug}'
                        tasks.append({
                            'search_task_id': task_id,
                            'category': cat,
                            'district': district,
                            'area': area,
                            'search_term': f'{term} {area} Dar es Salaam',
                            'source': 'multi_source',
                            'status': 'PENDING'
                        })
    else:
        for district, areas in DISTRICTS_AND_AREAS.items():
            for cat, term in SEARCH_TERMS:
                slug = term.replace(' ', '_')
                task_id = f'dist_{district}_{cat}_{slug}'
                tasks.append({
                    'search_task_id': task_id,
                    'category': cat,
                    'district': district,
                    'area': 'All',
                    'search_term': f'{term} {district} Dar es Salaam',
                    'source': 'multi_source',
                    'status': 'PENDING'
                })
            for area in areas:
                for cat, term in SEARCH_TERMS[:5]:
                    slug = term.replace(' ', '_')
                    task_id = f'area_{district}_{area}_{cat}_{slug}'
                    tasks.append({
                        'search_task_id': task_id,
                        'category': cat,
                        'district': district,
                        'area': area,
                        'search_term': f'{term} {area} Dar es Salaam',
                        'source': 'multi_source',
                        'status': 'PENDING'
                    })
    return tasks

if __name__ == '__main__':
    cluster_tasks = generate_cluster_search_tasks()
    print(f'Defined {len(HOTSPOT_CLUSTERS)} Hotspot Clusters.')
    print(f'Generated {len(cluster_tasks)} cluster-specific Swahili & Value-Chain tasks.')
