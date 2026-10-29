"""
Shopee Asset Manager & Image Pipeline
PT Indo Sukses Semesta - HOTS Trading / PT Waru Gunung

Handles:
1. Product-specific asset folders (1 folder per product):
   Shopee_Product_Assets/<Sanitized_Product_Name>/
     ├── hero_<Sanitized_Product_Name>.webp
     ├── side_<Sanitized_Product_Name>.webp
     └── <Sanitized_Product_Name>.json
2. Automatic downloading of Shopee Official images + WEBP conversion
3. Side-view photo matching from local catalog image bank (Images_Produk_Katalog)
4. JSON generation with side-to-side white background specs & Alibaba B2B function
5. Dynamic image upload/input handler from Web GUI
"""

import os
import re
import json
import csv
import urllib.request
import sqlite3
from io import BytesIO
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "Shopee_Product_Assets")
CATALOG_IMAGES_DIR = os.path.join(BASE_DIR, "Images_Produk_Katalog")
SHOPEE_APBOOTS_CSV = os.path.join(BASE_DIR, "Input", "shopee-co-id-2026-10-apboots.csv")
SHOPEE_PETROVA_CSV = os.path.join(BASE_DIR, "Input", "shopee-co-id-2026-10-petrova.csv")
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")

# User agent for downloading Shopee CDN images
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def ensure_assets_dir():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR, exist_ok=True)
    return ASSETS_DIR

def sanitize_name(name):
    """Sanitize product name for folder and file system naming."""
    if not name:
        return "Unnamed_Product"
    # Replace illegal characters
    cleaned = re.sub(r'[\\/*?:"<>|]', '', name)
    # Replace whitespace, hyphens, and periods with single underscore
    cleaned = re.sub(r'[\s\-.]+', '_', cleaned.strip())
    cleaned = re.sub(r'_+', '_', cleaned).strip('_.')
    return cleaned[:100]

def get_product_folder(product_name):
    """Return the dedicated directory path for a product."""
    folder_name = sanitize_name(product_name)
    folder_path = os.path.join(ASSETS_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_name, folder_path

def download_image_as_webp(image_url, output_path, max_size=(1000, 1000), quality=90):
    """Download image from URL, convert to WEBP with white background, and save."""
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            image_data = resp.read()
        
        img = Image.open(BytesIO(image_data))
        # Convert to RGB with white background if transparent
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Optional thumbnail / square fit
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save as WEBP
        img.save(output_path, "WEBP", quality=quality, method=6)
        return True, None
    except Exception as e:
        return False, str(e)

def save_local_image_as_webp(source_path, output_path, max_size=(1000, 1000), quality=90):
    """Convert and save a local image file as WEBP."""
    try:
        img = Image.open(source_path)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            bg.paste(img, mask=img.split()[3])
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(output_path, "WEBP", quality=quality, method=6)
        return True, None
    except Exception as e:
        return False, str(e)

def find_catalog_side_image(product_name):
    """Find a lateral / side-view photo for the product from Images_Produk_Katalog."""
    if not os.path.exists(CATALOG_IMAGES_DIR):
        return None
        
    files = os.listdir(CATALOG_IMAGES_DIR)
    # Clean tokens from product name
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', product_name).upper()
    tokens = [t for t in cleaned.split() if t not in ['AP', 'BOOTS', 'PETROVA', 'SEPATU', 'BOOT', 'PVC', 'SLIP', 'ON']]
    
    if not tokens:
        return None
        
    candidates = []
    for f in files:
        f_up = f.upper()
        # Look for files containing product tokens and side indicators (_02, _03, _04)
        if all(t in f_up for t in tokens[:2]) if len(tokens) >= 2 else (tokens[0] in f_up):
            candidates.append(f)
            
    if not candidates:
        return None
        
    # Prefer _02.jpg or _03.jpg which are typically side-to-side profile shots
    side_shots = [c for c in candidates if '_02' in c or '_03' in c or '_04' in c]
    chosen = side_shots[0] if side_shots else candidates[0]
    return os.path.join(CATALOG_IMAGES_DIR, chosen)

def create_white_background_side_image(hero_path, output_path):
    """Generate a clean side-view representation on pure white background if no side photo is available."""
    try:
        if not os.path.exists(hero_path):
            return False, "Hero path does not exist"
        img = Image.open(hero_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Create a clean white 1000x1000 canvas
        canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))
        # Resize image to fit nicely centered with margins
        img.thumbnail((880, 880), Image.Resampling.LANCZOS)
        x_offset = (1000 - img.width) // 2
        y_offset = (1000 - img.height) // 2
        canvas.paste(img, (x_offset, y_offset))
        canvas.save(output_path, "WEBP", quality=90, method=6)
        return True, None
    except Exception as e:
        return False, str(e)

def generate_alibaba_product_json(product_data, folder_name, folder_path):
    """
    Generate comprehensive Alibaba B2B JSON specification:
    - Side-to-side white background specs
    - Product function & commercial usage
    - GPSR & PT Waru Gunung compliance
    - Naming conventions: hero_<name>.webp and side_<name>.webp
    """
    raw_name = product_data.get('raw_name', '')
    sku = product_data.get('sku', '')
    brand = product_data.get('brand', 'AP Boots')
    price_idr = product_data.get('price_idr', '')
    sold_count = product_data.get('sold_count', '')
    rating = product_data.get('rating', '4.9')
    hero_url = product_data.get('image_url', '')

    # Derive classification and Alibaba B2B details
    is_petrova = brand.lower() == 'petrova'
    is_safety = any(s in raw_name.upper() for s in ['SAFETY', 'S4', 'S5', 'METAGUARD', 'STRENGTH', 'ULTIMATE'])
    is_clog = any(c in raw_name.upper() for c in ['CLOGS', 'CHEF', 'MEDIC', 'SLOP', 'SANDAL', 'LADIES'])
    is_allbike = any(a in raw_name.upper() for a in ['ALLBIKE', 'MOTO'])

    if is_safety:
        category_group = "Safety Footwear (Impact Resistant)"
        toe_protection = "Steel Toe Cap (Impact Resistant)"
        function_summary = "Industrial site protection, heavy equipment operations, warehouse safety, manufacturing floors."
    elif is_clog:
        category_group = "Workplace Hygiene & Hospitality Footwear"
        toe_protection = "Reinforced Plain Toe (Flexible Work Footwear)"
        function_summary = "Commercial kitchen floors, food preparation zones, cleanroom utility, light laboratory hygiene."
    elif is_allbike:
        category_group = "Water-Resistant Daily Footwear & Splash Protection"
        toe_protection = "Reinforced Plain Toe"
        function_summary = "Courier transit splash protection, rainy day commuting, light outdoor waterproof utility."
    else:
        category_group = "Agricultural & General Industrial Rubber Boots"
        toe_protection = "Reinforced Plain Toe"
        function_summary = "Agricultural harvesting, wet market processing, plantation drainage, construction mud protection."

    # Hero and Side filenames
    hero_filename = f"hero_{folder_name}.webp"
    side_filename = f"side_{folder_name}.webp"
    json_filename = f"{folder_name}.json"

    hero_local_path = os.path.join(folder_path, hero_filename)
    side_local_path = os.path.join(folder_path, side_filename)

    doc = {
        "alibaba_system_metadata": {
            "catalog_standard": "Alibaba B2B Global Trade Standard 2026",
            "platform_compliance": "GPSR EU 2023/988 & PT Waru Gunung Anti-Overclaim Matrix",
            "last_updated": "2026-10-29",
            "source_marketplace": "Shopee Official Store (Verified Reference)"
        },
        "product_identification": {
            "sku": sku,
            "product_name_shopee": raw_name,
            "product_name_sanitized": folder_name,
            "brand": brand,
            "model_series": raw_name.split('-')[0].strip() if '-' in raw_name else raw_name,
            "price_idr": price_idr,
            "sold_count": sold_count,
            "rating_score": rating
        },
        "manufacturer_and_export_entity": {
            "legal_manufacturer": {
                "name": "PT Waru Gunung",
                "facility_location": "Karang Pilang, Mastrip, Surabaya, East Java, Indonesia",
                "jurisdiction": "Republic of Indonesia",
                "role": "OEM / Legal Footwear Manufacturer"
            },
            "export_partner_and_seller_of_record": {
                "name": "PT Indo Sukses Semesta",
                "brand_unit": "HOTS Trading",
                "port_of_loading_primary": "Tanjung Perak Seaport (ID SUB), Surabaya",
                "port_of_loading_secondary": "Tanjung Priok Seaport (ID TKG), Jakarta",
                "role": "Authorized Global Export Distributor & B2B Seller of Record"
            }
        },
        "side_to_side_white_background_specifications": {
            "background_type": "Pure White (#FFFFFF / RGB 255, 255, 255)",
            "camera_angle": "Lateral Profile (Side-to-Side 90-Degree Orthogonal View)",
            "canvas_dimensions": "1000 x 1000 pixels (1:1 Square)",
            "visual_clarity": "Clean isolated silhouette highlighting shaft height, collar curve, vamp contour, and cleated outsole profile",
            "primary_side_asset": side_filename
        },
        "hero_image_specifications": {
            "background_type": "Clean White / Light Neutral Studio",
            "camera_angle": "3/4 Hero Perspective Front-Quarter View",
            "canvas_dimensions": "1000 x 1000 pixels (1:1 Square)",
            "primary_hero_asset": hero_filename,
            "source_shopee_cdn_url": hero_url
        },
        "technical_specifications": {
            "category_classification": category_group,
            "toe_cap_protection": toe_protection,
            "upper_material": "High-Grade Virgin Polyvinyl Chloride (PVC) / EVA Polymer",
            "outsole_tread_pattern": "Heavy-Duty Cleated Lug Outsole with Deep Anti-Slip Siping Channels",
            "waterproofing_level": "Water-Resistant Injection-Molded Seamless Construction",
            "lining_material": "Quick-Drying Breathable Polyester Textile Mesh Lining",
            "size_range_available": "EU 37 - 45 (UK 4 - 11, US 5 - 12)",
            "colorways": "Standard Industrial Black / High-Visibility Yellow / Agriculture Green / Hygiene White",
            "origin_country": "Made in Indonesia"
        },
        "b2b_commercial_functions": {
            "primary_applications": function_summary,
            "recommended_industries": [
                "Agricultural & Commercial Plantations (Oil Palm, Rice, Rubber)",
                "Aquaculture, Marine Processing & Commercial Wet Markets",
                "Civil Construction, Trenching & Heavy Infrastructure",
                "Food Processing Facilities, Commercial Catering & Cleanroom Utility",
                "Municipal Drainage, Disaster Relief & Heavy Monsoon Protection"
            ],
            "banned_claims_and_overclaim_removal": [
                "No unverified CE PPE II/III claims without certified lab documentation",
                "No unverified FDA medical device classification (AP Medic re-positioned to Workplace Hygiene Clogs)",
                "No unverified motorcycle crash PPE claims (Allbike re-positioned to Water-Resistant Shoe Covers)"
            ]
        },
        "packaging_and_logistics": {
            "packaging_type": "Export Grade 5-Ply Corrugated Master Carton",
            "pairs_per_carton": 12 if not is_clog else 24,
            "estimated_carton_weight_kg": 18.5 if not is_clog else 12.0,
            "container_loadability_20ft": "Approx. 3,600 - 4,200 pairs",
            "container_loadability_40ft_hq": "Approx. 8,500 - 9,600 pairs",
            "minimum_order_quantity_moq": "500 pairs (negotiable for trial orders)"
        },
        "local_assets_inventory": {
            "folder_relative_path": f"Shopee_Product_Assets/{folder_name}",
            "hero_image": hero_filename,
            "side_image": side_filename,
            "json_metadata": json_filename
        }
    }

    # Write JSON file into product folder
    json_path = os.path.join(folder_path, json_filename)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)

    return doc, json_path

def process_single_product(row, force_download=False):
    """
    Process one product row from Shopee CSV:
    1. Create folder Shopee_Product_Assets/<Sanitized_Name>/
    2. Download hero_<Sanitized_Name>.webp
    3. Find or generate side_<Sanitized_Name>.webp on white background
    4. Generate <Sanitized_Name>.json
    """
    raw_name = (row.get('name') or row.get('data2') or '').strip()
    if not raw_name:
        return None

    folder_name, folder_path = get_product_folder(raw_name)

    hero_filename = f"hero_{folder_name}.webp"
    side_filename = f"side_{folder_name}.webp"
    json_filename = f"{folder_name}.json"

    hero_path = os.path.join(folder_path, hero_filename)
    side_path = os.path.join(folder_path, side_filename)
    json_path = os.path.join(folder_path, json_filename)

    image_url = row.get('image', '').strip()

    # 1. Hero Image
    hero_downloaded = False
    if not os.path.exists(hero_path) or force_download:
        if image_url:
            ok, err = download_image_as_webp(image_url, hero_path)
            hero_downloaded = ok
    else:
        hero_downloaded = True

    # 2. Side Image
    side_downloaded = False
    if not os.path.exists(side_path) or force_download:
        # Check catalog image bank
        cat_side = find_catalog_side_image(raw_name)
        if cat_side and os.path.exists(cat_side):
            ok, err = save_local_image_as_webp(cat_side, side_path)
            side_downloaded = ok
        elif os.path.exists(hero_path):
            ok, err = create_white_background_side_image(hero_path, side_path)
            side_downloaded = ok
    else:
        side_downloaded = True

    # 3. JSON Generation
    product_data = {
        'raw_name': raw_name,
        'sku': row.get('sku', f"SHP-{folder_name[:12]}"),
        'brand': row.get('brand', 'Petrova' if 'petrova' in raw_name.lower() else 'AP Boots'),
        'price_idr': row.get('data', ''),
        'sold_count': row.get('data3', ''),
        'rating': row.get('data5', '4.9'),
        'image_url': image_url
    }
    doc, _ = generate_alibaba_product_json(product_data, folder_name, folder_path)

    return {
        "folder_name": folder_name,
        "folder_path": folder_path,
        "hero_file": hero_filename,
        "side_file": side_filename,
        "json_file": json_filename,
        "hero_exists": os.path.exists(hero_path),
        "side_exists": os.path.exists(side_path),
        "json_exists": os.path.exists(json_path),
        "raw_name": raw_name
    }

from concurrent.futures import ThreadPoolExecutor, as_completed

def process_all_shopee_products(limit=None, force_download=False, max_workers=8):
    """Batch process all Shopee AP Boots (104) and Petrova (19) products with ThreadPool."""
    ensure_assets_dir()
    rows_to_process = []

    # AP Boots (104 rows)
    if os.path.exists(SHOPEE_APBOOTS_CSV):
        with open(SHOPEE_APBOOTS_CSV, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if limit and len(rows_to_process) >= limit:
                    break
                row['brand'] = 'AP Boots'
                row['sku'] = f"SHP-{i+1:03d}"
                rows_to_process.append(row)

    # Petrova (19 rows)
    if os.path.exists(SHOPEE_PETROVA_CSV):
        with open(SHOPEE_PETROVA_CSV, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for j, row in enumerate(reader):
                if limit and len(rows_to_process) >= limit:
                    break
                row['brand'] = 'Petrova'
                row['sku'] = f"PTR-{j+1:03d}"
                rows_to_process.append(row)

    results = []
    print(f"Starting batch asset generation for {len(rows_to_process)} products with {max_workers} threads...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_product, row, force_download): row for row in rows_to_process}
        for future in as_completed(futures):
            try:
                res = future.result()
                if res:
                    results.append(res)
            except Exception as e:
                print(f"Error processing row: {e}")

    print(f"Successfully processed {len(results)}/{len(rows_to_process)} product asset folders.")
    return results

def get_all_shopee_products_status():
    """Get the live status of all products and their local folder assets."""
    ensure_assets_dir()
    products = []

    def check_status(csv_path, brand_name, sku_prefix):
        if not os.path.exists(csv_path):
            return
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                raw_name = (row.get('name') if brand_name == 'Petrova' else row.get('data2')) or row.get('data2') or ''
                raw_name = raw_name.strip()
                if not raw_name:
                    continue

                folder_name = sanitize_name(raw_name)
                folder_path = os.path.join(ASSETS_DIR, folder_name)

                hero_name = f"hero_{folder_name}.webp"
                side_name = f"side_{folder_name}.webp"
                json_name = f"{folder_name}.json"

                hero_exists = os.path.exists(os.path.join(folder_path, hero_name))
                side_exists = os.path.exists(os.path.join(folder_path, side_name))
                json_exists = os.path.exists(os.path.join(folder_path, json_name))

                sold_cnt = row.get('data2', '') if brand_name == 'Petrova' else row.get('data3', '')
                rating_val = row.get('data4', '4.9') if brand_name == 'Petrova' else row.get('data5', '4.9')

                products.append({
                    "sku": f"{sku_prefix}-{i+1:03d}",
                    "brand": brand_name,
                    "product_name": raw_name,
                    "folder_name": folder_name,
                    "price_idr": row.get('data', ''),
                    "sold_count": sold_cnt,
                    "rating": rating_val or '4.9',
                    "online_image_url": row.get('image', ''),
                    "hero_filename": hero_name,
                    "side_filename": side_name,
                    "json_filename": json_name,
                    "hero_exists": hero_exists,
                    "side_exists": side_exists,
                    "json_exists": json_exists,
                    "folder_exists": os.path.exists(folder_path)
                })

    check_status(SHOPEE_APBOOTS_CSV, "AP Boots", "SHP")
    check_status(SHOPEE_PETROVA_CSV, "Petrova", "PTR")

    return products

def save_uploaded_product_image(folder_name, image_bytes, image_type="hero"):
    """
    Handle user uploading/inputting an image for a product:
    - Auto-saves to Shopee_Product_Assets/<folder_name>/
    - Saves as hero_<folder_name>.webp or side_<folder_name>.webp
    - Re-generates/updates the JSON
    """
    folder_path = os.path.join(ASSETS_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{image_type}_{folder_name}.webp"
    dest_path = os.path.join(folder_path, filename)

    img = Image.open(BytesIO(image_bytes))
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
    img.save(dest_path, "WEBP", quality=92, method=6)

    # Update JSON
    json_path = os.path.join(folder_path, f"{folder_name}.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if image_type == "hero":
                data.setdefault("local_assets_inventory", {})["hero_image"] = filename
            elif image_type == "side":
                data.setdefault("local_assets_inventory", {})["side_image"] = filename
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    return {
        "success": True,
        "filename": filename,
        "folder": folder_name,
        "path": dest_path
    }

if __name__ == "__main__":
    print("Testing Shopee Asset Manager...")
    products = get_all_shopee_products_status()
    print(f"Total products in status: {len(products)}")
    # Process first 5 as a test
    res = process_all_shopee_products(limit=5)
    print(f"Processed sample: {len(res)} products")
    for r in res:
        print(f" - {r['raw_name'][:30]} => Folder: {r['folder_name']} (Hero: {r['hero_exists']}, Side: {r['side_exists']}, JSON: {r['json_exists']})")
