import os
import sys
import sqlite3
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "dar_agrovet.db")
EXCEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "Dar_Es_Salaam_Agrovet_Database.xlsx")

def export_to_excel(db_path=DB_PATH, excel_path=EXCEL_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)
    
    # Styles
    header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid") # Dark blue
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    zebra_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    def style_table(ws, headers, rows):
        ws.append(headers)
        for col_num in range(1, len(headers) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            ws.row_dimensions[1].height = 28
            
        for r_idx, row in enumerate(rows, start=2):
            ws.append(row)
            ws.row_dimensions[r_idx].height = 20
            is_zebra = (r_idx % 2 == 0)
            for c_idx in range(1, len(row) + 1):
                cell = ws.cell(row=r_idx, column=c_idx)
                cell.border = border_thin
                cell.font = Font(name="Calibri", size=10)
                if is_zebra:
                    cell.fill = zebra_fill
                if c_idx in [1, 9, 10]: # IDs or coordinates
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    cell.alignment = Alignment(vertical="center")
                    
        # Auto column width
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or '')
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 45)

    # -------------------------------------------------------------
    # 1. MASTER DATABASE
    # -------------------------------------------------------------
    ws1 = wb.create_sheet("MASTER DATABASE")
    headers1 = [
        "ID", "Business Name", "Category", "Secondary Categories", 
        "District", "Ward / Area", "Hotspot Cluster", "Street Address", "Phone", 
        "Alternative Phone", "WhatsApp", "Email", "Website", 
        "Latitude", "Longitude", "Google Maps Link", "Confidence", 
        "Evidence", "Duplicate Status", "Sources"
    ]
    cur.execute('''
        SELECT id, business_name, category, secondary_categories,
               district, ward_or_area, hotspot_cluster, street_or_address, phone,
               alternative_phone, whatsapp, email, website,
               latitude, longitude, confidence, evidence, duplicate_status, source_types
        FROM master_businesses
        WHERE verification_status = 'VERIFIED'
        ORDER BY 
            CASE WHEN hotspot_cluster = 'GENERAL_METROPOLITAN' OR hotspot_cluster IS NULL THEN 1 ELSE 0 END,
            hotspot_cluster, district, ward_or_area, business_name
    ''')
    rows1 = []
    for r in cur.fetchall():
        lat = r['latitude']
        lon = r['longitude']
        gmaps = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else ""
        sec = ", ".join(json.loads(r['secondary_categories'] or '[]'))
        src = ", ".join(json.loads(r['source_types'] or '[]'))
        rows1.append([
            r['id'], r['business_name'], r['category'], sec,
            r['district'], r['ward_or_area'], r['hotspot_cluster'] or 'GENERAL_METROPOLITAN',
            r['street_or_address'], r['phone'],
            r['alternative_phone'], r['whatsapp'], r['email'], r['website'],
            lat, lon, gmaps, r['confidence'], r['evidence'], r['duplicate_status'], src
        ])
    style_table(ws1, headers1, rows1)

    # -------------------------------------------------------------
    # 2. NEEDS REVIEW
    # -------------------------------------------------------------
    ws2 = wb.create_sheet("NEEDS REVIEW")
    headers2 = [
        "ID", "Business Name", "Category", "District", "Ward / Area", 
        "Street Address", "Phone", "Latitude", "Longitude", "Evidence / Ambiguity Note", "Sources"
    ]
    cur.execute('''
        SELECT id, business_name, category, district, ward_or_area, 
               street_or_address, phone, latitude, longitude, evidence, source_types
        FROM master_businesses
        WHERE verification_status = 'NEEDS_REVIEW'
        ORDER BY business_name
    ''')
    rows2 = []
    for r in cur.fetchall():
        src = ", ".join(json.loads(r['source_types'] or '[]'))
        rows2.append([
            r['id'], r['business_name'], r['category'], r['district'], r['ward_or_area'],
            r['street_or_address'], r['phone'], r['latitude'], r['longitude'], r['evidence'], src
        ])
    style_table(ws2, headers2, rows2)

    # -------------------------------------------------------------
    # 3. NOT RELEVANT
    # -------------------------------------------------------------
    ws3 = wb.create_sheet("NOT RELEVANT")
    headers3 = ["ID", "Business Name", "Excluded Category", "Exclusion Reason", "Evidence", "District", "Sources"]
    cur.execute('''
        SELECT id, business_name, category, exclusion_reason, evidence, district, source_types
        FROM master_businesses
        WHERE verification_status = 'NOT_RELEVANT'
        ORDER BY business_name
    ''')
    rows3 = []
    for r in cur.fetchall():
        src = ", ".join(json.loads(r['source_types'] or '[]'))
        rows3.append([
            r['id'], r['business_name'], r['category'], r['exclusion_reason'], r['evidence'], r['district'], src
        ])
    style_table(ws3, headers3, rows3)

    # -------------------------------------------------------------
    # 4. DISTRICT SUMMARY
    # -------------------------------------------------------------
    ws4 = wb.create_sheet("DISTRICT SUMMARY")
    headers4 = ["District", "Verified Businesses", "Percentage of Total"]
    cur.execute("SELECT COUNT(*) FROM master_businesses WHERE verification_status = 'VERIFIED'")
    total_verified = cur.fetchone()[0] or 1
    cur.execute('''
        SELECT district, COUNT(*) as cnt
        FROM master_businesses
        WHERE verification_status = 'VERIFIED'
        GROUP BY district
        ORDER BY cnt DESC
    ''')
    rows4 = []
    for r in cur.fetchall():
        pct = f"{(r['cnt'] / total_verified) * 100:.1f}%"
        rows4.append([r['district'], r['cnt'], pct])
    style_table(ws4, headers4, rows4)

    # -------------------------------------------------------------
    # 5. AREA SUMMARY
    # -------------------------------------------------------------
    ws5 = wb.create_sheet("AREA SUMMARY")
    headers5 = ["District", "Ward / Area", "Verified Businesses"]
    cur.execute('''
        SELECT district, ward_or_area, COUNT(*) as cnt
        FROM master_businesses
        WHERE verification_status = 'VERIFIED'
        GROUP BY district, ward_or_area
        ORDER BY district, cnt DESC
    ''')
    rows5 = [[r['district'], r['ward_or_area'], r['cnt']] for r in cur.fetchall()]
    style_table(ws5, headers5, rows5)

    # -------------------------------------------------------------
    # 6. CATEGORY SUMMARY
    # -------------------------------------------------------------
    ws6 = wb.create_sheet("CATEGORY SUMMARY")
    headers6 = ["Primary Category", "Business Count", "Percentage"]
    cur.execute('''
        SELECT category, COUNT(*) as cnt
        FROM master_businesses
        WHERE verification_status = 'VERIFIED'
        GROUP BY category
        ORDER BY cnt DESC
    ''')
    rows6 = []
    for r in cur.fetchall():
        pct = f"{(r['cnt'] / total_verified) * 100:.1f}%"
        rows6.append([r['category'], r['cnt'], pct])
    style_table(ws6, headers6, rows6)

    # -------------------------------------------------------------
    # 7. SOURCE SUMMARY
    # -------------------------------------------------------------
    ws7 = wb.create_sheet("SOURCE SUMMARY")
    headers7 = ["Source Platform / Channel", "Total Discovered Records", "Estimated API Cost ($)"]
    cur.execute('''
        SELECT source, SUM(records_returned) as total_recs, SUM(estimated_cost) as total_cost
        FROM usage_log
        GROUP BY source
        ORDER BY total_recs DESC
    ''')
    rows7 = []
    for r in cur.fetchall():
        rows7.append([r['source'], r['total_recs'], f"${r['total_cost']:.2f}"])
    style_table(ws7, headers7, rows7)

    # -------------------------------------------------------------
    # 8. SEARCH COVERAGE
    # -------------------------------------------------------------
    ws8 = wb.create_sheet("SEARCH COVERAGE")
    headers8 = ["Task ID", "Target Category", "District", "Area", "Search Term", "Status", "Date Completed"]
    cur.execute('''
        SELECT search_task_id, category, district, area, search_term, status, date_completed
        FROM search_tasks
        ORDER BY district, area
    ''')
    rows8 = []
    for r in cur.fetchall():
        rows8.append([
            r['search_task_id'], r['category'], r['district'], r['area'], 
            r['search_term'], r['status'], r['date_completed'] or "Completed"
        ])
    style_table(ws8, headers8, rows8)

    # -------------------------------------------------------------
    # 9. HOTSPOT CLUSTERS
    # -------------------------------------------------------------
    ws9 = wb.create_sheet("HOTSPOT CLUSTERS")
    headers9 = [
        "Hotspot Cluster", "District", "Verified Businesses", 
        "Percentage of Total", "Primary Commercial Specialty", 
        "Centroid Coordinates", "Field Marketing Priority & Route Strategy"
    ]
    
    cluster_strategies = {
        'Buguruni Cluster': {
            'priority': 'HIGH PRIORITY',
            'strategy': 'Walk Uhuru St & Mandela Rd junction. Target live chick booking depots and high-turnover broiler feed retailers.'
        },
        'Kariakoo & Gerezani Cluster': {
            'priority': 'CRITICAL / WHOLESALE',
            'strategy': 'Key clearinghouse for national and regional distribution. Target veterinary pharmaceutical wholesalers & feed millers.'
        },
        'Mbagala Cluster': {
            'priority': 'HIGH PRIORITY',
            'strategy': 'Route along Kilwa Rd from Zakhem to Rangi Tatu. Target large-volume commercial feed distributors and vaccination stockists.'
        },
        'Tegeta & Wazo Hill Cluster': {
            'priority': 'HIGH PRIORITY',
            'strategy': 'Northern arterial sweep along Bagamoyo Rd. Target peri-urban agrovets, dairy inputs, and poultry centers.'
        },
        'Kitunda & Chanika Cluster': {
            'priority': 'HIGH DENSITY PRODUCERS',
            'strategy': 'Smallholder poultry farming heartland. Target local agrovet stockists providing day-old chicks and Newcastle/Gumboro vaccines.'
        },
        'Mbezi & Kimara Corridor': {
            'priority': 'TRANSIT / REGIONAL',
            'strategy': 'Morogoro Rd highway corridor. Target transit feed depots around Magufuli Terminal, Stopover, and Kimara.'
        },
        'Tandika & Chang\'ombe Cluster': {
            'priority': 'MARKET & INDUSTRIAL',
            'strategy': 'Combine Tandika live poultry market visits with Chang\'ombe industrial feed additives & equipment suppliers.'
        },
        'Kibada & Kisarawe II Corridor': {
            'priority': 'GROWTH CORRIDOR',
            'strategy': 'Rapidly expanding commercial poultry belt. Target new feed depots, poultry housing equipment, and dairy inputs.'
        },
        'GENERAL_METROPOLITAN': {
            'priority': 'SECONDARY / DISPERSED',
            'strategy': 'Dispersed urban and residential retail clinics (Masaki, Mikocheni, Sinza, Mwenge, Ilala Boma) for companion animal & boutique products.'
        }
    }
    
    from backend.discovery.search_matrix import HOTSPOT_CLUSTERS
    cur.execute('''
        SELECT hotspot_cluster, COUNT(*) as cnt
        FROM master_businesses
        WHERE verification_status = 'VERIFIED'
        GROUP BY hotspot_cluster
        ORDER BY 
            CASE WHEN hotspot_cluster = 'GENERAL_METROPOLITAN' OR hotspot_cluster IS NULL THEN 1 ELSE 0 END,
            cnt DESC
    ''')
    rows9 = []
    for r in cur.fetchall():
        c_name = r['hotspot_cluster'] or 'GENERAL_METROPOLITAN'
        cnt = r['cnt']
        pct = f"{(cnt / total_verified) * 100:.1f}%"
        info = HOTSPOT_CLUSTERS.get(c_name, {})
        dist = info.get('district', 'Metropolitan Wide')
        spec = info.get('specialty', 'Dispersed urban veterinary and pet care services')
        coords = f"{info['centroid'][0]:.4f}, {info['centroid'][1]:.4f}" if 'centroid' in info else "Multi-centroid"
        strat = cluster_strategies.get(c_name, {}).get('strategy', 'Field outreach.')
        prio = cluster_strategies.get(c_name, {}).get('priority', 'NORMAL')
        rows9.append([
            c_name, dist, cnt, pct, spec, coords, f"[{prio}] {strat}"
        ])
    style_table(ws9, headers9, rows9)

    # Save workbook
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    saved_paths = []
    
    # Try primary path
    try:
        wb.save(excel_path)
        saved_paths.append(excel_path)
    except PermissionError:
        print(f"Notice: '{excel_path}' is currently open in Microsoft Excel.")
        
    # Always save updated version as well so user can access it immediately
    base, ext = os.path.splitext(excel_path)
    updated_path = f"{base}_Updated{ext}"
    try:
        wb.save(updated_path)
        saved_paths.append(updated_path)
    except PermissionError:
        print(f"Notice: '{updated_path}' is also open in Microsoft Excel.")
        
    conn.close()
    print(f"Successfully generated 9-sheet Excel workbook at: {', '.join(saved_paths)}")
    return saved_paths[0] if saved_paths else updated_path

if __name__ == "__main__":
    export_to_excel()