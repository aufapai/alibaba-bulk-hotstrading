"""
HOTS SYSTEM CATALOG BRIDGE
==========================
Synchronizes and ingests products from the HOTS Trading system database
(`Database/hotj4796_hotstrading (4).sql` or live MySQL connection)
into the Alibaba & Multi-Marketplace Master database (`Database/alibaba_master.db`).

Features:
- Parses system products, specifications, certifications, and categories.
- Sanitizes and extracts multi-source image JSON arrays.
- Computes live FOB USD prices alongside domestic IDR base prices using real-time Forex.
- Auto-maps products to Alibaba category taxonomy and Accio industry angles.
"""

import os
import re
import json
import sqlite3
import sys

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
SQL_DUMP_PATH = os.path.join(BASE_DIR, "Database", "hotj4796_hotstrading (4).sql")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from currency_calculator import get_live_usd_idr_rate, calculate_packaging_and_carton
from image_deduplicator import normalize_and_upgrade_image

def get_master_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def parse_system_catalog_from_sql(sql_path=SQL_DUMP_PATH):
    """
    Parses product records and specifications from the system MySQL dump.
    """
    if not os.path.exists(sql_path):
        return {"success": False, "error": f"SQL file not found at {sql_path}", "products": []}

    try:
        with open(sql_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return {"success": False, "error": str(e), "products": []}

    # Extract products table insert rows
    # Format: INSERT INTO `products` (...) VALUES (...)
    product_section_match = re.search(r"INSERT INTO `products`[\s\S]*?VALUES\s*([\s\S]+?);\n", content)
    if not product_section_match:
        return {"success": False, "error": "No INSERT INTO `products` found in SQL dump", "products": []}

    raw_values = product_section_match.group(1).strip()
    lines = [line.strip().rstrip(",") for line in raw_values.split("\n") if line.strip().startswith("(")]
    
    products = []
    for line in lines:
        if line.endswith(";"):
            line = line[:-1]
        if line.startswith("(") and line.endswith(")"):
            line = line[1:-1]
        
        # Parse fields using csv/sql reader logic
        fields = parse_sql_row_fields(line)
        if len(fields) >= 16:
            p_id = int(fields[0]) if fields[0].isdigit() else 0
            p_code = fields[1].strip("'")
            p_name = fields[2].strip("'")
            p_desc = fields[5].strip("'").replace("\\n", "\n").replace("\\r", "\r")
            p_cat = fields[6].strip("'") if fields[6] != "NULL" else "Safety Footwear"
            p_status = fields[7].strip("'")
            p_img_single = fields[10].strip("'") if fields[10] != "NULL" else ""
            p_images_json = fields[11].strip("'") if fields[11] != "NULL" else "[]"
            p_moq = fields[12].strip("'") if fields[12] != "NULL" else "100"
            try:
                p_price_idr = float(fields[15]) if fields[15] != "NULL" else 0.0
            except ValueError:
                p_price_idr = 0.0

            # Parse images JSON
            images = []
            if p_images_json and p_images_json.startswith("["):
                try:
                    # Clean escaped slashes
                    clean_json = p_images_json.replace("\\/", "/").replace('\\"', '"')
                    images = json.loads(clean_json)
                except Exception:
                    images = [p_img_single] if p_img_single else []
            elif p_img_single:
                images = [p_img_single]

            # Categorization & Industry Angle mapping
            cat_group, angle = categorize_system_product(p_name, p_cat, p_desc)

            products.append({
                "system_id": p_id,
                "sku": p_code or f"HOTS-{p_id:04d}",
                "name": p_name,
                "description": p_desc,
                "category_system": p_cat,
                "category_group": cat_group,
                "industry_angle": angle,
                "status": p_status,
                "base_price_idr": p_price_idr,
                "moq": p_moq,
                "image_url": p_img_single,
                "images": images
            })

    return {
        "success": True,
        "total_parsed": len(products),
        "source": os.path.basename(sql_path),
        "products": products
    }

def parse_sql_row_fields(row_str):
    """
    Splits SQL values accounting for quotes and commas inside text.
    """
    fields = []
    current = []
    in_quote = False
    quote_char = None
    escape = False

    for ch in row_str:
        if escape:
            current.append(ch)
            escape = False
            continue

        if ch == "\\":
            escape = True
            current.append(ch)
            continue

        if ch in ("'", '"'):
            if not in_quote:
                in_quote = True
                quote_char = ch
            elif quote_char == ch:
                in_quote = False
                quote_char = None
            current.append(ch)
        elif ch == "," and not in_quote:
            fields.append("".join(current).strip())
            current = []
        else:
            current.append(ch)

    if current:
        fields.append("".join(current).strip())

    return fields

def categorize_system_product(name, category, description):
    """
    Maps system product to standard Alibaba category group and Accio industry angle.
    """
    text = f"{name} {category} {description}".lower()

    if "s5" in text or "s4" in text or "safety" in text or "toe cap" in text or "metaguard" in text:
        return "AP Safety Boots", "Heavy Industrial & Construction"
    elif "chef" in text or "kitchen" in text:
        return "AP Chef Series", "Food Industry & Culinary"
    elif "medic" in text or "hospital" in text or "cleanroom" in text or "autoclave" in text:
        return "AP Medic Series", "Medical & Laboratory Cleanroom"
    elif "terra" in text or "eco" in text or "forest" in text or "army" in text:
        return "AP Terra Series", "Agricultural & Commercial Mud Utility"
    elif "orca" in text:
        return "AP Orca Series", "Fishery & Cold-Storage Wet Operations"
    elif "moto" in text or "bike" in text:
        return "AP Casual & Biker", "Motorcycle & Commuter Wet Weather"
    elif "kids" in text or "safari" in text:
        return "AP Kids Boots", "All-Weather Rain Utility"
    elif "clogs" in text or "sandal" in text or "slop" in text:
        return "AP Sandals & Clogs", "Hospitality & Leisure Slip-On"
    else:
        return "AP Classic Boots", "All-Weather Rain Utility"

def sync_system_products_to_master(sql_path=SQL_DUMP_PATH, overwrite_existing=False):
    """
    Ingests all products from the system catalog into `alibaba_master.db`.
    Preserves multi-source images, computes USD FOB price based on live forex,
    and updates/inserts cleanly.
    """
    parsed = parse_system_catalog_from_sql(sql_path)
    if not parsed["success"] or not parsed["products"]:
        return {"success": False, "error": parsed.get("error", "No products to sync")}

    rate, src_name, updated_at = get_live_usd_idr_rate()

    conn = get_master_db()
    cur = conn.cursor()

    inserted = 0
    updated = 0
    skipped = 0

    for p in parsed["products"]:
        sku = p["sku"]
        name = p["name"]
        idr = p["base_price_idr"]
        usd = round(idr / rate, 2) if idr and rate > 0 else 5.50
        if usd < 1.0:
            usd = 5.50

        # Sanitize images
        clean_imgs = []
        for img in p["images"]:
            norm_url, _ = normalize_and_upgrade_image(img, sanitize_for_alibaba=True)
            if norm_url and norm_url not in clean_imgs:
                clean_imgs.append(norm_url)

        img1 = clean_imgs[0] if len(clean_imgs) > 0 else (p["image_url"] or "")
        img2 = clean_imgs[1] if len(clean_imgs) > 1 else ""
        img3 = clean_imgs[2] if len(clean_imgs) > 2 else ""
        img4 = clean_imgs[3] if len(clean_imgs) > 3 else ""
        img5 = clean_imgs[4] if len(clean_imgs) > 4 else ""
        img6 = clean_imgs[5] if len(clean_imgs) > 5 else ""

        # Check if exists in master
        cur.execute("SELECT id FROM products WHERE sku = ? OR model_number = ?", (sku, sku))
        existing = cur.fetchone()

        if existing:
            if overwrite_existing:
                cur.execute("""
                UPDATE products SET
                    product_title = COALESCE(product_title, ?),
                    price_idr = ?,
                    price_usd = CASE WHEN price_usd IS NULL OR price_usd <= 0 THEN ? ELSE price_usd END,
                    category_group = ?,
                    industry_angle = ?,
                    image_1 = CASE WHEN image_1 IS NULL OR image_1 = '' THEN ? ELSE image_1 END,
                    image_2 = CASE WHEN image_2 IS NULL OR image_2 = '' THEN ? ELSE image_2 END,
                    image_3 = CASE WHEN image_3 IS NULL OR image_3 = '' THEN ? ELSE image_3 END,
                    image_4 = CASE WHEN image_4 IS NULL OR image_4 = '' THEN ? ELSE image_4 END,
                    image_5 = CASE WHEN image_5 IS NULL OR image_5 = '' THEN ? ELSE image_5 END,
                    image_6 = CASE WHEN image_6 IS NULL OR image_6 = '' THEN ? ELSE image_6 END,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (name, idr, usd, p["category_group"], p["industry_angle"], img1, img2, img3, img4, img5, img6, existing["id"]))
                updated += 1
            else:
                # Fill missing price_idr or images
                cur.execute("""
                UPDATE products SET
                    price_idr = COALESCE(price_idr, ?),
                    category_group = COALESCE(category_group, ?),
                    industry_angle = COALESCE(industry_angle, ?)
                WHERE id = ?
                """, (idr, p["category_group"], p["industry_angle"], existing["id"]))
                skipped += 1
        else:
            # Insert new product from HOTS system
            default_img = img1 if (img1 and img1.startswith("http")) else "https://hotstrading.com/backend/uploads/placeholder.webp"
            desc_html = f"<p><strong>{name}</strong></p><p>{p['description'] or 'High-quality industrial footwear engineered by AP Boots Indonesia.'}</p>"

            cur.execute("""
            INSERT INTO products (
                sku, model_number, alibaba_product_id, product_title, category, category_group,
                price_usd, price_idr, gross_weight_kg, moq1, tier1_price, tier2_price, tier3_price,
                color, size_range, gender, image_1, image_2, image_3, image_4, image_5, image_6,
                description_html, source, status, industry_angle, is_flagship
            ) VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?
            )
            """, (
                sku, sku, f"SYS-{p['system_id']}", name, p["category_group"], p["category_group"],
                usd, idr, 1.8, int(p["moq"]) if p["moq"].isdigit() else 100, usd, round(usd * 0.95, 2), round(usd * 0.90, 2),
                "Black / Yellow / Multi", "EU 38-45", "Men / Unisex",
                default_img, img2, img3, img4, img5, img6,
                desc_html, "hots_system_catalog", "draft", p["industry_angle"], 0
            ))
            inserted += 1

    conn.commit()
    conn.close()

    return {
        "success": True,
        "total_source_products": len(parsed["products"]),
        "inserted": inserted,
        "updated": updated,
        "skipped": skipped,
        "live_exchange_rate": rate,
        "forex_source": src_name
    }

if __name__ == "__main__":
    print("[INFO] Testing parse_system_catalog_from_sql...")
    res = parse_system_catalog_from_sql()
    print(f"Parsed {res.get('total_parsed', 0)} products from system database.")
    if res["products"]:
        sample = res["products"][0]
        print(f"Sample SKU: {sample['sku']} | Name: {sample['name']} | IDR: {sample['base_price_idr']} | Images: {len(sample['images'])}")
