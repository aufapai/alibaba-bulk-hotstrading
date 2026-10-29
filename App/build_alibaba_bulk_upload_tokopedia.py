import openpyxl
import pandas as pd
import re
import os
from analyze_marketplace_inputs import tokopedia_dict, shopee_items

BASE_DIR = r"d:\Work\Hots\Product Input"
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
TEMPLATE_PATH = os.path.join(BASE_DIR, "Template", "Alibaba default template (recommended) (1).xlsx") if os.path.exists(os.path.join(BASE_DIR, "Template", "Alibaba default template (recommended) (1).xlsx")) else os.path.join(BASE_DIR, "Alibaba default template (recommended) (1).xlsx")
OUTPUT_EXCEL = os.path.join(OUTPUT_DIR, "Alibaba_Bulk_Upload_Tokopedia_Master_2026.xlsx")
ROOT_OUTPUT_EXCEL = os.path.join(BASE_DIR, "Alibaba_Bulk_Upload_Tokopedia_Master_2026.xlsx")

# Match Shopee items by name for image fallback (using enriched database)
shopee_lookup = {}
try:
    import sqlite3
    db_file = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
    if os.path.exists(db_file):
        conn_shp = sqlite3.connect(db_file)
        cur_shp = conn_shp.cursor()
        cur_shp.execute("SELECT product_title, image_1, image_2, image_3, image_4, image_5, image_6 FROM products WHERE source = 'shopee'")
        for sr in cur_shp.fetchall():
            s_name = sr[0]
            if s_name:
                s_imgs = [u for u in sr[1:] if u and str(u).startswith('http')]
                clean_s = re.sub(r'[^a-z0-9]', '', str(s_name).lower())
                shopee_lookup[clean_s] = s_imgs
        conn_shp.close()
except Exception:
    pass


def get_public_cdn_url(url):
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if not url.startswith('http'):
        return None
        
    if '.net/' in url:
        path = url.split('.net/')[1].split('?')[0]
    elif '.com/' in url:
        path = url.split('.com/')[1].split('?')[0]
    else:
        path = url.split('?')[0]
        
    if 'tos-maliva' in path:
        return f"https://p16-oec-va.ibyteimg.com/{path}"
    elif 'tos-alisg' in path:
        return f"https://p16-images-comn-sg.tokopedia-static.net/{path}"
    return url

def clean_seo_title(raw_name, cat_type):
    # Strip Tokopedia variant suffixes like - 38, - 25, etc.
    name = re.sub(r'\s*-\s*\d+.*$', '', raw_name).strip()
    name = re.sub(r'[\r\n\t]+', ' ', name)
    name = re.sub(r'\s+', ' ', name)
    
    # Add keywords based on category
    if "terra" in name.lower():
        title = f"{name} Heavy Duty Waterproof PVC Safety Work Rain Boots"
    elif "orca" in name.lower():
        title = f"{name} Industrial Waterproof Protective High Rain Boots"
    elif "chef" in name.lower():
        title = f"{name} Slip Resistant Kitchen Chef Work Shoes Waterproof Slip On"
    elif "medic" in name.lower():
        title = f"{name} Medical Hospital Lab Cleanroom Protective Shoes Anti Slip"
    elif "allbike" in name.lower() or "moto" in name.lower():
        title = f"{name} Waterproof Motorcycle Riding Shoes Breathable PVC Casual"
    elif "safety" in name.lower() or "s5" in name.lower():
        title = f"{name} S5 Steel Toe Industrial Heavy Duty Safety Boots Waterproof"
    elif "star" in name.lower():
        title = f"{name} Casual Waterproof PVC Kets Sneakers Daily Shoes"
    elif "kids" in name.lower():
        title = f"{name} Waterproof Anti Slip Kids Rain Boots Cute Durable PVC"
    elif "clogs" in name.lower() or "995" in name.lower() or "sandal" in name.lower():
        title = f"{name} Comfortable Slip On PVC Clogs Slippers Anti Slip"
    else:
        title = f"{name} High Durability Waterproof PVC Protective Boots"
        
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > 128:
        title = title[:125] + "..."
    return title

def generate_b2b_html_description(name, desc_raw, weight_str, price_usd, cat_name):
    # Parse dimensions, outsoles, heights from desc_raw if present
    height_info = "35 - 40 cm"
    outsole_info = "25.5 - 29.5 cm"
    material_info = "100% Virgin High-Grade PVC / Nitrile Polymer"
    
    if desc_raw:
        # Search for height
        m_h = re.search(r'tinggi\s*([0-9,\.]+)\s*cm', desc_raw, re.IGNORECASE)
        if m_h:
            height_info = f"Approx. {m_h.group(1)} cm"
            
        m_mat = re.search(r'\*?bahan\s*:\s*([^\*\n\r]+)\*?', desc_raw, re.IGNORECASE)
        if m_mat:
            material_info = m_mat.group(1).strip()
            
    # Extract size guide if available
    size_guide_rows = """
        <tr><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">EU 38</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">25.5 cm</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">37.0 cm</td></tr>
        <tr><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">EU 39</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">26.0 cm</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">37.0 cm</td></tr>
        <tr><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">EU 40</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">27.0 cm</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">38.0 cm</td></tr>
        <tr><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">EU 41</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">27.5 cm</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">39.0 cm</td></tr>
        <tr><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">EU 42</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">28.0 cm</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">39.0 cm</td></tr>
        <tr><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">EU 43</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">29.5 cm</td><td style="padding:8px;border:1px solid #e2e8f0;text-align:center;">40.0 cm</td></tr>
    """

    html = f"""<div style="font-family: Arial, sans-serif; color: #1e293b; line-height: 1.6; max-width: 1000px; margin: 0 auto;">
    <!-- HEADER BRANDING -->
    <div style="background: linear-gradient(135deg, #1e3a8a, #0284c7); color: #ffffff; padding: 24px 28px; border-radius: 8px; margin-bottom: 24px;">
        <h2 style="margin: 0 0 8px 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;">AP BOOTS® — OFFICIAL GOLD SUPPLIER EXPORT LISTING</h2>
        <p style="margin: 0; font-size: 13.5px; opacity: 0.95;">Legal Manufacturer: <strong>PT Waru Gunung</strong> (Surabaya, Indonesia) | Export Partner: <strong>PT Indo Sukses Semesta</strong> (HOTS Trading)</p>
    </div>

    <!-- PRODUCT TITLE & OVERVIEW -->
    <div style="margin-bottom: 24px;">
        <h3 style="font-size: 18px; color: #0f172a; border-left: 4px solid #0284c7; padding-left: 12px; margin-bottom: 12px;">Product Overview: {name}</h3>
        <p style="font-size: 14px; color: #334155; margin-bottom: 12px;">
            The <strong>{name}</strong> is precision-engineered for industrial durability, safety, and all-day comfort. Manufactured utilizing high-pressure single-injection molding technology, this footwear provides reliable leak-proof protection against water, mud, mild chemicals, and abrasive surfaces. Ideal for high-demand B2B applications worldwide.
        </p>
    </div>

    <!-- GPSR SECTION 11: SAFE B2B COMPLIANCE & ANTI-OVERCLAIM DISCLAIMER -->
    <div style="background-color: #f1f5f9; border-left: 4px solid #475569; border-radius: 6px; padding: 14px 18px; margin-bottom: 24px; font-size: 12.5px; color: #334155; line-height: 1.55;">
        <p style="margin: 0 0 6px 0; font-weight: 700; color: #0f172a;">Compliance & Anti-Overclaim Notice (GPSR Aligned):</p>
        <p style="margin: 0 0 6px 0;">This product is supplied for general workplace and industrial use according to the specifications stated in this listing. Product performance depends on application and operating conditions. Buyers should review technical specifications, safety data, and inspect physical samples before placing bulk orders.</p>
        <p style="margin: 0;">The product is not represented as a medical device or certified PPE under EU/UK/US regulations unless the specific certificate and declaration are formally provided for the exact model and destination market.</p>
    </div>

    <!-- GPSR SECTION 6: MANDATORY SAFETY INFORMATION -->
    <div style="background-color: #fffbeb; border: 1.5px solid #f59e0b; border-radius: 8px; padding: 16px 20px; margin-bottom: 24px;">
        <h4 style="margin: 0 0 10px 0; font-size: 14.5px; color: #b45309; font-weight: 700; display: flex; align-items: center; gap: 6px;">
            <span>⚠️</span> Mandatory Safety Information & Usage Restrictions
        </h4>
        <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #78350f; line-height: 1.55;">
            <li style="margin-bottom: 4px;"><strong>Pre-Use Inspection:</strong> Inspect the product before each use. Do not use if torn, cracked, punctured, deformed, or damaged.</li>
            <li style="margin-bottom: 4px;"><strong>General Utility Scope:</strong> Designed for general industrial and utility use unless a verified protection standard is documented.</li>
            <li style="margin-bottom: 4px;"><strong>Non-Medical Device:</strong> This product is NOT a medical device and is not intended to diagnose, treat, cure, or prevent any illness.</li>
            <li style="margin-bottom: 4px;"><strong>Non-Certified PPE Disclaimer:</strong> Not certified as PPE unless applicable documentation is issued for the exact SKU.</li>
            <li style="margin-bottom: 4px;"><strong>Hazard Limitation:</strong> Keep away from open flames, concentrated chemicals, high-voltage electricity, and sharp penetrations unless certified.</li>
            <li style="margin-bottom: 4px;"><strong>Storage & Care:</strong> Store in a cool, dry place away from direct sunlight and aggressive chemicals. Clean with mild soapy water.</li>
            <li style="margin-bottom: 0;"><strong>Sample Approval:</strong> Performance may vary with operational conditions. Buyers must evaluate physical samples before volume deployment.</li>
        </ul>
    </div>

    <!-- KEY ADVANTAGES -->
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <h4 style="margin: 0 0 14px 0; font-size: 16px; color: #1e3a8a;">Key Product Advantages & Features</h4>
        <ul style="margin: 0; padding-left: 20px; font-size: 14px; color: #334155;">
            <li style="margin-bottom: 8px;"><strong>Seamless Waterproof:</strong> One-piece injection molded construction eliminates seams to ensure high liquid impermeability.</li>
            <li style="margin-bottom: 8px;"><strong>Anti-Slip Traction Outsole:</strong> Deep lug tread design delivers aggressive grip on mud, wet tile, oily floors, and uneven terrains.</li>
            <li style="margin-bottom: 8px;"><strong>Ergonomic Flex-Comfort:</strong> Specially formulated flexible PVC compound moves naturally with foot biomechanics to reduce fatigue during extended work shifts.</li>
            <li style="margin-bottom: 8px;"><strong>Extreme Weather & Chemical Resistance:</strong> Resistant to UV degradation, mild acids, alkalis, oils, and agricultural fertilizers.</li>
            <li style="margin-bottom: 0;"><strong>OEM / ODM Customization:</strong> Custom branding, color schemes, labeling, and carton packaging available for bulk export orders.</li>
        </ul>
    </div>

    <!-- TECHNICAL SPECIFICATION MATRIX -->
    <div style="margin-bottom: 24px;">
        <h4 style="font-size: 16px; color: #1e3a8a; border-left: 4px solid #0284c7; padding-left: 12px; margin-bottom: 14px;">Technical Specifications</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px; text-align: left;">
            <tbody>
                <tr style="background-color: #f1f5f9;"><th style="padding: 10px; border: 1px solid #cbd5e1; width: 30%;">Product Series</th><td style="padding: 10px; border: 1px solid #cbd5e1;">{cat_name}</td></tr>
                <tr><th style="padding: 10px; border: 1px solid #cbd5e1;">Legal Manufacturer</th><td style="padding: 10px; border: 1px solid #cbd5e1;">PT Waru Gunung (Surabaya, Indonesia)</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 10px; border: 1px solid #cbd5e1;">Export Supply Partner</th><td style="padding: 10px; border: 1px solid #cbd5e1;">PT Indo Sukses Semesta (HOTS Trading)</td></tr>
                <tr><th style="padding: 10px; border: 1px solid #cbd5e1;">Outsole Material</th><td style="padding: 10px; border: 1px solid #cbd5e1;">High-Grade PVC / Anti-Slip Rubbertech</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 10px; border: 1px solid #cbd5e1;">Upper Material</th><td style="padding: 10px; border: 1px solid #cbd5e1;">{material_info}</td></tr>
                <tr><th style="padding: 10px; border: 1px solid #cbd5e1;">Average Unit Weight</th><td style="padding: 10px; border: 1px solid #cbd5e1;">{weight_str} (Approx.)</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 10px; border: 1px solid #cbd5e1;">Standard Height</th><td style="padding: 10px; border: 1px solid #cbd5e1;">{height_info}</td></tr>
                <tr><th style="padding: 10px; border: 1px solid #cbd5e1;">Standard Outsole Length</th><td style="padding: 10px; border: 1px solid #cbd5e1;">{outsole_info}</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 10px; border: 1px solid #cbd5e1;">Size Range</th><td style="padding: 10px; border: 1px solid #cbd5e1;">EU 38 - 44 / US 6 - 11</td></tr>
                <tr><th style="padding: 10px; border: 1px solid #cbd5e1;">Origin</th><td style="padding: 10px; border: 1px solid #cbd5e1;">Made in Indonesia (Factory Direct Export via Tanjung Perak / Tanjung Priok)</td></tr>
                <tr style="background-color: #f1f5f9;"><th style="padding: 10px; border: 1px solid #cbd5e1;">Certification</th><td style="padding: 10px; border: 1px solid #cbd5e1;">SNI (Standar Nasional Indonesia) & Factory QC Export Standards</td></tr>
            </tbody>
        </table>
    </div>

    <!-- SIZE CONVERSION GUIDE -->
    <div style="margin-bottom: 24px;">
        <h4 style="font-size: 16px; color: #1e3a8a; border-left: 4px solid #0284c7; padding-left: 12px; margin-bottom: 14px;">Precision Size & Dimension Chart</h4>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="background-color: #1e3a8a; color: #ffffff;">
                    <th style="padding: 8px; border: 1px solid #1e3a8a; text-align: center;">EUR Size</th>
                    <th style="padding: 8px; border: 1px solid #1e3a8a; text-align: center;">Outsole Length (cm)</th>
                    <th style="padding: 8px; border: 1px solid #1e3a8a; text-align: center;">Shaft Height (cm)</th>
                </tr>
            </thead>
            <tbody>
                {size_guide_rows}
            </tbody>
        </table>
    </div>

    <!-- TARGET INDUSTRIAL APPLICATIONS -->
    <div style="margin-bottom: 24px;">
        <h4 style="font-size: 16px; color: #1e3a8a; border-left: 4px solid #0284c7; padding-left: 12px; margin-bottom: 12px;">Recommended Applications & Industries</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; font-size: 13px;">
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
                <strong>🌾 Agriculture & Forestry:</strong> Palm oil, rubber plantations, rice paddies, farming, and drainage work.
            </div>
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
                <strong>🏗️ Civil & Construction:</strong> Roadwork, cement pouring, earthmoving, trenching, and mining sites.
            </div>
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
                <strong>🐟 Marine & Food Processing:</strong> Fisheries, aquaculture, cold storage, slaughterhouses, and commercial kitchens.
            </div>
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px;">
                <strong>🛵 Daily & Heavy Rainfall:</strong> Urban flood safety, motorcycle commuting, and all-weather utility.
            </div>
        </div>
    </div>

    <!-- PACKAGING & EXPORT LOGISTICS -->
    <div style="background-color: #f1f5f9; border-radius: 8px; padding: 16px 20px; font-size: 13px; color: #334155;">
        <h5 style="margin: 0 0 8px 0; font-size: 14px; color: #0f172a;">Packaging & Shipping Information</h5>
        <p style="margin: 0 0 6px 0;">• <strong>Standard Export Packaging:</strong> 1 pair per individual polybag; 10 to 18 pairs packed in export grade corrugated master carton.</p>
        <p style="margin: 0 0 6px 0;">• <strong>Port of Loading:</strong> Tanjung Priok Seaport, Jakarta, Indonesia (FOB / CIF / CFR terms accepted).</p>
        <p style="margin: 0;">• <strong>Production Lead Time:</strong> Ready-to-ship stock dispatched within 7-14 days; Bulk custom OEM production 20-30 days.</p>
    </div>
</div>"""
    return html

def parse_weight_kg(w_str, default=1.7):
    if not w_str: return default
    w = str(w_str).lower().replace(',', '.')
    m = re.search(r'([0-9\.]+)', w)
    if not m: return default
    val = float(m.group(1))
    if 'g' in w and 'kg' not in w:
        return round(val / 1000.0, 2)
    return round(val, 2)

def main():
    print(f"Loading template from: {TEMPLATE_PATH}")
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb['Alibaba default template']

    # Clear existing rows from row 5
    if ws.max_row >= 5:
        ws.delete_rows(5, ws.max_row - 4)

    start_row = 5
    print(f"Populating {len(tokopedia_dict)} canonical Tokopedia products into Alibaba Bulk Template...")

    for idx, (url, prod) in enumerate(tokopedia_dict.items()):
        row_idx = start_row + idx

        raw_name = prod.get('name') or f"AP Boots Product {idx+1}"
        desc_raw = prod.get('desc', '')
        weight_raw = prod.get('weight') or '1.7 kg'
        weight_kg = parse_weight_kg(weight_raw, 1.7)
        etalase = prod.get('etalase', 'AP Boots')

        # Clean title
        title = clean_seo_title(raw_name, etalase)

        # Collect CDN Image URLs (Col 2 to 7)
        imgs = ['', '', '', '', '', '']
        main_img = prod.get('main_img')
        if main_img:
            imgs[0] = get_public_cdn_url(main_img)
            
        gallery_str = prod.get('gallery', '')
        if gallery_str:
            lines = [get_public_cdn_url(l.strip()) for l in gallery_str.split('\n') if l.strip().startswith('http')]
            for g_i, g_url in enumerate(lines[:5], 1):
                if g_i < 6 and not imgs[g_i]:
                    imgs[g_i] = g_url

        # Fallback to Shopee images if empty (Hanya main image, non-main image Shopee jangan di-load)
        clean_key = re.sub(r'[^a-z0-9]', '', raw_name.lower())
        for sk, sv in shopee_lookup.items():
            if sk in clean_key or clean_key[:12] in sk:
                if not imgs[0] and sv:
                    imgs[0] = sv[0]
                break

        # If primary image still empty, set a placeholder from official CDN
        if not imgs[0]:
            imgs[0] = "https://p16-images-comn-sg.tokopedia-static.net/tos-alisg-i-aphluv4xwc-sg/886938f2163140e3a9171a2481a51833~tplv-aphluv4xwc-white-pad-v1:1600:1600.jpeg"

        # Calculate Export Pricing in USD
        p_clean = prod.get('price_clean')
        if p_clean and p_clean > 10000:
            # wholesale B2B price is ~65% of local retail IDR converted at 15500
            base_usd = round((p_clean / 15500.0) * 0.70, 2)
            base_usd = max(3.50, min(25.0, base_usd))
        else:
            base_usd = 5.50

        t1_price = round(base_usd, 2)
        t2_price = round(base_usd * 0.95, 2)
        t3_price = round(base_usd * 0.90, 2)
        t4_price = round(base_usd * 0.85, 2)
        moq_p = 100

        # Description HTML
        html_desc = generate_b2b_html_description(raw_name, desc_raw, weight_raw, base_usd, etalase)

        # SKU code
        sku = f"APB-{idx+1:03d}"
        model = sku

        # Category mapping
        name_l = raw_name.lower()
        if "safety" in name_l or "s5" in name_l or "s4" in name_l or "metaguard" in name_l:
            cat = "Safety > Personal Protective Equipment > Foot Protection > Safety Shoes"
            feature = "Steel Toe, Waterproof, Anti-Slip, Chemical Resistant"
            gender = "Men / Unisex"
        elif "clogs" in name_l or "sandal" in name_l or "995" in name_l:
            cat = "Shoes & Accessories > Men's Shoes > Slippers > Slides Slippers"
            feature = "Comfort, Breathable, Lightweight, Slip-On"
            gender = "Unisex"
        elif "kids" in name_l:
            cat = "Toys, Kids & Baby > Kids' Fashion > Kids' Shoes > Rain Boots"
            feature = "Waterproof, Anti-Slip, Colorful, Flexible"
            gender = "Kids / Children"
        elif "allbike" in name_l or "moto" in name_l or "star" in name_l:
            cat = "Shoes & Accessories > Men's Shoes > Other Shoes"
            feature = "Waterproof, Breathable Air Vent, Ergonomic, Casual"
            gender = "Men / Unisex"
        else:
            cat = "Shoes & Accessories > Men's Shoes > Boots"
            feature = "100% Waterproof, Heavy Duty PVC, Non-Slip Outsole"
            gender = "Men / Unisex"

        outsole = "PVC / Rubber"
        upper = "PVC"
        season = "All Seasons"
        color = "Black; Green; White; Yellow"
        size = "EU 38-44"

        # Dimensions
        if weight_kg > 1.6:
            l_val, w_val, h_val = 60.0, 42.0, 38.0
        elif weight_kg > 1.0:
            l_val, w_val, h_val = 55.0, 40.0, 32.0
        else:
            l_val, w_val, h_val = 50.0, 35.0, 25.0

        # Build 57 column row data (1-indexed Col A to BE)
        row_data = [
            title,              # Col 1 (A): * Product title
            imgs[0],            # Col 2 (B): * Product image 1
            imgs[1],            # Col 3 (C): Product image 2
            imgs[2],            # Col 4 (D): Product image 3
            imgs[3],            # Col 5 (E): Product image 4
            imgs[4],            # Col 6 (F): Product image 5
            imgs[5],            # Col 7 (G): Product image 6
            html_desc,          # Col 8 (H): Product description
            "Indonesia",        # Col 9 (I): Place of origin
            "AP Boots",         # Col 10 (J): Brand name
            cat,                # Col 11 (K): Category
            "Outsole Material", # Col 12 (L): Product attribute name 1
            outsole,            # Col 13 (M): Product attribute value 1
            "Upper Material",   # Col 14 (N): Product attribute name 2
            upper,              # Col 15 (O): Product attribute value 2
            "Season",           # Col 16 (P): Product attribute name 3
            season,             # Col 17 (Q): Product attribute value 3
            "Feature",          # Col 18 (R): Product attribute name 4
            feature,            # Col 19 (S): Product attribute value 4
            "Gender",           # Col 20 (T): Product attribute name 5
            gender,             # Col 21 (U): Product attribute value 5
            "piece",            # Col 22 (V): Sell product by
            None,               # Col 23 (W): Batch quantity
            "Pair/Pairs",       # Col 24 (X): Unit
            "USD",              # Col 25 (Y): Currency
            "Tiered pricing",   # Col 26 (Z): Pricing type
            5000,               # Col 27 (AA): Inventory
            model,              # Col 28 (AB): SPU ID (Model number)
            sku,                # Col 29 (AC): SKU code
            t1_price,           # Col 30 (AD): SKU pricing
            "Color",            # Col 31 (AE): SKU attribute name 1
            color,              # Col 32 (AF): SKU attribute value 1
            "Size",             # Col 33 (AG): SKU attribute name 2
            size,               # Col 34 (AH): SKU attribute value 2
            None,               # Col 35 (AI): SKU attribute name 3
            None,               # Col 36 (AJ): SKU attribute value 3
            None,               # Col 37 (AK): SKU attribute name 4
            None,               # Col 38 (AL): SKU attribute value 4
            t1_price,           # Col 39 (AM): Tiered pricing 1
            moq_p,              # Col 40 (AN): MOQ 1
            t2_price,           # Col 41 (AO): Tiered pricing 2
            moq_p * 5,          # Col 42 (AP): MOQ 2
            t3_price,           # Col 43 (AQ): Tiered pricing 3
            moq_p * 10,         # Col 44 (AR): MOQ 3
            t4_price,           # Col 45 (AS): Range pricing (Lower limit)
            t1_price,           # Col 46 (AT): Range pricing (Higher limit)
            weight_kg,          # Col 47 (AU): * Gross weight (KG)
            "Default Shipping Template", # Col 48 (AV): * Shipping template name
            moq_p,              # Col 49 (AW): * Shipping quantity 1
            7,                  # Col 50 (AX): * Estimated shipping lead time 1
            moq_p * 5,          # Col 51 (AY): Shipping quantity 2
            14,                 # Col 52 (AZ): Estimated shipping lead time 2
            moq_p * 10,         # Col 53 (BA): Shipping quantity 3
            30,                 # Col 54 (BB): Estimated shipping lead time 3
            l_val,              # Col 55 (BC): Product size-Length
            w_val,              # Col 56 (BD): Product size-Width
            h_val               # Col 57 (BE): Product size-Height
        ]

        for col_i, val in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_i, value=val)

    print(f"Saving to Output: {OUTPUT_EXCEL}")
    wb.save(OUTPUT_EXCEL)
    print(f"Saving copy to Root: {ROOT_OUTPUT_EXCEL}")
    wb.save(ROOT_OUTPUT_EXCEL)
    print("Template generation complete successfully!")

if __name__ == '__main__':
    main()
