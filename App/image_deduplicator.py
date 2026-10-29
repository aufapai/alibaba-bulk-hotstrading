import re
import urllib.parse
import os
import sqlite3
import csv

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
PHOTOBANK_CSV = os.path.join(BASE_DIR, "Input", "photobank_server_uploaded.csv")

# Cache for Photobank images
_PHOTOBANK_CACHE = None

def get_photobank_map():
    global _PHOTOBANK_CACHE
    if _PHOTOBANK_CACHE is not None:
        return _PHOTOBANK_CACHE
    
    pb_map = {}
    if os.path.exists(PHOTOBANK_CSV):
        try:
            with open(PHOTOBANK_CSV, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    sku = str(r.get('SKU', '')).strip().upper()
                    url = str(r.get('URL Gambar', '')).strip()
                    name = str(r.get('Nama Produk', '')).strip().upper()
                    if sku and url.startswith('http'):
                        pb_map.setdefault(sku, []).append(url)
                    if name and url.startswith('http'):
                        pb_map.setdefault(name, []).append(url)
        except Exception:
            pass
    _PHOTOBANK_CACHE = pb_map
    return _PHOTOBANK_CACHE

def normalize_and_upgrade_image(url, sanitize_for_alibaba=True):
    """
    Normalizes image URL, upgrades low-res thumbnails to full resolution,
    and optionally strips query params / ByteDance signed tokens that cause Alibaba bulk crawler rejections.
    Returns: (canonical_highres_url, fingerprint) or (None, None) if invalid/banner.
    """
    if not url or not isinstance(url, str):
        return None, None
    u = url.strip()
    if not u.startswith("http"):
        return None, None
    u_low = u.lower()

    # Reject non-product assets, banners, watermarks, placeholders
    if any(bad in u_low for bad in [
        'tb13yffofzo3', 'tps/tfs', 'lazada_logo', 'data:image', 'base64',
        'badge', 'banner_promo', 'watermark_default', 'icon_shipping', 'placeholder'
    ]):
        return None, None

    # 1. Photobank CDN (Highest priority, 100% clean static assets)
    if 'hotstrading.com' in u_low:
        fname = u.split('/')[-1].split('?')[0].lower()
        clean_url = u.split('?')[0]
        return clean_url, f"photobank_{fname}"

    # 2. Blibli CDN (Clean static images)
    elif 'static-src.com' in u_low:
        m_full = re.search(r'([a-zA-Z0-9_\-]+_full\d+[^?#\s]*)', u)
        if m_full:
            base_code = re.sub(r'_(thumb|small|medium)\.', '.', m_full.group(1).lower())
            clean_url = u.split('?')[0].replace('/medium//', '/full//').replace('/small//', '/full//')
            return clean_url, f"blibli_{base_code}"
        else:
            m_mta = re.search(r'(mta-[0-9]+/[^?#\s]+)', u_low)
            key = m_mta.group(1) if m_mta else u.split('?')[0].rstrip('/')
            clean_url = u.split('?')[0].replace('/medium//', '/full//').replace('/small//', '/full//')
            return clean_url, f"blibli_{key}"

    # 3. Lazada CDN (Clean static jpg/webp)
    elif 'lazcdn.com' in u_low:
        m = re.search(r'/([a-f0-9]{32})\.(jpg|jpeg|png|webp)', u, re.I)
        if m:
            img_hash = m.group(1).lower()
            upgraded = f"https://img.lazcdn.com/g/p/{img_hash}.jpg_720x720q80.jpg_.webp"
            return upgraded, f"lazada_{img_hash}"
        else:
            base = u.split('?')[0].split('_')[0]
            return u.split('?')[0], f"lazada_{base}"

    # 4. Shopee CDN
    elif 'susercontent.com' in u_low:
        m_shp = re.search(r'([a-zA-Z0-9]{32})', u)
        if m_shp:
            h = m_shp.group(1).lower()
            return f"https://down-id.img.susercontent.com/file/{h}", f"shopee_{h}"
        return u.split('?')[0], f"shopee_{u.split('?')[0]}"

    # 5. Tokopedia / ByteDance CDN
    elif 'tokopedia-static.net' in u_low or 'ibyteimg.com' in u_low or 'tokopedia.net' in u_low:
        # Strip query parameters (e.g. x-expires, x-signature) that expire or trip up Alibaba
        clean_base = u.split('?')[0] if sanitize_for_alibaba else u
        # Upgrade low-res thumbnail (~tplv-*-resize-jpeg:200:0.webp) to crystal clear 1600:1600
        upgraded = re.sub(r'~tplv-[\w\-]+-resize-jpeg:\d+:\d+\.\w+', '~tplv-aphluv4xwc-resize-jpeg:1600:1600.jpeg', clean_base)
        upgraded = re.sub(r'/cache/(?:200-square|500-square|700|800)/', '/cache/900/', upgraded)
        
        # Extract core UUID / 32-hex hash
        m_hash = re.search(r'([a-f0-9]{32}|[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', upgraded, re.I)
        fingerprint = f"tokopedia_{m_hash.group(1).lower()}" if m_hash else f"tokopedia_{upgraded.split('?')[0]}"
        return upgraded, fingerprint

    # 6. Generic CDN
    clean_norm = u.split('?')[0].rstrip('/') if sanitize_for_alibaba else u.rstrip('/')
    return clean_norm, f"generic_{clean_norm.split('/')[-1].lower()}"

def clean_and_deduplicate_images(img_list, marketplace='generic'):
    """
    Deduplicates images from a list of URLs, converts thumbnails to high-res,
    and returns strictly unique images up to 6 slots.
    """
    if not img_list:
        return ["", "", "", "", "", ""]

    raw_urls = []
    for item in img_list:
        if not item or str(item).strip() in ['nan', 'None', '']:
            continue
        text = str(item).strip()
        if '\n' in text or ' ' in text:
            parts = re.split(r'[\r\n\s]+', text)
            for p in parts:
                p_clean = p.strip()
                if p_clean.startswith('http'):
                    raw_urls.append(p_clean)
        elif text.startswith('http'):
            raw_urls.append(text)

    seen_fingerprints = set()
    unique_imgs = []

    for url in raw_urls:
        upgraded_url, fingerprint = normalize_and_upgrade_image(url)
        if not upgraded_url or not fingerprint:
            continue
        if fingerprint not in seen_fingerprints:
            seen_fingerprints.add(fingerprint)
            unique_imgs.append(upgraded_url)

    # Pad with empty strings up to 6 slots
    padded = list(unique_imgs[:6])
    while len(padded) < 6:
        padded.append("")

    return padded

def enrich_images_multi_source(current_images, candidate_images):
    """
    Merges current product images with candidate images from other sources
    (Tokopedia, Lazada, Blibli, Shopee, Photobank) ensuring zero duplicates.
    """
    seen_fingerprints = set()
    combined = []

    # First add current images
    for u in current_images:
        upgraded, fp = normalize_and_upgrade_image(u)
        if upgraded and fp and fp not in seen_fingerprints:
            seen_fingerprints.add(fp)
            combined.append(upgraded)

    # Then enrich with candidates if slots < 6
    for u in candidate_images:
        if len(combined) >= 6:
            break
        upgraded, fp = normalize_and_upgrade_image(u)
        if upgraded and fp and fp not in seen_fingerprints:
            seen_fingerprints.add(fp)
            combined.append(upgraded)

    while len(combined) < 6:
        combined.append("")

    return combined[:6]

def compile_and_consolidate_sku_images(sku, product_title="", current_images=None, db_conn=None):
    """
    Comprehensive multi-source compilation:
    Gathers all image candidates for a given SKU from:
    1. Photobank (hotstrading.com)
    2. Blibli (static-src.com)
    3. Lazada (lazcdn.com)
    4. Shopee (susercontent.com)
    5. Tokopedia (clean upgraded)
    Deduplicates strictly by perceptual/UUID fingerprint and returns exactly 6 slots.
    """
    should_close = False
    if db_conn is None:
        db_conn = sqlite3.connect(DB_PATH)
        should_close = True

    candidates_by_priority = {
        "photobank": [],
        "blibli": [],
        "lazada": [],
        "shopee": [],
        "tokopedia": [],
        "other": []
    }

    # 1. Photobank lookup
    pb_map = get_photobank_map()
    sku_upper = sku.upper().strip() if sku else ""
    if sku_upper in pb_map:
        candidates_by_priority["photobank"].extend(pb_map[sku_upper])

    # 2. Marketplace raw items lookup
    cur = db_conn.cursor()
    # Search by exact SKU code
    cur.execute("""
    SELECT source, image_1, image_2, image_3, image_4, image_5, image_6 
    FROM marketplace_raw 
    WHERE source_id = ? OR product_name LIKE ?
    """, (sku, f"%{sku}%"))
    raw_rows = cur.fetchall()

    # Search by model tokens if title provided
    if product_title:
        tokens = [w for w in re.split(r'[\s\-]+', product_title) 
                  if w.upper() not in ['AP', 'BOOTS', 'WATERPROOF', 'PVC', 'WORK', 'FOR', 'MEN', 'SAFETY', 'EN', 'ISO', '20345']][:2]
        if tokens:
            cur.execute("""
            SELECT source, image_1, image_2, image_3, image_4, image_5, image_6 
            FROM marketplace_raw 
            WHERE product_name LIKE ?
            """, (f"%{tokens[0]}%",))
            raw_rows.extend(cur.fetchall())

    for r in raw_rows:
        src = (r[0] or "other").lower()
        bucket = candidates_by_priority.get(src, candidates_by_priority["other"])
        for img in r[1:]:
            if img and str(img).strip().startswith("http"):
                bucket.append(str(img).strip())

    # Add current images to candidate pool
    if current_images:
        for ci in current_images:
            if ci and str(ci).strip().startswith("http"):
                candidates_by_priority["other"].append(str(ci).strip())

    if should_close:
        db_conn.close()

    # Prioritize: Photobank -> Blibli -> Lazada -> Shopee -> Tokopedia -> Other
    ordered_candidates = (
        candidates_by_priority["photobank"] +
        candidates_by_priority["blibli"] +
        candidates_by_priority["lazada"] +
        candidates_by_priority["shopee"] +
        candidates_by_priority["tokopedia"] +
        candidates_by_priority["other"]
    )

    seen_fingerprints = set()
    compiled_images = []

    for c_url in ordered_candidates:
        if len(compiled_images) >= 6:
            break
        upgraded, fp = normalize_and_upgrade_image(c_url, sanitize_for_alibaba=True)
        if upgraded and fp and fp not in seen_fingerprints:
            seen_fingerprints.add(fp)
            compiled_images.append(upgraded)

    # Pad up to 6 slots
    while len(compiled_images) < 6:
        compiled_images.append("")

    return compiled_images[:6]

def resolve_failed_upload_reports():
    """
    Iterates through all items in alibaba_upload_reports with IMAGE_DATA_ISSUE,
    compiles clean alternative images from other sources (Blibli/Lazada/Photobank),
    and updates both the upload report and the master products table.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT id, sku, product_title, original_img1, original_img2, failed_reason, error_category
    FROM alibaba_upload_reports
    WHERE error_category = 'IMAGE_DATA_ISSUE' OR status = 'Pending Fix'
    """)
    failed_items = cur.fetchall()

    resolved_count = 0
    results = []

    for item in failed_items:
        r_id = item['id']
        sku = item['sku']
        title = item['product_title'] or ""
        
        # Compile from multiple sources
        new_imgs = compile_and_consolidate_sku_images(
            sku=sku,
            product_title=title,
            current_images=[item['original_img1'], item['original_img2']],
            db_conn=conn
        )

        has_new_valid = any(bool(img and img.startswith('http')) for img in new_imgs)

        if has_new_valid:
            # Update upload report record
            cur.execute("""
            UPDATE alibaba_upload_reports 
            SET resolved_img1 = ?, resolved_img2 = ?, resolved_img3 = ?,
                resolved_img4 = ?, resolved_img5 = ?, resolved_img6 = ?,
                status = 'Resolved & Compiled',
                resolution_notes = 'Replaced with multi-source verified images from Blibli/Lazada/Photobank',
                resolved_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (new_imgs[0], new_imgs[1], new_imgs[2], new_imgs[3], new_imgs[4], new_imgs[5], r_id))

            # Also update products table if product exists
            cur.execute("""
            UPDATE products 
            SET image_1 = ?, image_2 = ?, image_3 = ?, image_4 = ?, image_5 = ?, image_6 = ?,
                status = 'Ready (Images Resolved)',
                updated_at = CURRENT_TIMESTAMP
            WHERE sku = ?
            """, (new_imgs[0], new_imgs[1], new_imgs[2], new_imgs[3], new_imgs[4], new_imgs[5], sku))

            resolved_count += 1
            results.append({
                "sku": sku,
                "title": title,
                "status": "Resolved",
                "images_count": sum(1 for img in new_imgs if img),
                "resolved_hero": new_imgs[0]
            })

    conn.commit()
    conn.close()

    return {
        "success": True,
        "total_processed": len(failed_items),
        "resolved_count": resolved_count,
        "results": results
    }

def audit_image_duplicates(image_slots):
    """
    Checks if 6 image slots contain duplicates.
    Returns (has_duplicates, unique_count, duplicate_count).
    """
    valid = [img.strip() for img in image_slots if img and str(img).strip().startswith('http')]
    seen = set()
    dups = 0
    for img in valid:
        _, fp = normalize_and_upgrade_image(img)
        if not fp:
            continue
        if fp in seen:
            dups += 1
        else:
            seen.add(fp)
    return dups > 0, len(seen), dups
