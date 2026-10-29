import openpyxl
import sqlite3
import csv
import os
import re

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
TEMPLATE_PATH = os.path.join(BASE_DIR, "Template", "Alibaba default template (recommended) (1).xlsx")
WEBP_MAPPING_CSV = os.path.join(BASE_DIR, "Output", "photobank_webp_mapping.csv")
SERVER_UPLOADED_CSV = os.path.join(BASE_DIR, "Input", "photobank_server_uploaded.csv")
TOKOPEDIA_MASTER_CSV = os.path.join(BASE_DIR, "Output", "Alibaba_Bulk_Upload_Tokopedia_Master_2026.csv")
OUTPUT_EXCEL = os.path.join(BASE_DIR, "Output", "Alibaba_Bulk_Upload_November_2026.xlsx")

def load_photobank_server_urls():
    url_map = {}
    if os.path.exists(SERVER_UPLOADED_CSV):
        with open(SERVER_UPLOADED_CSV, 'r', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                orig = r.get('Nama File Asli', '').strip()
                url = r.get('URL Gambar', '').strip()
                if orig and url:
                    url_map[orig] = url
    return url_map

def load_tokopedia_fallbacks():
    tokopedia_imgs = {}
    if os.path.exists(TOKOPEDIA_MASTER_CSV):
        with open(TOKOPEDIA_MASTER_CSV, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for r_idx, row in enumerate(reader):
                if r_idx < 7 or not row:
                    continue
                title = row[0]
                sku = row[28] if len(row) > 28 else ""
                imgs = [row[c] for c in range(1, 7) if len(row) > c and str(row[c]).startswith('http')]
                if sku:
                    tokopedia_imgs[sku] = imgs
                if title:
                    tokopedia_imgs[title] = imgs
    return tokopedia_imgs

def load_photobank_webps():
    if not os.path.exists(WEBP_MAPPING_CSV):
        print(f"[!] Warning: {WEBP_MAPPING_CSV} not found!")
        return []
    with open(WEBP_MAPPING_CSV, 'r', encoding='utf-8') as f:
        return [r['webp_filename'] for r in csv.DictReader(f)]

def get_best_webp_images(title, cat_grp, color, webp_list, server_url_map=None):
    """
    Menemukan WebP gambar photobank terbaik berdasarkan nama model AP Boots.
    """
    t_low = title.lower()
    matches = []

    # 1. Clogs & Sandal Selop
    if 'clogs' in t_low:
        if 'pink' in t_low or 'ladies' in t_low:
            matches += [w for w in webp_list if 'pink_slip' in w or 'clogs' in w]
        else:
            matches += [w for w in webp_list if 'clogs' in w]
    elif any(k in t_low for k in ['sandal', 'selop', 'sendal', '989', '991', '995', '999', '1001']):
        matches += [w for w in webp_list if 'sandal_&_shoes' in w or 'clogs' in w]

    # 2. Allbike & Biker
    elif 'allbike 2' in t_low:
        if 'orange' in t_low:
            matches += [w for w in webp_list if 'allbike_2_orange' in w or 'orange_riding' in w]
        else:
            matches += [w for w in webp_list if 'allbike_2' in w or 'motorcycle_riding' in w]
    elif 'allbike' in t_low:
        if 'orange' in t_low:
            matches += [w for w in webp_list if 'allbike_orange' in w or 'orange_riding' in w]
        else:
            matches += [w for w in webp_list if 'allbike' in w or 'motorcycle_riding' in w]

    # 3. Moto series
    elif 'moto' in t_low:
        if 'moto 1' in t_low:
            matches += [w for w in webp_list if 'ap_moto.' in w or 'ap_moto_specs' in w]
        elif 'moto 2' in t_low:
            matches += [w for w in webp_list if 'ap_moto_2' in w or 'ap_moto_(2)' in w]
        elif 'moto 3' in t_low:
            matches += [w for w in webp_list if 'ap_moto_3' in w]
        else:
            matches += [w for w in webp_list if 'moto' in w]

    # 4. Chef
    elif 'chef' in t_low:
        matches += [w for w in webp_list if 'chef' in w]

    # 5. Medic
    elif 'medic' in t_low:
        matches += [w for w in webp_list if 'medic' in w]

    # 6. Safety Boots & Metaguard & AP MAX
    elif 'metaguard' in t_low:
        matches += [w for w in webp_list if 'metaguard' in w]
    elif 'safety s5' in t_low or 's5' in t_low or 'max' in t_low:
        matches += [w for w in webp_list if 's5' in w or 'safety_boot' in w or 'protective_boot' in w]
    elif 'safety s4' in t_low or 's4' in t_low:
        matches += [w for w in webp_list if 'protective_boot' in w or 'safety_boot' in w]
    elif 'orca' in t_low:
        matches += [w for w in webp_list if 'orca' in w]

    # 7. Terra series
    elif 'terra gp' in t_low:
        matches += [w for w in webp_list if 'terra_gp' in w]
    elif 'terra eco 3' in t_low:
        matches += [w for w in webp_list if 'terra_eco_3' in w]
    elif 'terra eco' in t_low:
        matches += [w for w in webp_list if 'terra_eco' in w]
    elif 'terra 1' in t_low:
        if 'putih' in t_low or 'white' in t_low:
            matches += [w for w in webp_list if 'terra_1_putih' in w]
        else:
            matches += [w for w in webp_list if 'terra_1' in w]
    elif 'terra' in t_low:
        matches += [w for w in webp_list if 'terra' in w]

    # 8. Classic 2003, 2005, 2017, 9303, 9506, Hobby N Work
    elif '2003' in t_low:
        if 'tricolour' in t_low or 'triwarna' in t_low:
            matches += [w for w in webp_list if '2003_hijau_tricolour' in w or 'triwarna' in w]
        else:
            matches += [w for w in webp_list if '2003' in w]
    elif '2005' in t_low:
        matches += [w for w in webp_list if '2005' in w]
    elif '2017' in t_low:
        if 'lime' in t_low or 'green' in t_low:
            matches += [w for w in webp_list if '2017_green' in w or 'green_highlight' in w]
        else:
            matches += [w for w in webp_list if '2017_go_green' in w or 'green_series' in w]
    elif '9303' in t_low:
        matches += [w for w in webp_list if '9303' in w]
    elif '9506' in t_low:
        matches += [w for w in webp_list if '9506' in w]
    elif 'hobby' in t_low:
        matches += [w for w in webp_list if 'hobby' in w]

    # 9. Kids & Safari
    elif 'safari' in t_low:
        matches += [w for w in webp_list if 'safari' in w or 'kids' in w]
    elif 'kids' in t_low or 'anak' in t_low or '2001' in t_low or '2012' in t_low:
        matches += [w for w in webp_list if 'kids' in w]

    # 10. Star (Sneakers)
    elif 'star' in t_low:
        matches += [w for w in webp_list if 'start_series' in w or 'sneaker' in w]

    # 11. Bola Series (963, 967, 969)
    elif any(k in t_low for k in ['963', '967', '969', 'bola']):
        matches += [w for w in webp_list if 'bola_series' in w]

    # 12. General fallback for boots
    elif 'boot' in t_low:
        matches += [w for w in webp_list if 'boot_product' in w or 'boots_product' in w or 'green_boot' in w]

    # Remove duplicates while preserving order
    unique_matches = list(dict.fromkeys(matches))
    if server_url_map:
        return [server_url_map[w] for w in unique_matches if w in server_url_map]
    return [f"https://hotstrading.com/backend/uploads/{w}" for w in unique_matches]

def generate_b2b_export_keywords(title, cat_grp):
    """
    Menghasilkan 3 keyword B2B standar ekspor bahasa Inggris per produk
    sesuai pilihan User (Rekomendasi) untuk listing Alibaba.com.
    """
    cat_l = (cat_grp or "").lower()
    t_l = title.lower()

    if "safety" in cat_l or "s5" in t_l or "metaguard" in t_l or "max" in t_l:
        k1 = "steel toe safety boots"
        k2 = "s5 waterproof work boots"
        k3 = "chemical resistant industrial footwear"
    elif "orca" in cat_l or "orca" in t_l:
        k1 = "industrial rubber boots"
        k2 = "waterproof high safety boots"
        k3 = "heavy duty protective gumboots"
    elif "chef" in cat_l or "chef" in t_l:
        k1 = "slip resistant chef shoes"
        k2 = "kitchen work footwear"
        k3 = "waterproof food service clogs"
    elif "medic" in cat_l or "medic" in t_l:
        k1 = "medical safety clogs"
        k2 = "hospital cleanroom shoes"
        k3 = "anti slip nursing footwear"
    elif "allbike" in cat_l or "biker" in cat_l or "moto" in t_l or "riding" in t_l:
        k1 = "waterproof motorcycle riding shoes"
        k2 = "breathable pvc rain shoes"
        k3 = "casual outdoor commuter footwear"
    elif "terra" in cat_l or "terra" in t_l:
        k1 = "waterproof pvc rain boots"
        k2 = "heavy duty work gumboots"
        k3 = "agriculture plantation boots"
    elif "kids" in cat_l or "safari" in t_l or "2012" in t_l or "anak" in t_l:
        k1 = "kids waterproof rain boots"
        k2 = "anti slip children rubber boots"
        k3 = "durable cute toddler gumboots"
    elif "sandals" in cat_l or "clogs" in cat_l or "sandal" in t_l or "selop" in t_l:
        k1 = "comfortable slip on clogs"
        k2 = "waterproof garden slippers"
        k3 = "anti slip eva pvc slides"
    elif "sneakers" in cat_l or "star" in t_l:
        k1 = "casual waterproof sneakers"
        k2 = "pvc canvas style shoes"
        k3 = "daily lightweight rain footwear"
    elif any(k in t_l for k in ["bola", "963", "967", "969", "pantofel", "977"]):
        k1 = "waterproof molded cleat shoes"
        k2 = "durable pvc outdoor shoes"
        k3 = "slip resistant utility footwear"
    else:
        k1 = "waterproof pvc rain boots"
        k2 = "industrial protective footwear"
        k3 = "anti slip rubber work boots"

    return f"{k1}, {k2}, {k3}"

def is_valid_image(url):
    """
    Memastikan URL gambar valid dan bukan placeholder kosong.
    """
    if not url or not isinstance(url, str):
        return False
    u = url.strip()
    if not u.startswith("http"):
        return False
    # Check for empty placeholder hashes
    if "886938f2163140e3a9171a2481a51833" in u:
        return False
    # Check for unuploaded dummy photobank links (which return text/html 404)
    if "hotstrading.com/backend/uploads/" in u and "photobank/" not in u:
        return False
    return True

def main():
    print("=" * 70)
    print("      BUILDING ALIBABA NOVEMBER 2026 BULK UPLOAD BATCH")
    print("               PT Indo Sukses Semesta - AP Boots")
    print("=" * 70)

    server_url_map = load_photobank_server_urls()
    print(f"[*] Loaded {len(server_url_map)} uploaded Photobank server URLs.")

    tokopedia_fallbacks = load_tokopedia_fallbacks()
    print(f"[*] Loaded {len(tokopedia_fallbacks)} Tokopedia CDN fallback sets.")

    webp_list = load_photobank_webps()
    print(f"[*] Loaded {len(webp_list)} WebP images from photobank mapping.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM products ORDER BY id ASC")
    products = [dict(row) for row in cur.fetchall()]
    print(f"[*] Retrieved {len(products)} products from alibaba_master.db.")

    # 1. Update image links and keywords for each product
    valid_batch_products = []
    photobank_upgrades = 0

    for p in products:
        sku = p['sku']
        title = p['product_title']
        cat = p['category_group']
        color = p['color']

        # Find best photobank WebP images that are verified uploaded on server
        webp_matches = get_best_webp_images(title, cat, color, webp_list, server_url_map)

        # Existing images from DB (filter out broken html/fake photobank links)
        existing_imgs = [
            p.get(f'image_{i}') for i in range(1, 7)
            if is_valid_image(p.get(f'image_{i}'))
        ]

        # Tokopedia fallbacks
        tkp_imgs = tokopedia_fallbacks.get(sku) or tokopedia_fallbacks.get(title) or []

        # Combine images: Photobank WebPs first, then existing CDN, then Tokopedia fallbacks
        combined_imgs = []
        for w in webp_matches:
            if w not in combined_imgs:
                combined_imgs.append(w)
        for e in existing_imgs:
            if e not in combined_imgs:
                combined_imgs.append(e)
        for t in tkp_imgs:
            if t not in combined_imgs:
                combined_imgs.append(t)

        # Ensure we have at least up to 6 image slots
        final_imgs = (combined_imgs + [None] * 6)[:6]

        # Check if product has at least 1 VALID image
        has_valid_img = is_valid_image(final_imgs[0])

        # Generate 3 B2B export keywords
        new_keywords = generate_b2b_export_keywords(title, cat)

        # Update in Database
        cur.execute("""
            UPDATE products
            SET image_1 = ?, image_2 = ?, image_3 = ?, image_4 = ?, image_5 = ?, image_6 = ?,
                keywords = ?, updated_at = CURRENT_TIMESTAMP
            WHERE sku = ?
        """, (
            final_imgs[0], final_imgs[1], final_imgs[2],
            final_imgs[3], final_imgs[4], final_imgs[5],
            new_keywords, sku
        ))

        if webp_matches:
            photobank_upgrades += 1

        # Keep for November batch if it has valid images
        if has_valid_img:
            p_updated = p.copy()
            for i in range(1, 7):
                p_updated[f'image_{i}'] = final_imgs[i-1]
            p_updated['keywords'] = new_keywords
            valid_batch_products.append(p_updated)
        else:
            print(f"  [-] EXCLUDED from November Batch (No Valid Image): {sku} - {title}")

    conn.commit()
    conn.close()

    print(f"\n[+] Database updated successfully!")
    print(f"    - Photobank WebP upgrades applied: {photobank_upgrades} products")
    print(f"    - B2B Export Keywords generated: {len(products)} products")
    print(f"    - Products eligible for November Batch: {len(valid_batch_products)} of {len(products)}")

    # 2. Populate into Excel Template
    print(f"\n[*] Loading Alibaba Excel template: {TEMPLATE_PATH}")
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb['Alibaba default template']

    # Delete existing data rows starting from row 5
    if ws.max_row >= 5:
        ws.delete_rows(5, ws.max_row - 4)

    start_row = 5

    for idx, prod in enumerate(valid_batch_products):
        row_idx = start_row + idx

        sku = prod['sku']
        title = prod['product_title']
        cat = prod['category']
        html_desc = prod['description_html']
        weight_kg = prod['gross_weight_kg'] or 1.7
        l_val = prod['pkg_length'] or 60.0
        w_val = prod['pkg_width'] or 42.0
        h_val = prod['pkg_height'] or 38.0

        t1_price = prod['tier1_price'] or prod['price_usd'] or 5.50
        t2_price = prod['tier2_price'] or round(t1_price * 0.95, 2)
        t3_price = prod['tier3_price'] or round(t1_price * 0.90, 2)
        t4_price = prod['tier4_price'] or round(t1_price * 0.85, 2)
        moq_p = prod['moq1'] or 100

        # Build 57 column row data (1-indexed Col A to BE)
        row_data = [
            title,                      # Col 1 (A): * Product title
            prod.get('image_1'),        # Col 2 (B): * Product image 1
            prod.get('image_2'),        # Col 3 (C): Product image 2
            prod.get('image_3'),        # Col 4 (D): Product image 3
            prod.get('image_4'),        # Col 5 (E): Product image 4
            prod.get('image_5'),        # Col 6 (F): Product image 5
            prod.get('image_6'),        # Col 7 (G): Product image 6
            html_desc,                  # Col 8 (H): Product description
            prod.get('place_of_origin') or "Indonesia", # Col 9 (I): Place of origin
            prod.get('brand_name') or "AP Boots",      # Col 10 (J): Brand name
            cat,                        # Col 11 (K): Category
            "Outsole Material",         # Col 12 (L): Product attribute name 1
            prod.get('outsole_material') or "PVC / Rubber", # Col 13 (M): Product attribute value 1
            "Upper Material",           # Col 14 (N): Product attribute name 2
            prod.get('upper_material') or "PVC",            # Col 15 (O): Product attribute value 2
            "Season",                   # Col 16 (P): Product attribute name 3
            prod.get('season') or "All Seasons",            # Col 17 (Q): Product attribute value 3
            "Feature",                  # Col 18 (R): Product attribute name 4
            prod.get('feature') or "Waterproof, Anti-Slip, High Durability", # Col 19 (S): Product attribute value 4
            "Gender",                   # Col 20 (T): Product attribute name 5
            prod.get('gender') or "Men / Unisex",           # Col 21 (U): Product attribute value 5
            prod.get('sell_by') or "piece",                 # Col 22 (V): Sell product by
            None,                       # Col 23 (W): Batch quantity
            prod.get('unit') or "Pair/Pairs",               # Col 24 (X): Unit
            prod.get('currency') or "USD",                  # Col 25 (Y): Currency
            prod.get('pricing_type') or "Tiered pricing",   # Col 26 (Z): Pricing type
            prod.get('inventory') or 5000,                  # Col 27 (AA): Inventory
            sku,                        # Col 28 (AB): SPU ID (Model number)
            sku,                        # Col 29 (AC): SKU code
            t1_price,                   # Col 30 (AD): SKU pricing
            "Color",                    # Col 31 (AE): SKU attribute name 1
            prod.get('color') or "Black; Green; White; Yellow", # Col 32 (AF): SKU attribute value 1
            "Size",                     # Col 33 (AG): SKU attribute name 2
            prod.get('size_range') or "EU 38-44",              # Col 34 (AH): SKU attribute value 2
            None,                       # Col 35 (AI): SKU attribute name 3
            None,                       # Col 36 (AJ): SKU attribute value 3
            None,                       # Col 37 (AK): SKU attribute name 4
            None,                       # Col 38 (AL): SKU attribute value 4
            t1_price,                   # Col 39 (AM): Tiered pricing 1
            moq_p,                      # Col 40 (AN): MOQ 1
            t2_price,                   # Col 41 (AO): Tiered pricing 2
            moq_p * 5,                  # Col 42 (AP): MOQ 2
            t3_price,                   # Col 43 (AQ): Tiered pricing 3
            moq_p * 10,                 # Col 44 (AR): MOQ 3
            t4_price,                   # Col 45 (AS): Range pricing (Lower limit)
            t1_price,                   # Col 46 (AT): Range pricing (Higher limit)
            weight_kg,                  # Col 47 (AU): * Gross weight (KG)
            prod.get('shipping_template') or "Default Shipping Template", # Col 48 (AV): * Shipping template name
            moq_p,                      # Col 49 (AW): * Shipping quantity 1
            prod.get('lead_time_1') or 7, # Col 50 (AX): * Estimated shipping lead time 1
            moq_p * 5,                  # Col 51 (AY): Shipping quantity 2
            prod.get('lead_time_2') or 14, # Col 52 (AZ): Estimated shipping lead time 2
            moq_p * 10,                 # Col 53 (BA): Shipping quantity 3
            prod.get('lead_time_3') or 30, # Col 54 (BB): Estimated shipping lead time 3
            l_val,                      # Col 55 (BC): Product size-Length
            w_val,                      # Col 56 (BD): Product size-Width
            h_val                       # Col 57 (BE): Product size-Height
        ]

        for col_i, val in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_i, value=val)

    print(f"[*] Saving November Batch Excel to: {OUTPUT_EXCEL}")
    wb.save(OUTPUT_EXCEL)
    print("=" * 70)
    print(f"Batch generation completed successfully! Total products in batch: {len(valid_batch_products)}")
    print("=" * 70)

if __name__ == '__main__':
    main()
