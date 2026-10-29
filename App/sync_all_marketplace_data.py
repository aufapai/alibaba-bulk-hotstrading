import os
import sys
import re
import glob
import sqlite3
import pandas as pd
import openpyxl
from datetime import datetime

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
INPUT_DIR = os.path.join(BASE_DIR, "Input")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from image_deduplicator import clean_and_deduplicate_images, normalize_and_upgrade_image
from keyword_bot import match_product_keywords
from accio_keyword_generator import generate_accio_listing, clean_model_name

STOPWORDS = {
    'SEPATU', 'BOOT', 'BOOTS', 'PVC', 'KARET', 'SHOES', 'PRIA', 'WANITA', 'ANAK',
    'ORIGINAL', 'ASLI', 'SERIES', 'WARNA', 'SIZE', 'UKURAN', 'HITAM', 'PUTIH',
    'HIJAU', 'KUNING', 'MERAH', 'COKLAT', 'BIRU', 'ABU', 'ORANGE', 'MULTI', 'STABILO',
    'BESAR', 'KECIL', 'FASHION', 'MOTIF', 'STRIPE', 'DAN', 'UNTUK', 'DAPUR', 'KETS',
    'SLIP', 'ON', 'KERJA', 'SAFETY', 'PENDEK', 'TINGGI', 'OFFICIAL', 'STORE',
    'TERBARU', 'MURAH', 'BEST', 'SELLER'
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_model_signatures(name):
    """
    Extracts high-confidence matching tokens for AP Boots models,
    ignoring sizes, colors, and generic product words.
    """
    if not name or pd.isna(name):
        return []
    raw = str(name).strip()
    clean = re.sub(r'\s*-\s*\d+.*$', '', raw)
    clean = re.sub(r'(?i)^AP\s*Boots\s*', '', clean)
    clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', clean)
    words = [w.upper() for w in clean.split() if w.upper() not in STOPWORDS]

    keys = []
    if len(words) >= 2:
        keys.append(f"{words[0]}_{words[1]}")
        keys.append(f"{words[0]} {words[1]}")
    if len(words) >= 1:
        keys.append(words[0])

    m_num = re.findall(r'\b(\d{3,4})\b', raw)
    for n in m_num:
        if n not in keys:
            keys.append(n)

    alpha = re.sub(r'[^A-Z0-9]', '', raw.upper())
    if alpha and len(alpha) <= 25 and alpha not in keys:
        keys.append(alpha)

    return keys

def build_comprehensive_image_bank():
    """
    Scans Photobank CSVs and all raw marketplace inputs (Tokopedia, Blibli, Lazada, Shopee)
    to create an indexed pool of verified high-res product photos.
    """
    print("--> Indexing Multi-Source Platform Images for Combination...")
    bank = {}

    def register_images(name_str, urls):
        if not name_str or not urls:
            return
        valid_urls = []
        for u in urls:
            if u and str(u).strip().startswith('http'):
                upg, _ = normalize_and_upgrade_image(str(u).strip())
                if upg and upg not in valid_urls:
                    valid_urls.append(upg)
        if not valid_urls:
            return

        sigs = get_model_signatures(name_str)
        for s in sigs:
            bank.setdefault(s, []).extend(valid_urls)

    # 1. Photobank CSV
    pb_file = os.path.join(INPUT_DIR, "photobank_server_uploaded.csv")
    if os.path.exists(pb_file):
        try:
            df_pb = pd.read_csv(pb_file)
            for _, r in df_pb.iterrows():
                sku = str(r.get('SKU', '')).strip()
                name = str(r.get('Nama Produk', '')).strip()
                url = str(r.get('URL Gambar', '')).strip()
                if url.startswith('http'):
                    register_images(sku, [url])
                    register_images(name, [url])
        except Exception:
            pass

    # 2. Additional Photobank batches
    pb_dir = os.path.join(BASE_DIR, "datagambar photbank")
    if os.path.exists(pb_dir):
        for f in glob.glob(os.path.join(pb_dir, "*.csv")):
            try:
                df_b = pd.read_csv(f)
                for _, r in df_b.iterrows():
                    sku = str(r.get('SKU', '')).strip()
                    name = str(r.get('Nama Produk', '')).strip()
                    url = str(r.get('URL Gambar', '')).strip()
                    if url.startswith('http'):
                        register_images(sku, [url])
                        register_images(name, [url])
            except Exception:
                pass

    # 3. Tokopedia input files
    tok_files = ["tokopedia-com-2026-09-23-3 (1).xlsx", "tokopedia-com-2026-09-23-3.xlsx", "tokopedia-com-2026-09-23.xlsx"]
    for tf in tok_files:
        p = os.path.join(INPUT_DIR, tf)
        if os.path.exists(p):
            try:
                df_t = pd.read_excel(p)
                for _, r in df_t.iterrows():
                    name = str(r.get('product_name') or r.get('data') or '').strip()
                    imgs = [str(r.get('main_image') or '').strip()]
                    for line in str(r.get('image_17') or '').split():
                        if line.startswith('http'): imgs.append(line.strip())
                    register_images(name, imgs)
            except Exception:
                pass

    # 4. Blibli input
    p_bli = os.path.join(INPUT_DIR, "blibli-com-2026-10-14.xlsx")
    if os.path.exists(p_bli):
        try:
            df_bl = pd.read_excel(p_bli)
            for _, r in df_bl.iterrows():
                name = str(r.get('name') or r.get('item_page_title') or '').strip()
                imgs = [str(r.get(c) or '').strip() for c in df_bl.columns if 'image' in c.lower() and str(r.get(c) or '').startswith('http')]
                register_images(name, imgs)
        except Exception:
            pass

    # 5. Lazada input
    p_laz = os.path.join(INPUT_DIR, "lazada-co-id-2026-10-14.xlsx")
    if os.path.exists(p_laz):
        try:
            df_lz = pd.read_excel(p_laz)
            for _, r in df_lz.iterrows():
                name = str(r.get('name') or r.get('title') or '').strip()
                raw_imgs = str(r.get('image_1') or '') + ' ' + str(r.get('image_27') or '')
                imgs = [u.strip() for u in raw_imgs.split() if u.strip().startswith('http')]
                register_images(name, imgs)
        except Exception:
            pass

    # Deduplicate candidate lists within each key
    for k in bank:
        clean_list = []
        seen = set()
        for u in bank[k]:
            if u not in seen:
                seen.add(u)
                clean_list.append(u)
        bank[k] = clean_list

    print(f"  [OK] Multi-source image bank ready with {len(bank)} model keys.")

    def lookup_images(query_str, exclude_urls=None, max_count=6):
        if not query_str:
            return []
        excludes = set(exclude_urls or [])
        sigs = get_model_signatures(query_str)
        candidates = []
        for s in sigs:
            if s in bank:
                for u in bank[s]:
                    if u not in excludes and u not in candidates:
                        candidates.append(u)
        return candidates[:max_count]

    return lookup_images

def init_schemas(conn):
    cur = conn.cursor()

    # 1. Main Products Table (Alibaba Listing Catalog)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        model_number TEXT,
        alibaba_product_id TEXT,
        product_title TEXT NOT NULL,
        category TEXT NOT NULL,
        category_group TEXT,
        keywords TEXT,
        image_1 TEXT NOT NULL,
        image_2 TEXT,
        image_3 TEXT,
        image_4 TEXT,
        image_5 TEXT,
        image_6 TEXT,
        description_html TEXT NOT NULL,
        place_of_origin TEXT DEFAULT 'Indonesia',
        brand_name TEXT DEFAULT 'AP Boots',
        outsole_material TEXT DEFAULT 'PVC / Rubber',
        upper_material TEXT DEFAULT 'PVC',
        season TEXT DEFAULT 'All Seasons',
        feature TEXT,
        gender TEXT DEFAULT 'Men / Unisex',
        sell_by TEXT DEFAULT 'piece',
        unit TEXT DEFAULT 'Pair/Pairs',
        currency TEXT DEFAULT 'USD',
        pricing_type TEXT DEFAULT 'Tiered pricing',
        inventory INTEGER DEFAULT 5000,
        price_usd REAL DEFAULT 5.50,
        color TEXT DEFAULT 'Black; Green; White; Yellow',
        size_range TEXT DEFAULT 'EU 38-44',
        tier1_price REAL,
        moq1 INTEGER DEFAULT 100,
        tier2_price REAL,
        moq2 INTEGER DEFAULT 500,
        tier3_price REAL,
        moq3 INTEGER DEFAULT 1000,
        tier4_price REAL,
        gross_weight_kg REAL DEFAULT 1.7,
        shipping_template TEXT DEFAULT 'Default Shipping Template',
        lead_time_1 INTEGER DEFAULT 7,
        lead_time_2 INTEGER DEFAULT 14,
        lead_time_3 INTEGER DEFAULT 30,
        pkg_length REAL DEFAULT 60.0,
        pkg_width REAL DEFAULT 42.0,
        pkg_height REAL DEFAULT 38.0,
        status TEXT DEFAULT 'Ready for Upload',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source TEXT DEFAULT 'alibaba_master',
        price_idr INTEGER,
        sold_count INTEGER DEFAULT 0,
        rating_score REAL,
        industry_angle TEXT,
        target_keywords TEXT,
        source_url TEXT,
        is_flagship INTEGER DEFAULT 0,
        flagship_rank INTEGER,
        raw_source_title TEXT
    );
    """)

    # 2. Raw Marketplace Items Table with UNIQUE(source, product_name)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS marketplace_raw (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        source_id TEXT,
        product_name TEXT NOT NULL,
        price_idr INTEGER,
        price_usd REAL,
        sold_raw TEXT,
        sold_count INTEGER DEFAULT 0,
        rating_score REAL,
        source_url TEXT,
        raw_images_text TEXT,
        image_1 TEXT,
        image_2 TEXT,
        image_3 TEXT,
        image_4 TEXT,
        image_5 TEXT,
        image_6 TEXT,
        unique_images_count INTEGER DEFAULT 0,
        duplicate_images_removed INTEGER DEFAULT 0,
        category_raw TEXT,
        description_raw TEXT,
        brand TEXT DEFAULT 'AP Boots',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_mkt_source_name ON marketplace_raw (source, product_name);")


    # 3. Alibaba 800 Matrix Master Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alibaba_matrix_800 (
        listing_id TEXT PRIMARY KEY,
        unique_sku_code TEXT NOT NULL,
        base_sku TEXT,
        base_product_name TEXT,
        angle_id TEXT,
        target_industry_angle TEXT,
        alibaba_product_title TEXT,
        alibaba_category TEXT,
        brand TEXT,
        place_of_origin TEXT,
        upper_material TEXT,
        outsole_material TEXT,
        toe_style TEXT,
        boot_height TEXT,
        colors TEXT,
        size_range TEXT,
        key_features TEXT,
        target_application TEXT,
        primary_keyword_1 TEXT,
        primary_keyword_2 TEXT,
        primary_keyword_3 TEXT,
        longtail_keywords TEXT,
        moq_pairs INTEGER,
        price_tier1_usd REAL,
        price_tier2_usd REAL,
        price_tier3_usd REAL,
        pairs_per_carton INTEGER,
        carton_dimensions TEXT,
        carton_gross_weight_kg REAL,
        carton_cbm REAL,
        port_of_loading TEXT,
        estimated_lead_time TEXT,
        tailored_html_description TEXT,
        image_1 TEXT,
        image_2 TEXT,
        image_3 TEXT,
        image_4 TEXT,
        image_5 TEXT,
        image_6 TEXT
    );
    """)

    # Ensure image columns exist in alibaba_matrix_800
    cur.execute("PRAGMA table_info(alibaba_matrix_800)")
    mat_cols = [r['name'] for r in cur.fetchall()]
    for img_c in ['image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6']:
        if img_c not in mat_cols:
            cur.execute(f"ALTER TABLE alibaba_matrix_800 ADD COLUMN {img_c} TEXT")

    # 4. Alibaba Keywords Manager Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alibaba_keywords (
        unique_sku_code TEXT PRIMARY KEY,
        base_product_name TEXT,
        target_industry_angle TEXT,
        alibaba_product_title TEXT,
        primary_keyword_1 TEXT,
        primary_keyword_2 TEXT,
        primary_keyword_3 TEXT,
        longtail_keywords TEXT
    );
    """)

    conn.commit()

def cleanup_duplicate_marketplace_data(conn):
    """
    Cleans out historical duplicate records before syncing fresh data,
    ensuring 0 duplicate product names per platform while keeping catalog safe.
    """
    cur = conn.cursor()
    # Purge marketplace_raw to allow clean unique population
    cur.execute("DELETE FROM marketplace_raw")
    # Clean marketplace sources from products table to prevent SKU / title fragmentation
    cur.execute("DELETE FROM products WHERE source IN ('tokopedia', 'shopee', 'blibli', 'lazada')")
    conn.commit()
    print("  [OK] Cleaned historical marketplace duplicates. Ready for pristine ingestion.")

def sync_tokopedia(conn):
    """
    Loads and deduplicates Tokopedia products strictly by product name.
    Across the 3 Tokopedia input files, keeps exactly 1 richest record per product name.
    """
    tok_files = [
        "tokopedia-com-2026-09-23-3 (1).xlsx",
        "tokopedia-com-2026-09-23-3.xlsx",
        "tokopedia-com-2026-09-23.xlsx"
    ]
    cur = conn.cursor()
    tok_dict = {}

    for tf in tok_files:
        fpath = os.path.join(INPUT_DIR, tf)
        if not os.path.exists(fpath):
            continue
        print(f"--> Reading Tokopedia inputs from: {tf}")
        df = pd.read_excel(fpath)
        for _, r in df.iterrows():
            name = str(r.get('product_name') or r.get('data') or '').strip()
            if not name or name == 'nan':
                continue
            norm_name = re.sub(r'\s+', ' ', name)

            # Price IDR
            price_raw = str(r.get('price') or '')
            m_p = re.search(r'([0-9\.]+)', price_raw)
            price_idr = int(m_p.group(1).replace('.', '')) if m_p else None

            # Sold count
            sold_raw = str(r.get('sold') or '')
            sold_count = 0
            if 'rb' in sold_raw.lower():
                try: sold_count = int(float(sold_raw.lower().replace('rb','').replace('+','').replace(',','.')) * 1000)
                except: sold_count = 1000
            else:
                m_s = re.search(r'(\d+)', sold_raw)
                if m_s: sold_count = int(m_s.group(1))

            # URL
            url = str(r.get('item_page_link') or '').split('?')[0].rstrip('/')

            # Images
            raw_imgs = []
            m_img = str(r.get('main_image') or '').strip()
            if m_img.startswith('http'):
                raw_imgs.append(m_img)
            for line in str(r.get('image_17') or '').split():
                if line.startswith('http') and line not in raw_imgs:
                    raw_imgs.append(line.strip())

            if norm_name not in tok_dict:
                tok_dict[norm_name] = {
                    'name': norm_name,
                    'price_idr': price_idr or 65000,
                    'sold_raw': sold_raw,
                    'sold_count': sold_count,
                    'rating_score': 4.9,
                    'url': url,
                    'images': raw_imgs
                }
            else:
                # Merge into existing record (richest data wins)
                rec = tok_dict[norm_name]
                if price_idr and (not rec['price_idr'] or rec['price_idr'] == 65000):
                    rec['price_idr'] = price_idr
                if sold_count > rec['sold_count']:
                    rec['sold_count'] = sold_count
                    rec['sold_raw'] = sold_raw
                if url and not rec['url']:
                    rec['url'] = url
                for img in raw_imgs:
                    if img not in rec['images']:
                        rec['images'].append(img)

    inserted = 0
    for idx, (pname, item) in enumerate(tok_dict.items(), start=1):
        price_idr = item['price_idr']
        price_usd = round(price_idr / 16000.0, 2)
        sku = f"TOK-{idx:03d}"
        model = pname.split('-')[0].strip()[:30]

        dedup_imgs = clean_and_deduplicate_images(item['images'], marketplace='tokopedia')
        valid_count = sum(1 for img in dedup_imgs if img)
        dups_removed = max(0, len(item['images']) - valid_count)

        kw_info = match_product_keywords(pname, category="Boots")

        # 1. Insert into marketplace_raw (authentic data intact)
        cur.execute("""
        INSERT INTO marketplace_raw (
            source, source_id, product_name, price_idr, price_usd, sold_raw,
            sold_count, rating_score, source_url, raw_images_text,
            image_1, image_2, image_3, image_4, image_5, image_6,
            unique_images_count, duplicate_images_removed, category_raw, brand
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source, product_name) DO UPDATE SET
            price_idr = excluded.price_idr,
            price_usd = excluded.price_usd,
            image_1 = excluded.image_1,
            image_2 = excluded.image_2,
            image_3 = excluded.image_3,
            image_4 = excluded.image_4,
            image_5 = excluded.image_5,
            image_6 = excluded.image_6;
        """, (
            'tokopedia', sku, pname, price_idr, price_usd, item['sold_raw'],
            item['sold_count'], item['rating_score'], item['url'], "\n".join(item['images']),
            dedup_imgs[0], dedup_imgs[1], dedup_imgs[2], dedup_imgs[3], dedup_imgs[4], dedup_imgs[5],
            valid_count, dups_removed, "Sepatu Boot Pria", "AP Boots"
        ))

        # 2. Insert into products (authentic title & raw_source_title intact)
        cur.execute("""
        INSERT INTO products (
            sku, model_number, product_title, raw_source_title, category, category_group,
            keywords, image_1, image_2, image_3, image_4, image_5, image_6,
            description_html, price_usd, tier1_price, tier2_price, tier3_price,
            moq1, moq2, moq3, gross_weight_kg, status, source, price_idr,
            sold_count, rating_score, industry_angle, source_url
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        ) ON CONFLICT(sku) DO UPDATE SET
            product_title = excluded.product_title,
            raw_source_title = excluded.raw_source_title,
            keywords = excluded.keywords,
            image_1 = excluded.image_1,
            image_2 = excluded.image_2,
            image_3 = excluded.image_3,
            image_4 = excluded.image_4,
            image_5 = excluded.image_5,
            image_6 = excluded.image_6,
            price_usd = excluded.price_usd,
            price_idr = excluded.price_idr,
            sold_count = excluded.sold_count,
            rating_score = excluded.rating_score,
            updated_at = CURRENT_TIMESTAMP;
        """, (
            sku, model, pname, pname, "Shoes & Accessories > Men's Shoes > Boots",
            "AP Boots Tokopedia", kw_info['keywords'],
            dedup_imgs[0], dedup_imgs[1], dedup_imgs[2], dedup_imgs[3], dedup_imgs[4], dedup_imgs[5],
            f"<p>Official Tokopedia AP Boots - {pname}. Guaranteed 100% Genuine Indonesian Footwear.</p>",
            price_usd, price_usd, round(price_usd*0.95, 2), round(price_usd*0.90, 2),
            100, 500, 1000, 1.7, "Ready for Upload", "tokopedia", price_idr,
            item['sold_count'], item['rating_score'], kw_info['target_industry_angle'], item['url']
        ))
        inserted += 1

    conn.commit()
    print(f"  [OK] Processed exactly {inserted} unique Tokopedia products (0 duplicates).")
    return inserted

def sync_shopee(conn, lookup_images):
    """
    Loads Shopee products, ensuring 0 duplicates by product name.
    Prioritizes official Shopee October catalogs:
    - Petrova: Input/shopee-co-id-2026-10-petrova.csv
    - AP Boots: Input/shopee-co-id-2026-10-apboots.csv
    With fallback to shopee-co-id-2026-09-23.xlsx.
    Enforces GPSR Batch Compliance PT Waru Gunung on product descriptions and titles.
    """
    shopee_sources = []
    shp_petrova = os.path.join(INPUT_DIR, "shopee-co-id-2026-10-petrova.csv")
    shp_apboots = os.path.join(INPUT_DIR, "shopee-co-id-2026-10-apboots.csv")
    shp_legacy = os.path.join(INPUT_DIR, "shopee-co-id-2026-09-23.xlsx")

    if os.path.exists(shp_petrova):
        shopee_sources.append(("Petrova", pd.read_csv(shp_petrova), os.path.basename(shp_petrova)))
    if os.path.exists(shp_apboots):
        shopee_sources.append(("AP Boots", pd.read_csv(shp_apboots), os.path.basename(shp_apboots)))
    if not shopee_sources and os.path.exists(shp_legacy):
        shopee_sources.append(("AP Boots", pd.read_excel(shp_legacy), os.path.basename(shp_legacy)))

    if not shopee_sources:
        print(f"[WARN] No Shopee input files found in: {INPUT_DIR}")
        return 0

    cur = conn.cursor()
    total_inserted = 0

    for default_brand, df_shp, source_file in shopee_sources:
        print(f"--> Ingesting Shopee {default_brand} products from: {source_file} ({len(df_shp)} rows)")
        shp_dict = {}
        for _, r in df_shp.iterrows():
            if pd.notna(r.get('name')):
                name = str(r.get('name')).strip()
            elif pd.notna(r.get('data2')):
                name = str(r.get('data2')).strip()
            else:
                name = str(r.iloc[4] if len(r) > 4 else '').strip()
            if not name or name == 'nan':
                continue
            norm_name = re.sub(r'\s+', ' ', name)
            if norm_name not in shp_dict:
                shp_dict[norm_name] = r

        for idx, (pname, r) in enumerate(shp_dict.items(), start=1):
            price_raw = str(r.get('data') or (r.iloc[3] if len(r) > 3 else ''))
            m_p = re.search(r'([0-9\.]+)', price_raw)
            if m_p:
                p_val = float(m_p.group(1))
                price_idr = int(p_val * 1000) if p_val < 1000 else int(p_val)
            else:
                price_idr = 55000
            price_usd = round(price_idr / 16000.0, 2)

            if pd.notna(r.get('name')):
                sold_raw = str(r.get('data2') or '')
                try: rating = float(r.get('data4') or 4.9)
                except: rating = 4.9
            else:
                sold_raw = str(r.get('data3') or '')
                try: rating = float(r.get('data5') or 4.9)
                except: rating = 4.9

            sold_count = 0
            if 'rb' in sold_raw.lower():
                try: sold_count = int(float(sold_raw.lower().replace('rb','').replace('+','').replace(',','.')) * 1000)
                except: sold_count = 1000
            else:
                m_s = re.search(r'(\d+)', sold_raw)
                if m_s: sold_count = int(m_s.group(1))

            brand = "Petrova" if "petrova" in pname.lower() else "AP Boots"
            sku = f"PTR-{idx:03d}" if brand == "Petrova" else f"SHP-{idx:03d}"
            model = clean_model_name(pname)
            url = str(r.get('web_scraper_start_url') or ("https://shopee.co.id/petrovabootsofficial" if brand == "Petrova" else "https://shopee.co.id/apbootsofficial"))

            all_imgs = []
            for col in ['image', 'image2', 'image3', 'image4']:
                raw_url = str(r.get(col) or '').strip()
                if raw_url and raw_url.startswith('http') and raw_url != 'nan':
                    upg_url, _ = normalize_and_upgrade_image(raw_url)
                    chosen = upg_url or raw_url
                    if chosen not in all_imgs:
                        all_imgs.append(chosen)

            if len(all_imgs) < 6:
                extra_imgs = lookup_images(pname, exclude_urls=all_imgs, max_count=6 - len(all_imgs))
                for ext in extra_imgs:
                    if ext and ext not in all_imgs:
                        all_imgs.append(ext)

            while len(all_imgs) < 6:
                all_imgs.append("")

            try:
                accio_pkg = generate_accio_listing(
                    sku=sku,
                    product_title=pname,
                    category_group=f"{brand} Shopee",
                    existing_price=price_usd,
                    existing_weight=1.7
                )
                title_to_save = accio_pkg['primary_title']
                keywords_to_save = accio_pkg['keywords']
                desc_html_to_save = accio_pkg['description_html']
                angle_to_save = accio_pkg['target_industry_angle']
            except Exception as ex:
                print(f"  [WARN] Accio generation failed for {sku}: {ex}")
                title_to_save = pname
                keywords_to_save = f"{brand} boots, Indonesia factory direct, PT Waru Gunung"
                desc_html_to_save = f"<p>{brand} manufactured by PT Waru Gunung - {pname}.</p>"
                angle_to_save = "Civil Construction" if "safety" in pname.lower() else "Agriculture & Farming"

            # Insert into marketplace_raw
            cur.execute("""
            INSERT INTO marketplace_raw (
                source, source_id, product_name, price_idr, price_usd, sold_raw,
                sold_count, rating_score, source_url, raw_images_text,
                image_1, image_2, image_3, image_4, image_5, image_6,
                unique_images_count, duplicate_images_removed, category_raw, brand
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source, product_name) DO UPDATE SET
                price_idr = excluded.price_idr,
                price_usd = excluded.price_usd,
                image_1 = excluded.image_1,
                image_2 = excluded.image_2,
                image_3 = excluded.image_3,
                image_4 = excluded.image_4,
                image_5 = excluded.image_5,
                image_6 = excluded.image_6;
            """, (
                'shopee', sku, pname, price_idr, price_usd, sold_raw,
                sold_count, rating, url, "\n".join([img for img in all_imgs if img]),
                all_imgs[0], all_imgs[1], all_imgs[2], all_imgs[3], all_imgs[4], all_imgs[5],
                sum(1 for img in all_imgs if img), 0, f"Sepatu Boot {brand} Shopee", brand
            ))

            # Insert into products
            cur.execute("""
            INSERT INTO products (
                sku, model_number, product_title, raw_source_title, category, category_group,
                keywords, image_1, image_2, image_3, image_4, image_5, image_6,
                description_html, price_usd, tier1_price, tier2_price, tier3_price,
                moq1, moq2, moq3, gross_weight_kg, status, source, price_idr,
                sold_count, rating_score, industry_angle, source_url, brand_name, place_of_origin
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            ) ON CONFLICT(sku) DO UPDATE SET
                product_title = excluded.product_title,
                raw_source_title = excluded.raw_source_title,
                keywords = excluded.keywords,
                image_1 = excluded.image_1,
                image_2 = excluded.image_2,
                image_3 = excluded.image_3,
                image_4 = excluded.image_4,
                image_5 = excluded.image_5,
                image_6 = excluded.image_6,
                description_html = excluded.description_html,
                price_usd = excluded.price_usd,
                price_idr = excluded.price_idr,
                sold_count = excluded.sold_count,
                rating_score = excluded.rating_score,
                industry_angle = excluded.industry_angle,
                brand_name = excluded.brand_name,
                place_of_origin = excluded.place_of_origin,
                updated_at = CURRENT_TIMESTAMP;
            """, (
                sku, model, title_to_save, pname, "Shoes & Accessories > Men's Shoes > Boots",
                f"{brand} Shopee Official", keywords_to_save,
                all_imgs[0], all_imgs[1], all_imgs[2], all_imgs[3], all_imgs[4], all_imgs[5],
                desc_html_to_save,
                price_usd, price_usd, round(price_usd*0.95, 2), round(price_usd*0.90, 2),
                100, 500, 1000, 1.7, "Ready for Upload", "shopee", price_idr,
                sold_count, rating, angle_to_save, url, brand, "Indonesia"
            ))
            total_inserted += 1

    conn.commit()
    print(f"  [OK] Processed exactly {total_inserted} total Shopee products (Petrova & AP Boots).")
    return total_inserted

    conn.commit()
    print(f"  [OK] Processed exactly {inserted} unique Shopee products ({brand}). Enriched {enriched_images_count} products with image 2-6.")
    return inserted

    conn.commit()
    print(f"  [OK] Processed exactly {inserted} unique Shopee products. Enriched {enriched_images_count} products with image 2-6.")
    return inserted

def sync_blibli(conn):
    """Loads and deduplicates Blibli products by product name."""
    bli_file = os.path.join(INPUT_DIR, "blibli-com-2026-10-14.xlsx")
    if not os.path.exists(bli_file):
        bli_file = os.path.join(INPUT_DIR, "blibli-com-2026-10-14.csv")
    if not os.path.exists(bli_file):
        return 0

    df = pd.read_excel(bli_file) if bli_file.endswith('.xlsx') else pd.read_csv(bli_file)
    cur = conn.cursor()
    print(f"--> Ingesting Blibli products from: {os.path.basename(bli_file)} ({len(df)} rows)")

    bli_dict = {}
    for _, r in df.iterrows():
        name = str(r.get('name') or r.get('item_page_title') or '').strip()
        if not name or name == 'nan':
            continue
        norm_name = re.sub(r'\s+', ' ', name)
        if norm_name not in bli_dict:
            bli_dict[norm_name] = r

    inserted = 0
    img_cols = [c for c in df.columns if 'image' in c.lower()]

    for idx, (pname, r) in enumerate(bli_dict.items(), start=1):
        raw_val = str(r.get('data') or r.get('price') or '')
        m = re.search(r'([\d\.]+)', raw_val)
        if m:
            val_f = float(m.group(1))
            price_idr = int(val_f * 1000) if val_f < 1000 else int(val_f)
        else:
            price_idr = 75000
        price_usd = round(price_idr / 16000.0, 2)

        sold_raw = str(r.get('data2') or '')
        sold_count = 0
        m_s = re.search(r'(\d+)', sold_raw)
        if m_s: sold_count = int(m_s.group(1))

        try: rating = float(r.get('ratingvalue') or r.get('rating') or 4.9)
        except: rating = 4.9

        raw_imgs = []
        for c in img_cols:
            v = str(r.get(c) or '').strip()
            if v.startswith('http') and v not in raw_imgs:
                raw_imgs.append(v)

        dedup_imgs = clean_and_deduplicate_images(raw_imgs, marketplace='blibli')
        valid_count = sum(1 for img in dedup_imgs if img)

        sku = f"BLI-{idx:03d}"
        model = pname.split('-')[0].strip()[:30]
        url = str(r.get('item_page_link') or '')
        desc = str(r.get('product_description') or r.get('Description') or '')
        kw_info = match_product_keywords(pname, category="Boots")

        # 1. Insert into marketplace_raw (authentic data intact)
        cur.execute("""
        INSERT INTO marketplace_raw (
            source, source_id, product_name, price_idr, price_usd, sold_raw,
            sold_count, rating_score, source_url, raw_images_text,
            image_1, image_2, image_3, image_4, image_5, image_6,
            unique_images_count, duplicate_images_removed, category_raw, description_raw, brand
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source, product_name) DO UPDATE SET
            price_idr = excluded.price_idr,
            price_usd = excluded.price_usd,
            image_1 = excluded.image_1,
            image_2 = excluded.image_2,
            image_3 = excluded.image_3,
            image_4 = excluded.image_4,
            image_5 = excluded.image_5,
            image_6 = excluded.image_6;
        """, (
            'blibli', sku, pname, price_idr, price_usd, sold_raw,
            sold_count, rating, url, "\n".join(raw_imgs),
            dedup_imgs[0], dedup_imgs[1], dedup_imgs[2], dedup_imgs[3], dedup_imgs[4], dedup_imgs[5],
            valid_count, 0, "Boots & Workwear", desc[:500], "AP Boots"
        ))

        # 2. Insert into products (authentic title & raw_source_title intact)
        cur.execute("""
        INSERT INTO products (
            sku, model_number, product_title, raw_source_title, category, category_group,
            keywords, image_1, image_2, image_3, image_4, image_5, image_6,
            description_html, price_usd, tier1_price, tier2_price, tier3_price,
            moq1, moq2, moq3, gross_weight_kg, status, source, price_idr,
            sold_count, rating_score, industry_angle, source_url
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        ) ON CONFLICT(sku) DO UPDATE SET
            product_title = excluded.product_title,
            raw_source_title = excluded.raw_source_title,
            keywords = excluded.keywords,
            image_1 = excluded.image_1,
            image_2 = excluded.image_2,
            image_3 = excluded.image_3,
            image_4 = excluded.image_4,
            image_5 = excluded.image_5,
            image_6 = excluded.image_6,
            price_usd = excluded.price_usd,
            price_idr = excluded.price_idr,
            sold_count = excluded.sold_count,
            rating_score = excluded.rating_score,
            updated_at = CURRENT_TIMESTAMP;
        """, (
            sku, model, pname, pname, "Shoes & Accessories > Men's Shoes > Boots",
            "AP Boots Blibli", kw_info['keywords'],
            dedup_imgs[0], dedup_imgs[1], dedup_imgs[2], dedup_imgs[3], dedup_imgs[4], dedup_imgs[5],
            f"<p>Official AP Boots Blibli - {pname}. High quality rubber & PVC footwear.</p>",
            price_usd, price_usd, round(price_usd*0.95, 2), round(price_usd*0.90, 2),
            100, 500, 1000, 1.7, "Ready for Upload", "blibli", price_idr,
            sold_count, rating, kw_info['target_industry_angle'], url
        ))
        inserted += 1

    conn.commit()
    print(f"  [OK] Processed exactly {inserted} unique Blibli products (0 duplicates).")
    return inserted

def sync_lazada(conn):
    """Loads and deduplicates Lazada products by product name."""
    laz_file = os.path.join(INPUT_DIR, "lazada-co-id-2026-10-14.xlsx")
    if not os.path.exists(laz_file):
        laz_file = os.path.join(INPUT_DIR, "lazada-co-id-2026-10-14.csv")
    if not os.path.exists(laz_file):
        return 0

    df = pd.read_excel(laz_file) if laz_file.endswith('.xlsx') else pd.read_csv(laz_file)
    cur = conn.cursor()
    print(f"--> Ingesting Lazada products from: {os.path.basename(laz_file)} ({len(df)} rows)")

    laz_dict = {}
    for _, r in df.iterrows():
        name = str(r.get('name') or r.get('title') or '').strip()
        if not name or name == 'nan':
            continue
        norm_name = re.sub(r'\s+', ' ', name)
        if norm_name not in laz_dict:
            laz_dict[norm_name] = r

    inserted = 0
    for idx, (pname, r) in enumerate(laz_dict.items(), start=1):
        price_idr = None
        data_str = str(r.get('data') or '')
        if 'Rp' in data_str:
            m = re.search(r'Rp\s*([\d\.]+)', data_str)
            if m:
                price_idr = int(m.group(1).replace('.', ''))
        if not price_idr and pd.notna(r.get('price')):
            try:
                p = float(r.get('price'))
                price_idr = int(p * 1000) if p < 1000 else int(p)
            except:
                price_idr = 50000
        price_usd = round((price_idr or 50000) / 16000.0, 2)

        sold_raw = str(r.get('data2') or '')
        sold_count = 0
        m_s = re.search(r'(\d+)', sold_raw)
        if m_s: sold_count = int(m_s.group(1))

        try: rating = float(r.get('rating_score') or 4.8)
        except: rating = 4.8

        raw_imgs = str(r.get('image_1') or '') + '\n' + str(r.get('image_27') or '')
        raw_img_list = [u.strip() for u in raw_imgs.split() if u.strip().startswith('http')]
        dedup_imgs = clean_and_deduplicate_images(raw_img_list, marketplace='lazada')
        valid_count = sum(1 for img in dedup_imgs if img)

        sku = f"LAZ-{idx:03d}"
        model = pname.split('-')[0].strip()[:30]
        url = str(r.get('item_page_link') or '')
        kw_info = match_product_keywords(pname, category="Boots")

        # 1. Insert into marketplace_raw (authentic data intact)
        cur.execute("""
        INSERT INTO marketplace_raw (
            source, source_id, product_name, price_idr, price_usd, sold_raw,
            sold_count, rating_score, source_url, raw_images_text,
            image_1, image_2, image_3, image_4, image_5, image_6,
            unique_images_count, duplicate_images_removed, category_raw, brand
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source, product_name) DO UPDATE SET
            price_idr = excluded.price_idr,
            price_usd = excluded.price_usd,
            image_1 = excluded.image_1,
            image_2 = excluded.image_2,
            image_3 = excluded.image_3,
            image_4 = excluded.image_4,
            image_5 = excluded.image_5,
            image_6 = excluded.image_6;
        """, (
            'lazada', sku, pname, price_idr, price_usd, sold_raw,
            sold_count, rating, url, raw_imgs,
            dedup_imgs[0], dedup_imgs[1], dedup_imgs[2], dedup_imgs[3], dedup_imgs[4], dedup_imgs[5],
            valid_count, 0, "Boots & Shoes", "AP Boots"
        ))

        # 2. Insert into products (authentic title & raw_source_title intact)
        cur.execute("""
        INSERT INTO products (
            sku, model_number, product_title, raw_source_title, category, category_group,
            keywords, image_1, image_2, image_3, image_4, image_5, image_6,
            description_html, price_usd, tier1_price, tier2_price, tier3_price,
            moq1, moq2, moq3, gross_weight_kg, status, source, price_idr,
            sold_count, rating_score, industry_angle, source_url
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        ) ON CONFLICT(sku) DO UPDATE SET
            product_title = excluded.product_title,
            raw_source_title = excluded.raw_source_title,
            keywords = excluded.keywords,
            image_1 = excluded.image_1,
            image_2 = excluded.image_2,
            image_3 = excluded.image_3,
            image_4 = excluded.image_4,
            image_5 = excluded.image_5,
            image_6 = excluded.image_6,
            price_usd = excluded.price_usd,
            price_idr = excluded.price_idr,
            sold_count = excluded.sold_count,
            rating_score = excluded.rating_score,
            updated_at = CURRENT_TIMESTAMP;
        """, (
            sku, model, pname, pname, "Shoes & Accessories > Men's Shoes > Boots",
            "AP Boots Lazada", kw_info['keywords'],
            dedup_imgs[0], dedup_imgs[1], dedup_imgs[2], dedup_imgs[3], dedup_imgs[4], dedup_imgs[5],
            f"<p>Official AP Boots Lazada - {pname}. Guaranteed 100% genuine export quality.</p>",
            price_usd, price_usd, round(price_usd*0.95, 2), round(price_usd*0.90, 2),
            100, 500, 1000, 1.7, "Ready for Upload", "lazada", price_idr,
            sold_count, rating, kw_info['target_industry_angle'], url
        ))
        inserted += 1

    conn.commit()
    print(f"  [OK] Processed exactly {inserted} unique Lazada products (0 duplicates).")
    return inserted

def sync_800_matrix(conn, lookup_images):
    """
    Loads 810 matrix listings & keywords into SQLite and combines them
    with high-resolution product photos from the multi-source image bank.
    """
    matrix_file = os.path.join(INPUT_DIR, "alibaba-800-listing-matrix.xlsx")
    if not os.path.exists(matrix_file):
        print(f"[WARN] 800 Matrix file not found: {matrix_file}")
        return 0, 0

    cur = conn.cursor()
    print(f"--> Combining Alibaba 800 Matrix with Platform Images: {os.path.basename(matrix_file)}")

    # 1. Keywords Sheet
    df_kw = pd.read_excel(matrix_file, sheet_name='Keyword_Manager_Database')
    kw_count = 0
    for _, r in df_kw.iterrows():
        sku = str(r.get('Unique_SKU_Code', '')).strip()
        if not sku:
            continue
        cur.execute("""
        INSERT INTO alibaba_keywords (
            unique_sku_code, base_product_name, target_industry_angle,
            alibaba_product_title, primary_keyword_1, primary_keyword_2,
            primary_keyword_3, longtail_keywords
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(unique_sku_code) DO UPDATE SET
            base_product_name = excluded.base_product_name,
            target_industry_angle = excluded.target_industry_angle,
            alibaba_product_title = excluded.alibaba_product_title,
            primary_keyword_1 = excluded.primary_keyword_1,
            primary_keyword_2 = excluded.primary_keyword_2,
            primary_keyword_3 = excluded.primary_keyword_3,
            longtail_keywords = excluded.longtail_keywords;
        """, (
            sku,
            str(r.get('Base_Product_Name', '')).strip(),
            str(r.get('Target_Industry_Angle', '')).strip(),
            str(r.get('Alibaba_Product_Title', '')).strip(),
            str(r.get('Primary_Keyword_1', '')).strip(),
            str(r.get('Primary_Keyword_2', '')).strip(),
            str(r.get('Primary_Keyword_3', '')).strip(),
            str(r.get('Longtail_Keywords', '')).strip()
        ))
        kw_count += 1

    # 2. 800 Listings Master Sheet
    df_mat = pd.read_excel(matrix_file, sheet_name='800_Listings_Master')
    mat_count = 0
    combined_images_count = 0

    for _, r in df_mat.iterrows():
        lid = str(r.get('Listing_ID', '')).strip()
        if not lid or lid == 'nan':
            lid = str(r.get('Unique_SKU_Code', f"800-MAT-{mat_count+1}")).strip()

        base_name = str(r.get('Base_Product_Name', '')).strip()
        base_sku = str(r.get('Base_SKU', '')).strip()

        # Combine images from the platform input image bank
        cand_imgs = lookup_images(base_name, max_count=6)
        if not cand_imgs and base_sku:
            cand_imgs = lookup_images(base_sku, max_count=6)

        # Fallback to category catalog default if needed
        if not cand_imgs:
            cand_imgs = ["https://p16-images-comn-sg.tokopedia-static.net/tos-alisg-i-aphluv4xwc-sg/c134f882bb9646459cfbb06e2a19ddb0~tplv-aphluv4xwc-white-pad-v1:1600:1600.jpeg"]
        else:
            combined_images_count += 1

        while len(cand_imgs) < 6:
            cand_imgs.append("")

        cur.execute("""
        INSERT INTO alibaba_matrix_800 (
            listing_id, unique_sku_code, base_sku, base_product_name, angle_id,
            target_industry_angle, alibaba_product_title, alibaba_category, brand,
            place_of_origin, upper_material, outsole_material, toe_style, boot_height,
            colors, size_range, key_features, target_application, primary_keyword_1,
            primary_keyword_2, primary_keyword_3, longtail_keywords, moq_pairs,
            price_tier1_usd, price_tier2_usd, price_tier3_usd, pairs_per_carton,
            carton_dimensions, carton_gross_weight_kg, carton_cbm, port_of_loading,
            estimated_lead_time, tailored_html_description,
            image_1, image_2, image_3, image_4, image_5, image_6
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(listing_id) DO UPDATE SET
            alibaba_product_title = excluded.alibaba_product_title,
            primary_keyword_1 = excluded.primary_keyword_1,
            primary_keyword_2 = excluded.primary_keyword_2,
            primary_keyword_3 = excluded.primary_keyword_3,
            longtail_keywords = excluded.longtail_keywords,
            price_tier1_usd = excluded.price_tier1_usd,
            image_1 = excluded.image_1,
            image_2 = excluded.image_2,
            image_3 = excluded.image_3,
            image_4 = excluded.image_4,
            image_5 = excluded.image_5,
            image_6 = excluded.image_6;
        """, (
            lid,
            str(r.get('Unique_SKU_Code', '')).strip(),
            base_sku,
            base_name,
            str(r.get('Angle_ID', '')).strip(),
            str(r.get('Target_Industry_Angle', '')).strip(),
            str(r.get('Alibaba_Product_Title', '')).strip(),
            str(r.get('Alibaba_Category', '')).strip(),
            str(r.get('Brand', 'AP Boots')).strip(),
            str(r.get('Place_of_Origin', 'Surabaya, Indonesia')).strip(),
            str(r.get('Upper_Material', 'PVC / Synthetic Rubber')).strip(),
            str(r.get('Outsole_Material', 'Nitrile Rubber / Heavy Duty PVC')).strip(),
            str(r.get('Toe_Style', 'Plain Toe / Steel Toe')).strip(),
            str(r.get('Boot_Height', 'Mid-Calf / High')).strip(),
            str(r.get('Colors', 'Black; Green; White; Yellow')).strip(),
            str(r.get('Size_Range', 'EU 38 - 44')).strip(),
            str(r.get('Key_Features', 'Waterproof, Anti-Slip')).strip(),
            str(r.get('Target_Application', 'Industrial Safety & Agriculture')).strip(),
            str(r.get('Primary_Keyword_1', '')).strip(),
            str(r.get('Primary_Keyword_2', '')).strip(),
            str(r.get('Primary_Keyword_3', '')).strip(),
            str(r.get('Longtail_Keywords', '')).strip(),
            int(r.get('MOQ_Pairs', 60) or 60),
            float(r.get('Price_Tier1_USD (MOQ 60)', 5.50) or 5.50),
            float(r.get('Price_Tier2_USD (MOQ 300)', 4.80) or 4.80),
            float(r.get('Price_Tier3_USD (MOQ 1200)', 4.20) or 4.20),
            int(r.get('Pairs_Per_Carton', 12) or 12),
            str(r.get('Carton_Dimensions', '60 x 42 x 38 cm')).strip(),
            float(r.get('Carton_Gross_Weight_KG', 18.0) or 18.0),
            float(r.get('Carton_CBM', 0.095) or 0.095),
            str(r.get('Port_of_Loading', 'Tanjung Perak, Surabaya, Indonesia')).strip(),
            str(r.get('Estimated_Lead_Time', '7-21 Days')).strip(),
            str(r.get('Tailored_HTML_Description', '')).strip(),
            cand_imgs[0], cand_imgs[1], cand_imgs[2], cand_imgs[3], cand_imgs[4], cand_imgs[5]
        ))
        mat_count += 1

    conn.commit()
    print(f"  [OK] Synced {kw_count} keywords and {mat_count} matrix listings combined with platform photos ({combined_images_count} listings directly matched).")
    return kw_count, mat_count

def run_sync_pipeline():
    """Main execution function that syncs everything into SQLite."""
    print("=================================================================")
    print(" STARTING COMPLETE DATABASE INGESTION & PLATFORM COMBINATION")
    print(f" Database: {DB_PATH}")
    print(f" Source Folder: {INPUT_DIR}")
    print("=================================================================")

    conn = get_db()
    init_schemas(conn)
    cleanup_duplicate_marketplace_data(conn)

    # 1. Build Multi-Source Image Bank for Combination
    image_lookup = build_comprehensive_image_bank()

    # 2. Ingest Platform Datasets without Duplicate Product Names
    tok_cnt = sync_tokopedia(conn)
    shp_cnt = sync_shopee(conn, image_lookup)
    bli_cnt = sync_blibli(conn)
    laz_cnt = sync_lazada(conn)

    # 3. Combine 800 Matrix with Platform Product Photos
    kw_cnt, mat_cnt = sync_800_matrix(conn, image_lookup)

    # Grand totals
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM products")
    total_products = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM marketplace_raw")
    total_raw = cur.fetchone()[0]

    cur.execute("SELECT source, count(*) FROM products GROUP BY source")
    breakdown = {r[0]: r[1] for r in cur.fetchall()}

    conn.close()

    summary = {
        "success": True,
        "database": DB_PATH,
        "total_catalog_products": total_products,
        "total_raw_scraped": total_raw,
        "tokopedia_products": tok_cnt,
        "shopee_products": shp_cnt,
        "blibli_products": bli_cnt,
        "lazada_products": laz_cnt,
        "matrix_800_listings": mat_cnt,
        "matrix_keywords": kw_cnt,
        "breakdown": breakdown,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    print("\n=================================================================")
    print(" DATABASE INGESTION & PLATFORM COMBINATION COMPLETE!")
    print(f" Total Products in Catalog: {total_products}")
    print(f" Total Raw Marketplace Items: {total_raw} (Tokopedia: {tok_cnt}, Shopee: {shp_cnt}, Blibli: {bli_cnt}, Lazada: {laz_cnt})")
    print(f" 800 Matrix Listings in DB: {mat_cnt} (Combined with Platform Images)")
    print(f" Breakdown by Source: {breakdown}")
    print("=================================================================")
    return summary

if __name__ == '__main__':
    run_sync_pipeline()
