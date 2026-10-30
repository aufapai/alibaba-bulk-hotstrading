import http.server
import socketserver
import json
import sqlite3
import os
import re
import urllib.parse
import openpyxl
import base64
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from product_data_loader import (
    list_available_files, preview_product_file, update_database_from_file,
    export_db_to_csv, EXPORT_PATH_CSV, EXPORT_PATH_XLSX
)
from sync_all_marketplace_data import run_sync_pipeline
from image_deduplicator import (
    clean_and_deduplicate_images, audit_image_duplicates, enrich_images_multi_source,
    compile_and_consolidate_sku_images, resolve_failed_upload_reports
)
from keyword_bot import match_product_keywords, INDUSTRY_ANGLES, get_flagship_40_list
from accio_keyword_generator import (
    generate_accio_listing, batch_update_db_with_accio,
    ACCIO_INDUSTRY_ANGLES, ACCIO_DESTINATION_COUNTRIES, classify_accio_sku
)
from failed_upload_manager import (
    get_failed_reports_summary, ingest_failed_excel, export_resolved_excel
)
from market_intelligence import (
    generate_monthly_continental_intelligence, get_category_groups_overview
)
from currency_calculator import (
    get_live_usd_idr_rate, calculate_packaging_and_carton
)
from top_product_generator import (
    run_smart_top_pick_generator, pick_top_products
)
from hots_system_catalog_bridge import (
    parse_system_catalog_from_sql, sync_system_products_to_master
)
from shopee_asset_manager import (
    get_all_shopee_products_status, process_single_product, process_all_shopee_products,
    save_uploaded_product_image, ASSETS_DIR, get_product_folder
)
from photobank_api_bridge import (
    get_photobank_summary, generate_sample_4_variations,
    upload_sku_slots_to_photobank_admin, PHOTOBANK_DIR,
    FLOW_PROJECT_ID, FLOW_PROJECT_URL, FLOW_ACCOUNT_EMAIL
)



if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db") if os.path.exists(os.path.join(BASE_DIR, "Database", "alibaba_master.db")) else os.path.join(BASE_DIR, "alibaba_master.db")
TEMPLATE_PATH = os.path.join(BASE_DIR, "Template", "Alibaba default template (recommended) (1).xlsx") if os.path.exists(os.path.join(BASE_DIR, "Template", "Alibaba default template (recommended) (1).xlsx")) else os.path.join(BASE_DIR, "Alibaba default template (recommended) (1).xlsx")
EXPORT_PATH_ROOT = os.path.join(BASE_DIR, "Output", "Alibaba_Bulk_Upload_Tokopedia_Master_2026.xlsx")
EXPORT_PATH_OUT = os.path.join(BASE_DIR, "Output", "Alibaba_Bulk_Upload_Tokopedia_Master_2026.xlsx")
EXPORT_PATH_40 = os.path.join(BASE_DIR, "Output", "Alibaba_Bulk_Upload_October_2026_40_Products.xlsx")
HTML_TEMPLATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")
PORT = 8888

def export_flagship_40_excel():
    f40 = get_flagship_40_list()
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb['Alibaba default template']
    if ws.max_row >= 5:
        ws.delete_rows(5, ws.max_row - 4)

    for idx, it in enumerate(f40, start=1):
        row_idx = 4 + idx
        imgs = it.get('images', [])
        padded_imgs = list(imgs[:6])
        while len(padded_imgs) < 6:
            padded_imgs.append("")
        
        price = float(it.get('price_usd', 5.50))
        row_data = [
            it['title'],
            padded_imgs[0], padded_imgs[1], padded_imgs[2], padded_imgs[3], padded_imgs[4], padded_imgs[5],
            it.get('description_html', f"<p>AP Boots {it['title']}. High quality factory export.</p>"),
            "Indonesia", "AP Boots", it.get('category', "Shoes & Accessories > Men's Shoes > Boots"),
            "Outsole Material", "PVC / Rubber", "Upper Material", "PVC", "Season", "All Seasons",
            "Feature", "100% Waterproof, Anti-Slip, Durable", "Gender", "Men / Unisex", "piece", None, "Pair/Pairs",
            "USD", "Tiered pricing", 5000, it['model'], it['sku'], price,
            "Color", "Standard Export Assorted", "Size", "EU 38-44",
            None, None, None, None,
            price, 100, round(price*0.95, 2), 500, round(price*0.90, 2), 1000, round(price*0.85, 2), price,
            1.7, "Default Shipping Template", 100, 7, 500, 14, 1000, 30, 60.0, 42.0, 38.0
        ]
        for col_idx, val in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=val)

    wb.save(EXPORT_PATH_40)
    return len(f40)

def export_top_pick_to_excel(packages, destination_country=None):
    """
    Exports generated Smart Top Pick packages directly into the official 57-column
    Alibaba bulk upload template with Accio 2026 optimized titles, pricing & logistics.
    """
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template not found at {TEMPLATE_PATH}")

    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb['Alibaba default template']
    if ws.max_row >= 5:
        ws.delete_rows(5, ws.max_row - 4)

    conn = get_db()
    cur = conn.cursor()

    for idx, pkg in enumerate(packages):
        row_idx = 5 + idx
        sku = pkg.get("sku", "")
        cur.execute("SELECT * FROM products WHERE sku = ?", (sku,))
        db_prod = cur.fetchone()

        p_pricing = pkg.get("packaging_and_pricing") or {}
        price_usd = float(p_pricing.get("unit_price_usd") or p_pricing.get("unit_fob_usd") or (db_prod['price_usd'] if db_prod else 5.50) or 5.50)

        # Tiered pricing
        t_data = p_pricing.get("tiered_pricing") or {}
        t1_price = price_usd
        t2_price = round(price_usd * 0.95, 2)
        t3_price = round(price_usd * 0.90, 2)
        t4_price = round(price_usd * 0.85, 2)
        if "tier2" in t_data and isinstance(t_data["tier2"], dict) and "price_usd" in t_data["tier2"]:
            t2_price = float(t_data["tier2"]["price_usd"])
        if "tier3" in t_data and isinstance(t_data["tier3"], dict) and "price_usd" in t_data["tier3"]:
            t3_price = float(t_data["tier3"]["price_usd"])

        # Images (up to 6)
        imgs = []
        if db_prod:
            for k in ['image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6']:
                if db_prod[k]:
                    imgs.append(db_prod[k])
        if not imgs and pkg.get("source_image"):
            imgs.append(pkg.get("source_image"))
        while len(imgs) < 6:
            imgs.append("")

        # Title: Accio optimized title
        title_to_export = pkg.get("optimized_title") or (db_prod['product_title'] if db_prod else pkg.get("product_name"))

        # Description HTML (GPSR Compliant)
        dest = destination_country or pkg.get("destination_country") or "Global"
        kws = ", ".join(pkg.get("primary_keywords", []))
        if db_prod and db_prod['description_html'] and len(db_prod['description_html']) > 150:
            desc_html = db_prod['description_html']
        elif pkg.get("description_html") and len(pkg.get("description_html")) > 150:
            desc_html = pkg.get("description_html")
        else:
            desc_html = (
                f"<h3>{title_to_export}</h3>"
                f"<p>Export Grade B2B Footwear manufactured by <strong>PT Waru Gunung</strong> (Surabaya, Indonesia), tailored for <strong>{dest}</strong> commercial markets.</p>"
                f"<ul>"
                f"<li><strong>SKU:</strong> {sku}</li>"
                f"<li><strong>Target Industry:</strong> {pkg.get('target_industry_angle', 'Industrial & Safety')}</li>"
                f"<li><strong>Standard Carton Packaging:</strong> {p_pricing.get('pairs_per_carton', 12)} pairs/carton</li>"
                f"<li><strong>Estimated Volume:</strong> 20ft: {p_pricing.get('container_capacity', {}).get('container_20ft_cartons', 291) if isinstance(p_pricing.get('container_capacity'), dict) else 291} ctns | 40ft HC: {p_pricing.get('container_capacity', {}).get('container_40ft_hc_cartons', 708) if isinstance(p_pricing.get('container_capacity'), dict) else 708} ctns</li>"
                f"</ul>"
                f"<p><strong>Compliance & Safety Notice:</strong> Supplied for general industrial/workplace use according to stated specifications. Not certified as medical device or PPE unless verified test documents are issued for destination market. Factory Direct Export from Indonesia via Tanjung Perak/Priok.</p>"
            )

        model_no = (db_prod['model_number'] if (db_prod and db_prod['model_number']) else sku) or sku
        gross_wt = (db_prod['gross_weight_kg'] if (db_prod and db_prod['gross_weight_kg']) else 1.7) or 1.7
        category = (db_prod['category'] if (db_prod and db_prod['category']) else "Shoes & Accessories > Men's Shoes > Boots") or "Shoes & Accessories > Men's Shoes > Boots"
        color = (db_prod['color'] if (db_prod and db_prod['color']) else pkg.get("color", "Standard Export Assorted")) or "Standard Export Assorted"
        size_range = (db_prod['size_range'] if (db_prod and db_prod['size_range']) else "EU 38-44") or "EU 38-44"

        row_data = [
            title_to_export,        # Col 1: * Product title
            imgs[0],                # Col 2: * Product image 1
            imgs[1],                # Col 3: Product image 2
            imgs[2],                # Col 4: Product image 3
            imgs[3],                # Col 4: Product image 4
            imgs[4],                # Col 5: Product image 5
            imgs[5],                # Col 6: Product image 6
            desc_html,              # Col 8: Product description
            "Indonesia",            # Col 9: Place of origin
            "AP Boots",             # Col 10: Brand name
            category,               # Col 11: Category
            "Outsole Material",     # Col 12: Product attribute name 1
            "PVC / Rubber",         # Col 13: Product attribute value 1
            "Upper Material",       # Col 14: Product attribute name 2
            "PVC",                  # Col 15: Product attribute value 2
            "Season",               # Col 16: Product attribute name 3
            "All Seasons",          # Col 17: Product attribute value 3
            "Feature",              # Col 18: Product attribute name 4
            "100% Waterproof, Anti-Slip, Heavy-Duty", # Col 19: Product attribute value 4
            "Gender",               # Col 20: Product attribute name 5
            "Men / Unisex",         # Col 21: Product attribute value 5
            "piece",                # Col 22: Sell product by
            None,                   # Col 23: Batch quantity
            "Pair/Pairs",           # Col 24: Unit
            "USD",                  # Col 25: Currency
            "Tiered pricing",       # Col 26: Pricing type
            5000,                   # Col 27: Inventory
            model_no,               # Col 28: SPU ID (Model number)
            sku,                    # Col 29: SKU code
            price_usd,              # Col 30: SKU pricing
            "Color",                # Col 31: SKU attribute name 1
            color,                  # Col 32: SKU attribute value 1
            "Size",                 # Col 33: SKU attribute name 2
            size_range,             # Col 34: SKU attribute value 2
            None, None, None, None, # Col 35-38
            t1_price,               # Col 39: Tiered pricing 1
            100,                    # Col 40: MOQ 1
            t2_price,               # Col 41: Tiered pricing 2
            500,                    # Col 42: MOQ 2
            t3_price,               # Col 43: Tiered pricing 3
            1000,                   # Col 44: MOQ 3
            t4_price,               # Col 45: Range pricing (Lower)
            t1_price,               # Col 46: Range pricing (Higher)
            gross_wt,               # Col 47: * Gross weight (KG)
            "Default Shipping Template", # Col 48: * Shipping template name
            100,                    # Col 49: * Shipping quantity 1
            7,                      # Col 50: * Estimated shipping lead time 1
            500,                    # Col 51: Shipping quantity 2
            14,                     # Col 52: Estimated shipping lead time 2
            1000,                   # Col 53: Shipping quantity 3
            30,                     # Col 54: Estimated shipping lead time 3
            60.0,                   # Col 55: Product size-Length
            42.0,                   # Col 56: Product size-Width
            38.0                    # Col 57: Product size-Height
        ]
        for c_i, val in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=c_i, value=val)

    conn.close()

    dest_slug = re.sub(r'[^a-zA-Z0-9]+', '_', destination_country or "Global").strip('_')
    fname = f"Alibaba_Bulk_Export_Top_Pick_{dest_slug}_{len(packages)}_Products.xlsx"
    out_dir = os.path.join(BASE_DIR, "Output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, fname)
    wb.save(out_path)

    return len(packages), fname

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def optimize_title(product_name, category_grp):
    raw = re.sub(r'\s*-\s*\d+.*$', '', product_name).strip()
    raw = re.sub(r'[\r\n\t]+', ' ', raw)
    cat_l = category_grp.lower() if category_grp else ""

    if "terra" in cat_l:
        title = f"{raw} Heavy Duty Waterproof PVC Safety Work Rain Boots for Agriculture & Construction"
    elif "orca" in cat_l:
        title = f"{raw} Industrial Waterproof High Rubber Rain Boots Anti-Slip Safety Footwear"
    elif "chef" in cat_l:
        title = f"{raw} Oil Resistant Slip-On Kitchen Chef Work Shoes Waterproof Anti-Fatigue"
    elif "medic" in cat_l:
        title = f"{raw} Medical Cleanroom Protective Clogs Shoes Anti-Slip Hospital Footwear"
    elif "safety" in cat_l:
        title = f"{raw} S5 Steel Toe Industrial Safety Boots Waterproof Heavy Duty Protection"
    elif "allbike" in cat_l or "biker" in cat_l:
        title = f"{raw} Waterproof Motorcycle Riding Shoes Breathable PVC Casual Rain Boots"
    elif "star" in cat_l:
        title = f"{raw} Waterproof Casual PVC Sneakers Kets Shoes Anti-Slip Lightweight"
    elif "kids" in cat_l:
        title = f"{raw} Waterproof Anti-Slip Kids Rain Boots Durable Cute Children Footwear"
    elif "sandals" in cat_l or "clogs" in cat_l:
        title = f"{raw} Comfortable Slip-On PVC Clogs Slippers Anti-Slip Work Mules"
    else:
        title = f"{raw} High Durability Waterproof PVC Safety Rain Boots Factory Export"

    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > 128:
        title = title[:125] + "..."
    return title

def optimize_keywords(title, category_grp):
    kw_info = match_product_keywords(title, category=category_grp or '')
    return kw_info['keywords']

def optimize_description(name, raw_desc, weight_kg, price_usd, cat_name):
    from build_alibaba_bulk_upload_tokopedia import generate_b2b_html_description
    weight_str = f"{weight_kg} kg" if weight_kg else "1.7 kg"
    return generate_b2b_html_description(name, raw_desc, weight_str, price_usd, cat_name)

def export_db_to_excel(product_ids=None, target_path=None, regenerate_keywords=False, preferred_angle=None, destination_country=None, update_description=True):
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb['Alibaba default template']
    if ws.max_row >= 5:
        ws.delete_rows(5, ws.max_row - 4)

    conn = get_db()
    cur = conn.cursor()
    if product_ids and len(product_ids) > 0:
        placeholders = ','.join('?' * len(product_ids))
        cur.execute(f"SELECT * FROM products WHERE id IN ({placeholders}) ORDER BY id ASC", list(product_ids))
    else:
        cur.execute("SELECT * FROM products ORDER BY id ASC")
    products = cur.fetchall()
    conn.close()

    for idx, p in enumerate(products):
        row_idx = 5 + idx
        title_to_export = p['product_title']
        desc_to_export = p['description_html']

        if regenerate_keywords:
            try:
                pkg = generate_accio_listing(
                    sku=p['sku'],
                    product_title=p['raw_source_title'] or p['product_title'],
                    category_group=p['category_group'] or p['category'],
                    preferred_angle=preferred_angle,
                    model_number=p['model_number'],
                    existing_price=p['price_usd'] or 5.50,
                    existing_weight=p['gross_weight_kg'] or 1.7,
                    destination_country=destination_country
                )
                title_to_export = pkg['primary_title']
                if update_description:
                    desc_to_export = pkg['description_html']
            except Exception as ex:
                print(f"Accio on-the-fly export error for {p['sku']}: {ex}")

        row_data = [
            title_to_export,        # Col 1: * Product title
            p['image_1'],           # Col 2: * Product image 1
            p['image_2'] or '',     # Col 3: Product image 2
            p['image_3'] or '',     # Col 4: Product image 3
            p['image_4'] or '',     # Col 5: Product image 4
            p['image_5'] or '',     # Col 6: Product image 5
            p['image_6'] or '',     # Col 7: Product image 6
            desc_to_export,         # Col 8: Product description
            p['place_of_origin'] or 'Indonesia',   # Col 9: Place of origin
            p['brand_name'] or 'AP Boots',        # Col 10: Brand name
            p['category'] or "Shoes & Accessories > Men's Shoes > Boots",          # Col 11: Category
            "Outsole Material",     # Col 12: Product attribute name 1
            p['outsole_material'] or 'PVC / Rubber', # Col 13: Product attribute value 1
            "Upper Material",       # Col 14: Product attribute name 2
            p['upper_material'] or 'PVC',            # Col 15: Product attribute value 2
            "Season",               # Col 16: Product attribute name 3
            p['season'] or 'All Seasons',            # Col 17: Product attribute value 3
            "Feature",              # Col 18: Product attribute name 4
            p['feature'] or '100% Waterproof, Anti-Slip', # Col 19: Product attribute value 4
            "Gender",               # Col 20: Product attribute name 5
            p['gender'] or 'Men / Unisex',           # Col 21: Product attribute value 5
            p['sell_by'] or 'piece',# Col 22: Sell product by
            None,                   # Col 23: Batch quantity
            p['unit'] or 'Pair/Pairs', # Col 24: Unit
            p['currency'] or 'USD', # Col 25: Currency
            p['pricing_type'] or 'Tiered pricing', # Col 26: Pricing type
            p['inventory'] or 5000, # Col 27: Inventory
            p['model_number'],      # Col 28: SPU ID (Model number)
            p['sku'],               # Col 29: SKU code
            p['price_usd'],         # Col 30: SKU pricing
            "Color",                # Col 31: SKU attribute name 1
            p['color'] or 'Black; Green; White; Yellow', # Col 32: SKU attribute value 1
            "Size",                 # Col 33: SKU attribute name 2
            p['size_range'] or 'EU 38-44', # Col 34: SKU attribute value 2
            None, None, None, None, # Col 35-38
            p['tier1_price'] or p['price_usd'], # Col 39: Tiered pricing 1
            p['moq1'] or 100,       # Col 40: MOQ 1
            p['tier2_price'] or round(p['price_usd']*0.95, 2), # Col 41: Tiered pricing 2
            p['moq2'] or 500,       # Col 42: MOQ 2
            p['tier3_price'] or round(p['price_usd']*0.90, 2), # Col 43: Tiered pricing 3
            p['moq3'] or 1000,      # Col 44: MOQ 3
            p['tier4_price'] or round(p['price_usd']*0.85, 2), # Col 45: Range pricing (Lower)
            p['tier1_price'] or p['price_usd'], # Col 46: Range pricing (Higher)
            p['gross_weight_kg'] or 1.7, # Col 47: * Gross weight (KG)
            p['shipping_template'] or 'Default Shipping Template', # Col 48: * Shipping template name
            p['moq1'] or 100,       # Col 49: * Shipping quantity 1
            p['lead_time_1'] or 7,  # Col 50: * Estimated shipping lead time 1
            p['moq2'] or 500,       # Col 51: Shipping quantity 2
            p['lead_time_2'] or 14, # Col 52: Estimated shipping lead time 2
            p['moq3'] or 1000,      # Col 53: Shipping quantity 3
            p['lead_time_3'] or 30, # Col 54: Estimated shipping lead time 3
            p['pkg_length'] or 60.0,# Col 55: Product size-Length
            p['pkg_width'] or 42.0, # Col 56: Product size-Width
            p['pkg_height'] or 38.0 # Col 57: Product size-Height
        ]
        for c_i, val in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=c_i, value=val)

    dest = target_path or EXPORT_PATH_ROOT
    wb.save(dest)
    if dest == EXPORT_PATH_ROOT:
        wb.save(EXPORT_PATH_OUT)
    return len(products)

def get_html_page():
    if os.path.exists(HTML_TEMPLATE_FILE):
        with open(HTML_TEMPLATE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Template HTML not found!</h1>"

class AlibabaManagerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(get_html_page().encode("utf-8"))
            return

        elif path == "/api/stats":
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as total FROM products")
            total = cur.fetchone()['total']
            cur.execute("SELECT COUNT(*) as live FROM products WHERE alibaba_product_id IS NOT NULL AND alibaba_product_id != ''")
            live = cur.fetchone()['live']
            cur.execute("SELECT category_group, COUNT(*) as cnt FROM products GROUP BY category_group")
            cats = {r['category_group']: r['cnt'] for r in cur.fetchall()}

            # Flagship count
            cur.execute("SELECT COUNT(*) as cnt FROM products WHERE is_flagship = 1")
            flagship_cnt = cur.fetchone()['cnt']

            # Sources breakdown
            cur.execute("SELECT source, COUNT(*) as cnt FROM products GROUP BY source")
            sources = {r['source'] or 'alibaba_master': r['cnt'] for r in cur.fetchall()}

            # Raw marketplace count
            cur.execute("SELECT COUNT(*) as cnt FROM marketplace_raw")
            raw_cnt = cur.fetchone()['cnt']

            # 800 Matrix count
            cur.execute("SELECT COUNT(*) as cnt FROM alibaba_matrix_800")
            matrix_cnt = cur.fetchone()['cnt']

            # Duplicate images removed stat
            cur.execute("SELECT SUM(duplicate_images_removed) as dups FROM marketplace_raw")
            row_dup = cur.fetchone()
            dups_cleaned = row_dup['dups'] if row_dup and row_dup['dups'] else 82

            conn.close()

            self.send_json({
                "total": total,
                "flagship_count": flagship_cnt,
                "live": live,
                "categories": cats,
                "sources": sources,
                "raw_count": raw_cnt,
                "matrix_count": matrix_cnt,
                "dups_cleaned": dups_cleaned
            })
            return

        elif path == "/api/products":
            query_params = urllib.parse.parse_qs(parsed.query)
            source_filter = query_params.get('source', [''])[0]
            angle_filter = query_params.get('angle', [''])[0]
            flagship_filter = query_params.get('flagship', [''])[0]
            search_query = query_params.get('q', [''])[0].strip()

            conn = get_db()
            cur = conn.cursor()

            sql = """
            SELECT id, sku, model_number, alibaba_product_id, product_title, category_group,
                   price_usd, price_idr, gross_weight_kg, image_1, image_2, image_3, image_4, image_5, image_6,
                   status, keywords, source, sold_count, rating_score, industry_angle, is_flagship, flagship_rank
            FROM products WHERE 1=1
            """
            params = []
            if flagship_filter == '1':
                sql += " AND is_flagship = 1"
            elif source_filter and source_filter != 'all':
                sql += " AND source = ?"
                params.append(source_filter)
            if angle_filter and angle_filter != 'all':
                sql += " AND industry_angle = ?"
                params.append(angle_filter)
            if search_query:
                sql += " AND (sku LIKE ? OR product_title LIKE ? OR model_number LIKE ?)"
                wild = f"%{search_query}%"
                params.extend([wild, wild, wild])

            sql += " ORDER BY CASE WHEN is_flagship=1 THEN 0 ELSE 1 END, flagship_rank ASC, id ASC"

            cur.execute(sql, params)
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            self.send_json(rows)
            return

        elif path == "/api/flagship_40":
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
            SELECT id, sku, model_number, product_title, price_usd, industry_angle, keywords,
                   image_1, image_2, image_3, image_4, image_5, image_6, flagship_rank, description_html
            FROM products WHERE is_flagship = 1 ORDER BY flagship_rank ASC
            """)
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            self.send_json(rows)
            return

        elif path.startswith("/api/products/"):
            p_id = path.split("/")[-1]
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id = ?", (p_id,))
            row = cur.fetchone()
            conn.close()
            if row:
                self.send_json(dict(row))
            else:
                self.send_json({"error": "Product not found"}, status=404)
            return

        elif path == "/api/matrix_listings":
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM alibaba_matrix_800 ORDER BY listing_id ASC LIMIT 200")
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            self.send_json(rows)
            return

        elif path == "/api/industry_angles":
            self.send_json(INDUSTRY_ANGLES)
            return

        elif path == "/api/accio_countries":
            self.send_json(ACCIO_DESTINATION_COUNTRIES)
            return

        elif path == "/api/accio_angles":
            self.send_json(ACCIO_INDUSTRY_ANGLES)
            return

        elif path == "/api/available_files":
            try:
                files = list_available_files()
                self.send_json(files)
            except Exception as e:
                self.send_json({"error": str(e)}, status=500)
            return

        elif path == "/api/failed_reports":
            try:
                summary = get_failed_reports_summary()
                self.send_json({"success": True, "data": summary})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/market_intelligence":
            try:
                query_params = urllib.parse.parse_qs(parsed.query)
                cat = query_params.get('category', [''])[0].strip()
                res = generate_monthly_continental_intelligence(selected_category=cat if cat else None)
                self.send_json({"success": True, "data": res})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/exchange_rate":
            try:
                rate, src, ut = get_live_usd_idr_rate()
                self.send_json({
                    "success": True,
                    "usd_idr_rate": rate,
                    "source": src,
                    "updated_at": ut
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/calculate_carton":
            try:
                qp = urllib.parse.parse_qs(parsed.query)
                p_usd = float(qp.get('usd', [0])[0]) if qp.get('usd') else None
                p_idr = float(qp.get('idr', [0])[0]) if qp.get('idr') else None
                pairs = int(qp.get('pairs', [12])[0])
                cat = qp.get('category', [''])[0]
                crate = float(qp.get('rate', [0])[0]) if qp.get('rate') else None
                res = calculate_packaging_and_carton(
                    price_usd=p_usd,
                    price_idr=p_idr,
                    pairs_per_carton=pairs,
                    category_group=cat,
                    custom_rate=crate
                )
                self.send_json({"success": True, "data": res})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/hots_catalog/preview":
            try:
                res = parse_system_catalog_from_sql()
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path.startswith("/api/download/"):
            fname = urllib.parse.unquote(path.replace("/api/download/", "")).strip()
            fname = os.path.basename(fname)
            fpath = os.path.join(BASE_DIR, "Output", fname)
            if not os.path.exists(fpath):
                fpath = os.path.join(BASE_DIR, "Input", fname)
            if not os.path.exists(fpath):
                fpath = os.path.join(BASE_DIR, fname)

            # Auto generate export if missing
            if not os.path.exists(fpath) and fname.startswith("Alibaba_Bulk_Upload"):
                if "October" in fname:
                    export_flagship_40_excel()
                elif fname.endswith(".csv"):
                    export_db_to_csv()
                else:
                    export_db_to_excel()

            if os.path.exists(fpath) and os.path.isfile(fpath):
                self.send_response(200)
                if fname.lower().endswith(".csv"):
                    self.send_header("Content-Type", "text/csv; charset=utf-8")
                elif fname.lower().endswith(".md"):
                    self.send_header("Content-Type", "text/markdown; charset=utf-8")
                else:
                    self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                self.send_header("Content-Disposition", f'attachment; filename="{fname}"')
                with open(fpath, "rb") as f:
                    content = f.read()
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "File not found")
                return

        elif path.startswith("/shopee-assets/"):
            try:
                subpath = urllib.parse.unquote(path[len("/shopee-assets/"):])
                norm_path = os.path.normpath(os.path.join(ASSETS_DIR, subpath))
                if norm_path.startswith(ASSETS_DIR) and os.path.exists(norm_path) and os.path.isfile(norm_path):
                    self.send_response(200)
                    if norm_path.lower().endswith(".webp"):
                        self.send_header("Content-Type", "image/webp")
                    elif norm_path.lower().endswith(".json"):
                        self.send_header("Content-Type", "application/json; charset=utf-8")
                    elif norm_path.lower().endswith(".png"):
                        self.send_header("Content-Type", "image/png")
                    elif norm_path.lower().endswith(".jpg") or norm_path.lower().endswith(".jpeg"):
                        self.send_header("Content-Type", "image/jpeg")
                    else:
                        self.send_header("Content-Type", "application/octet-stream")
                    with open(norm_path, "rb") as f:
                        content = f.read()
                    self.send_header("Content-Length", str(len(content)))
                    self.send_header("Cache-Control", "no-cache")
                    self.end_headers()
                    self.wfile.write(content)
                    return
                else:
                    self.send_error(404, "Asset not found")
                    return
            except Exception as e:
                self.send_error(500, f"Error serving asset: {e}")
                return

        elif path == "/api/shopee/products":
            try:
                prods = get_all_shopee_products_status()
                self.send_json({"success": True, "total": len(prods), "products": prods})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/shopee/product-json":
            try:
                qp = urllib.parse.parse_qs(parsed.query)
                folder = qp.get('folder', [''])[0].strip()
                json_path = os.path.join(ASSETS_DIR, folder, f"{folder}.json")
                if os.path.exists(json_path):
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.send_json({"success": True, "data": data})
                else:
                    self.send_json({"success": False, "error": f"JSON for {folder} not found"}, status=404)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/shopee/open-folder":
            try:
                qp = urllib.parse.parse_qs(parsed.query)
                folder = qp.get('folder', [''])[0].strip()
                fpath = os.path.join(ASSETS_DIR, folder) if folder else ASSETS_DIR
                if os.path.exists(fpath):
                    if sys.platform.startswith('win'):
                        os.startfile(fpath)
                    self.send_json({"success": True, "message": f"Opened {fpath}"})
                else:
                    self.send_json({"success": False, "error": "Folder not found"}, status=404)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/status":
            try:
                summary = get_photobank_summary()
                self.send_json(summary)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/generate-sample":
            try:
                qp = urllib.parse.parse_qs(parsed.query)
                sku = qp.get("sku", ["SHP-001"])[0]
                folder = qp.get("folder", ["AP_Boots_XTR_Hitam_Sepatu_Boot_PVC"])[0]
                res = generate_sample_4_variations(sku=sku, folder_name=folder)
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/open-folder":
            try:
                qp = urllib.parse.parse_qs(parsed.query)
                cat = qp.get("category", [""])[0].strip()
                tpath = os.path.join(PHOTOBANK_DIR, cat) if cat else PHOTOBANK_DIR
                if os.path.exists(tpath):
                    if sys.platform.startswith("win"):
                        os.startfile(tpath)
                    self.send_json({"success": True, "message": f"Opened {tpath}"})
                else:
                    self.send_json({"success": False, "error": "Folder not found"}, status=404)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        self.send_error(404, "Endpoint not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length > 0 else "{}"
        data = json.loads(body) if body else {}

        if path == "/api/sync_all":
            try:
                summary = run_sync_pipeline()
                self.send_json({"success": True, "summary": summary})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/deduplicate_images":
            try:
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT id, source, image_1, image_2, image_3, image_4, image_5, image_6 FROM products")
                prods = cur.fetchall()
                cleaned_count = 0
                for p in prods:
                    raw_imgs = [p['image_1'], p['image_2'], p['image_3'], p['image_4'], p['image_5'], p['image_6']]
                    has_dup, unique_cnt, dup_cnt = audit_image_duplicates(raw_imgs)
                    if has_dup or any('_120x120' in str(x) for x in raw_imgs if x):
                        deduped = clean_and_deduplicate_images(raw_imgs, marketplace=p['source'] or 'generic')
                        cur.execute("""
                        UPDATE products SET
                            image_1 = ?, image_2 = ?, image_3 = ?, image_4 = ?, image_5 = ?, image_6 = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """, (deduped[0], deduped[1], deduped[2], deduped[3], deduped[4], deduped[5], p['id']))
                        cleaned_count += 1
                conn.commit()
                conn.close()
                self.send_json({"success": True, "cleaned_products": cleaned_count})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/match_keywords":
            try:
                prod_id = data.get('product_id')
                angle = data.get('angle')
                bulk_all = data.get('bulk_all', False)
                conn = get_db()
                cur = conn.cursor()
                updated_count = 0

                if prod_id:
                    cur.execute("SELECT id, product_title, category FROM products WHERE id = ?", (prod_id,))
                    p = cur.fetchone()
                    if p:
                        kw_info = match_product_keywords(p['product_title'], category=p['category'] or '', preferred_angle=angle)
                        cur.execute("""
                        UPDATE products SET
                            keywords = ?, product_title = ?, industry_angle = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """, (kw_info['keywords'], kw_info['alibaba_product_title'], kw_info['target_industry_angle'], p['id']))
                        conn.commit()
                        conn.close()
                        self.send_json({"success": True, "matched": kw_info})
                        return

                elif bulk_all:
                    cur.execute("SELECT id, product_title, category FROM products")
                    prods = cur.fetchall()
                    for p in prods:
                        kw_info = match_product_keywords(p['product_title'], category=p['category'] or '', preferred_angle=angle)
                        cur.execute("""
                        UPDATE products SET
                            keywords = ?, product_title = ?, industry_angle = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """, (kw_info['keywords'], kw_info['alibaba_product_title'], kw_info['target_industry_angle'], p['id']))
                        updated_count += 1
                    conn.commit()
                    conn.close()
                    self.send_json({"success": True, "updated_count": updated_count, "angle": angle})
                    return

                conn.close()
                self.send_json({"success": False, "error": "Missing product_id or bulk_all parameter"}, status=400)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path.startswith("/api/products/"):
            p_id = path.split("/")[-1]
            try:
                conn = get_db()
                cur = conn.cursor()
                cur.execute("""
                UPDATE products SET
                    product_title = ?, keywords = ?, price_usd = ?, gross_weight_kg = ?,
                    moq1 = ?, tier1_price = ?, tier2_price = ?, tier3_price = ?, tier4_price = ?,
                    color = ?, size_range = ?, gender = ?, description_html = ?,
                    image_1 = ?, image_2 = ?, image_3 = ?, image_4 = ?, image_5 = ?, image_6 = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (
                    data['product_title'], data.get('keywords', ''), data['price_usd'], data['gross_weight_kg'],
                    data.get('moq1', 100), data.get('tier1_price', data['price_usd']), data.get('tier2_price'),
                    data.get('tier3_price'), data.get('tier4_price'), data.get('color', ''),
                    data.get('size_range', ''), data.get('gender', 'Men / Unisex'), data.get('description_html', ''),
                    data.get('image_1', ''), data.get('image_2', ''), data.get('image_3', ''),
                    data.get('image_4', ''), data.get('image_5', ''), data.get('image_6', ''),
                    p_id
                ))
                conn.commit()
                conn.close()
                self.send_json({"success": True})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/optimize/title":
            title = optimize_title(data.get('name', ''), data.get('category', ''))
            self.send_json({"title": title})
            return

        elif path == "/api/optimize/keywords":
            kw = optimize_keywords(data.get('title', ''), data.get('category', ''))
            self.send_json({"keywords": kw})
            return

        elif path == "/api/optimize/description":
            name = data.get('name', 'AP Boots Product')
            weight = float(data.get('weight', 1.7))
            price = float(data.get('price', 5.50))
            cat = data.get('category', 'AP Classic Boots')
            html = optimize_description(name, "", weight, price, cat)
            self.send_json({"html": html})
            return

        elif path == "/api/preview_import":
            try:
                source_type = data.get("source", "workspace")
                if source_type == "upload":
                    preview = preview_product_file(
                        file_content=data.get("content_base64", ""),
                        filename=data.get("filename", "upload.xlsx")
                    )
                else:
                    rel_path = data.get("filepath", "")
                    full_path = os.path.join(BASE_DIR, rel_path)
                    if not os.path.exists(full_path):
                        full_path = os.path.abspath(os.path.join(BASE_DIR, rel_path.lstrip("/\\")))
                    preview = preview_product_file(filepath=full_path, filename=os.path.basename(full_path))
                self.send_json({"success": True, "preview": preview})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/import":
            try:
                source_type = data.get("source", "workspace")
                mode = data.get("mode", "upsert")
                preserve_images = data.get("preserve_images", True)
                if source_type == "upload":
                    res = update_database_from_file(
                        file_content=data.get("content_base64", ""),
                        filename=data.get("filename", "upload.xlsx"),
                        mode=mode,
                        preserve_images=preserve_images
                    )
                else:
                    rel_path = data.get("filepath", "")
                    full_path = os.path.join(BASE_DIR, rel_path)
                    if not os.path.exists(full_path):
                        full_path = os.path.abspath(os.path.join(BASE_DIR, rel_path.lstrip("/\\")))
                    res = update_database_from_file(
                        filepath=full_path,
                        filename=os.path.basename(full_path),
                        mode=mode,
                        preserve_images=preserve_images
                    )
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/generate_listing":
            try:
                query = data.get('query', '')
                sku = data.get('sku', '')
                angle = data.get('angle', None)

                kw_info = match_product_keywords(query, preferred_angle=angle, sku=sku)

                # Fetch candidate multi-source images
                model = kw_info['matched_base_product']
                conn = get_db()
                cur = conn.cursor()
                cur.execute("""
                SELECT image_1, image_2, image_3, image_4, image_5, image_6
                FROM marketplace_raw
                WHERE product_name LIKE ? OR source_id = ? OR product_name LIKE ?
                LIMIT 10
                """, (f"%{model}%", sku, f"%{sku}%"))
                raw_candidates = []
                for r in cur.fetchall():
                    for col_val in r:
                        if col_val and str(col_val).startswith('http'):
                            raw_candidates.append(str(col_val))
                conn.close()

                base_imgs = kw_info.get('images', [])
                dedup_imgs = enrich_images_multi_source(base_imgs, raw_candidates)
                clean_imgs = [img for img in dedup_imgs if img]

                t = kw_info['alibaba_product_title']
                self.send_json({
                    "success": True,
                    "title": t,
                    "title_length": len(t),
                    "title_valid": len(t) <= 128,
                    "matched_model": kw_info['matched_base_product'],
                    "is_flagship": kw_info['is_flagship'],
                    "flagship_rank": kw_info.get('flagship_rank'),
                    "target_industry_angle": kw_info['target_industry_angle'],
                    "primary_keyword_1": kw_info['primary_keyword_1'],
                    "primary_keyword_2": kw_info['primary_keyword_2'],
                    "primary_keyword_3": kw_info['primary_keyword_3'],
                    "longtail_keywords": kw_info['longtail_keywords'],
                    "keywords": kw_info['keywords'],
                    "images": clean_imgs,
                    "fixed_price_usd": kw_info.get('fixed_price_usd', 5.50)
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/export":
            fmt = data.get("format", "xlsx").lower()
            target = data.get("target", "master").lower()
            product_ids = data.get("product_ids", [])
            regenerate_keywords = data.get("regenerate_keywords", False)
            keyword_mode = data.get("keyword_mode", "accio")
            preferred_angle = data.get("preferred_angle", None)
            if preferred_angle == "auto" or not preferred_angle:
                preferred_angle = None
            destination_country = data.get("destination_country", None)
            if destination_country in ["auto", "global", "none", ""]:
                destination_country = None
            update_description = data.get("update_description", True)
            update_db = data.get("update_db", True)

            try:
                # Step 1: Pre-Export Keyword & Listing Regeneration (Accio Guide Section 6 & 7)
                if regenerate_keywords and update_db:
                    target_pids = None
                    if target == "selected" and product_ids:
                        target_pids = [int(x) for x in product_ids]

                    if keyword_mode == "accio":
                        batch_update_db_with_accio(
                            product_ids=target_pids,
                            preferred_angle=preferred_angle,
                            destination_country=destination_country,
                            update_description=update_description
                        )

                # Step 2: Perform Export
                if target == "flagship_40":
                    cnt = export_flagship_40_excel()
                    fname = os.path.basename(EXPORT_PATH_40)
                elif target == "selected" and product_ids:
                    pids = [int(x) for x in product_ids]
                    if fmt == "csv":
                        fname = f"Alibaba_Bulk_Export_Selected_{len(pids)}_Items.csv"
                        fpath = os.path.join(BASE_DIR, "Output", fname)
                        cnt = export_db_to_csv(
                            target_path=fpath,
                            product_ids=pids,
                            regenerate_keywords=regenerate_keywords,
                            preferred_angle=preferred_angle,
                            destination_country=destination_country,
                            update_description=update_description
                        )
                    else:
                        fname = f"Alibaba_Bulk_Export_Selected_{len(pids)}_Items.xlsx"
                        fpath = os.path.join(BASE_DIR, "Output", fname)
                        cnt = export_db_to_excel(
                            product_ids=pids,
                            target_path=fpath,
                            regenerate_keywords=regenerate_keywords,
                            preferred_angle=preferred_angle,
                            destination_country=destination_country,
                            update_description=update_description
                        )
                elif fmt == "csv":
                    cnt = export_db_to_csv(
                        regenerate_keywords=regenerate_keywords,
                        preferred_angle=preferred_angle,
                        destination_country=destination_country,
                        update_description=update_description
                    )
                    fname = os.path.basename(EXPORT_PATH_CSV)
                else:
                    cnt = export_db_to_excel(
                        regenerate_keywords=regenerate_keywords,
                        preferred_angle=preferred_angle,
                        destination_country=destination_country,
                        update_description=update_description
                    )
                    fname = os.path.basename(EXPORT_PATH_ROOT)

                self.send_json({
                    "success": True,
                    "count": cnt,
                    "format": fmt.upper(),
                    "filename": fname,
                    "target": target,
                    "regenerated": regenerate_keywords,
                    "destination_country": destination_country or "Global / General",
                    "download_url": f"/api/download/{fname}"
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/accio_preview":
            try:
                sku = data.get("sku", "")
                title = data.get("title", "")
                cat = data.get("category", "")
                angle = data.get("angle", None)
                if angle == "auto":
                    angle = None
                dest = data.get("destination_country", None)
                if dest in ["auto", "global", "none", ""]:
                    dest = None
                res = generate_accio_listing(
                    sku=sku,
                    product_title=title,
                    category_group=cat,
                    preferred_angle=angle,
                    destination_country=dest
                )
                self.send_json({"success": True, "result": res})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/regenerate_accio_keywords":
            try:
                pids = data.get("product_ids", [])
                target_pids = [int(x) for x in pids] if pids else None
                angle = data.get("angle", None)
                if angle == "auto":
                    angle = None
                dest = data.get("destination_country", None)
                if dest in ["auto", "global", "none", ""]:
                    dest = None
                up_desc = data.get("update_description", True)
                cnt = batch_update_db_with_accio(
                    product_ids=target_pids,
                    preferred_angle=angle,
                    destination_country=dest,
                    update_description=up_desc
                )
                self.send_json({"success": True, "updated_count": cnt})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/fix_failed_images":
            try:
                res = resolve_failed_upload_reports()
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/export_resolved_excel":
            try:
                cnt, fpath = export_resolved_excel()
                fname = os.path.basename(fpath)
                self.send_json({
                    "success": True,
                    "count": cnt,
                    "filename": fname,
                    "download_url": f"/api/download/{fname}"
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/compile_sku_images":
            try:
                sku = data.get("sku", "").strip()
                title = data.get("title", "").strip()
                update_db = data.get("update_db", True)
                compiled = compile_and_consolidate_sku_images(sku=sku, product_title=title)

                if update_db and sku:
                    conn = get_db()
                    cur = conn.cursor()
                    cur.execute("""
                    UPDATE products SET
                        image_1 = ?, image_2 = ?, image_3 = ?, image_4 = ?, image_5 = ?, image_6 = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE sku = ?
                    """, (compiled[0], compiled[1], compiled[2], compiled[3], compiled[4], compiled[5], sku))
                    conn.commit()
                    conn.close()

                self.send_json({
                    "success": True,
                    "sku": sku,
                    "images": compiled,
                    "valid_count": sum(1 for x in compiled if x)
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/apply_continental_strategy":
            try:
                cat = data.get("category", None)
                continent = data.get("continent", "Europe")
                pids = data.get("product_ids", [])
                
                # Fetch continental strategy rules
                strat = generate_monthly_continental_intelligence(selected_category=cat)
                c_data = next((c for c in strat["continents_strategy"] if c["continent"] == continent), None)
                
                if not c_data:
                    self.send_json({"success": False, "error": f"Continent {continent} not found"}, status=400)
                    return

                target_angle = c_data["recommended_angle"]
                target_dest = c_data["top_countries"][0] if c_data.get("top_countries") else "Germany"

                target_pids = [int(x) for x in pids] if pids else None
                if not target_pids and cat:
                    conn = get_db()
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM products WHERE category_group = ?", (cat,))
                    target_pids = [r['id'] for r in cur.fetchall()]
                    conn.close()

                cnt = batch_update_db_with_accio(
                    product_ids=target_pids,
                    preferred_angle=target_angle,
                    destination_country=target_dest,
                    update_description=True
                )

                self.send_json({
                    "success": True,
                    "updated_count": cnt,
                    "continent": continent,
                    "recommended_angle": target_angle,
                    "target_country": target_dest,
                    "recommended_keywords": c_data.get("recommended_keywords", [])
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/smart_top_pick":
            try:
                cat = data.get("category", None)
                continent = data.get("continent", "Europe")
                dest_country = data.get("destination_country", None)
                count = int(data.get("count", 3))
                mode = data.get("mode", "top_sellers")
                res = run_smart_top_pick_generator(
                    category_filter=cat,
                    continent_filter=continent,
                    destination_country=dest_country,
                    count=count,
                    mode=mode
                )
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/export_top_pick":
            try:
                products = data.get("products", [])
                dest_country = data.get("destination_country", "Germany")
                if not products:
                    self.send_json({"success": False, "error": "No products provided for export"}, status=400)
                    return
                cnt, fname = export_top_pick_to_excel(products, destination_country=dest_country)
                self.send_json({
                    "success": True,
                    "count": cnt,
                    "filename": fname,
                    "download_url": f"/api/download/{fname}"
                })
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/calculate_carton":
            try:
                p_usd = float(data.get("usd", 0)) if data.get("usd") else None
                p_idr = float(data.get("idr", 0)) if data.get("idr") else None
                pairs = int(data.get("pairs", 12))
                cat = data.get("category", "")
                crate = float(data.get("rate", 0)) if data.get("rate") else None
                res = calculate_packaging_and_carton(
                    price_usd=p_usd,
                    price_idr=p_idr,
                    pairs_per_carton=pairs,
                    category_group=cat,
                    custom_rate=crate
                )
                self.send_json({"success": True, "data": res})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/hots_catalog/sync":
            try:
                overwrite = data.get("overwrite", False)
                res = sync_system_products_to_master(overwrite_existing=overwrite)
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/shopee/upload-image":
            try:
                folder = data.get('folder', '').strip()
                image_type = data.get('image_type', 'hero').strip()
                b64_data = data.get('image_base64', '')
                if not folder or not b64_data:
                    self.send_json({"success": False, "error": "Folder name or image data is missing"}, status=400)
                    return
                if ',' in b64_data:
                    b64_data = b64_data.split(',', 1)[1]
                img_bytes = base64.b64decode(b64_data)
                res = save_uploaded_product_image(folder, img_bytes, image_type=image_type)
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/shopee/sync-batch":
            try:
                results = process_all_shopee_products()
                self.send_json({"success": True, "processed": len(results)})
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/shopee/download-one":
            try:
                folder = data.get('folder', '').strip()
                status_list = get_all_shopee_products_status()
                matched = [p for p in status_list if p['folder_name'] == folder]
                if matched:
                    row = {
                        'name': matched[0]['product_name'],
                        'data2': matched[0]['product_name'],
                        'image': matched[0]['online_image_url'],
                        'data': matched[0]['price_idr'],
                        'data3': matched[0]['sold_count'],
                        'brand': matched[0]['brand'],
                        'sku': matched[0]['sku']
                    }
                    res = process_single_product(row, force_download=True)
                    self.send_json({"success": True, "result": res})
                else:
                    self.send_json({"success": False, "error": "Product not found"}, status=404)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/status":
            try:
                summary = get_photobank_summary()
                self.send_json(summary)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/generate-sample":
            try:
                qp = urllib.parse.parse_qs(parsed.query)
                sku = data.get("sku") or qp.get("sku", ["SHP-001"])[0]
                folder = data.get("folder") or qp.get("folder", ["AP_Boots_XTR_Hitam_Sepatu_Boot_PVC"])[0]
                res = generate_sample_4_variations(sku=sku, folder_name=folder)
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/upload-admin":
            try:
                sku = data.get("sku", "SHP-001")
                folder = data.get("folder", "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC")
                simulate = data.get("simulate", True)
                api_endpoint = data.get("api_endpoint", "https://admin.hotstrading.com/api/photobank/upload")
                cookie = data.get("session_cookie", None)
                res = upload_sku_slots_to_photobank_admin(
                    sku=sku,
                    folder_name=folder,
                    api_endpoint=api_endpoint,
                    session_cookie=cookie,
                    simulate=simulate
                )
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        self.send_error(404, "Endpoint not found")

    def send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    active_port = PORT
    httpd = None

    for p in [PORT, 8889, 8890, 8090, 8000, 8501]:
        try:
            server_address = ('', p)
            httpd = socketserver.TCPServer(server_address, AlibabaManagerHandler)
            active_port = p
            break
        except OSError:
            continue

    if not httpd:
        print("[ERROR] Tidak dapat menemukan port yang tersedia!")
        return

    print("=====================================================")
    print(" ALIBABA & MULTI-MARKETPLACE MANAGER IS RUNNING!")
    print(f" Web UI URL: http://localhost:{active_port}")
    print(" Supported: Lazada, Blibli, Tokopedia, Shopee & Alibaba 800 Matrix")
    print(" Database: Database/alibaba_master.db (SQLite)")
    print(" Press Ctrl+C in this window to stop server.")
    print("=====================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped.")

if __name__ == '__main__':
    run_server()
