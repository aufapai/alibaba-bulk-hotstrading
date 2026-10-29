# -*- coding: utf-8 -*-
import os
import sys
import csv
import sqlite3
import re
import openpyxl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PARENT_DIR, 'Database', 'alibaba_master.db')
TOKOPEDIA_EXCEL = os.path.join(PARENT_DIR, 'Output', 'Alibaba_Bulk_Upload_Tokopedia_Master_2026.xlsx')
INPUT_TEMPLATE_CSV = os.path.join(BASE_DIR, 'Alibaba_Bulk_Template.csv')
OUTPUT_EXPANDED_CSV = os.path.join(BASE_DIR, 'Alibaba_Bulk_Template_With_Prompts.csv')
OUTPUT_MASTER_CSV = os.path.join(BASE_DIR, 'Alibaba_Master_106_SKU_ImageGen_Ready.csv')
OUTPUT_BLANK_CSV = os.path.join(BASE_DIR, 'Alibaba_Template_Input_Kosong.csv')

HEADER_FIELDS = [
    'SKU code',
    '* Product title',
    'Category',
    '* Product image 1',
    'Description',
    'Color',
    'Material',
    'Sole',
    'Branding',
    'Auto_Generated_Description',
    'Prompt_Slot1_Hero_WhiteBG',
    'Prompt_Slot2_Side_Profile',
    'Prompt_Slot3_Outsole_Tread',
    'Prompt_Slot4_Contextual_Usage'
]

COLOR_KEYWORDS = [
    'green lime', 'roots n leaves', 'army green', 'dark brown', 'light grey',
    'kuning', 'yellow', 'hijau', 'green', 'hitam', 'black', 'putih', 'white',
    'orange', 'oranye', 'merah', 'red', 'biru', 'blue', 'abu-abu', 'abu', 'grey',
    'gray', 'coklat', 'brown', 'pink', 'tosca', 'maroon', 'navy'
]

def load_tokopedia_image_map():
    tokopedia_map = {}
    if not os.path.exists(TOKOPEDIA_EXCEL):
        print(f"[!] File Tokopedia Excel tidak ditemukan di: {TOKOPEDIA_EXCEL}")
        return tokopedia_map

    try:
        wb = openpyxl.load_workbook(TOKOPEDIA_EXCEL, data_only=True)
        ws = wb['Alibaba default template']
        for r in list(ws.iter_rows(values_only=True))[4:]:
            if not r or not r[0]: continue
            title = str(r[0]).strip()
            img1 = str(r[1]).strip() if len(r) > 1 and r[1] else ""
            model = str(r[27]).strip() if len(r) > 27 and r[27] else ""
            sku = str(r[28]).strip() if len(r) > 28 and r[28] else ""
            
            if img1 and img1.startswith("http"):
                if sku: tokopedia_map[sku.upper()] = img1
                if model: tokopedia_map[model.upper()] = img1
                if title:
                    clean_t = title.split(' - ')[0].strip().upper()
                    tokopedia_map[clean_t] = img1
                    tokopedia_map[title.upper()] = img1
        print(f"[*] Berhasil memuat {len(tokopedia_map)} pemetaan gambar Tokopedia!")
    except Exception as e:
        print(f"[!] Gagal membaca gambar Tokopedia Excel: {e}")
    return tokopedia_map

def detect_color_from_title(title_str, default_color_col):
    tl = title_str.lower()
    for c in COLOR_KEYWORDS:
        if re.search(r'\b' + re.escape(c) + r'\b', tl):
            return c.title()
    if default_color_col and default_color_col.strip() not in ['', 'nan', 'None']:
        first_c = default_color_col.split(';')[0].strip()
        return first_c.title()
    return 'Black'

def get_contextual_scene(category_str, title_str):
    text = f"{category_str} {title_str}".lower()
    if any(k in text for k in ['safety', 's5', 'metaguard', 'steel', 'baja', 'industri']):
        return (
            'an active industrial manufacturing factory floor with concrete ground and yellow safety boundary lines',
            'industrial safety, manufacturing plants, and heavy workplace protection'
        )
    elif any(k in text for k in ['terra', 'kebun', 'tani', 'agri', 'eco', 'sawah']):
        return (
            'a muddy agricultural plantation terrain with damp tropical soil in outdoor daylight',
            'agricultural work, farming, forestry, and outdoor plantation'
        )
    elif any(k in text for k in ['orca', 'tambang', 'heavy', 'proyek']):
        return (
            'a heavy-duty construction worksite with gravel, coarse concrete debris, and outdoor daylight',
            'heavy construction, infrastructure projects, and rugged outdoor terrain'
        )
    elif any(k in text for k in ['chef', 'dapur', 'food', 'kuliner', 'restoran']):
        return (
            'a clean commercial restaurant kitchen with wet non-slip floor tiles and stainless steel fixtures',
            'commercial kitchen, culinary hygiene, and food-processing environments'
        )
    elif any(k in text for k in ['medic', 'hospital', 'klinik', 'medis']):
        return (
            'a sanitized medical laboratory corridor with polished vinyl clinical flooring',
            'healthcare, clinical cleanrooms, and medical laboratory hygiene standards'
        )
    elif any(k in text for k in ['biker', 'allbike', 'moto', 'motor', 'riding']):
        return (
            'a wet asphalt city street after rain with glossy puddle reflections and tarmac texture',
            'motorcycle commuting, courier riding, and all-weather city commuting'
        )
    elif any(k in text for k in ['kids', 'anak', 'safari', 'balita']):
        return (
            'a rain-splashed paved pedestrian sidewalk with colorful autumn leaves',
            'everyday kids wet-weather walking, rainy school days, and outdoor play'
        )
    elif any(k in text for k in ['clog', 'sandal', 'selop']):
        return (
            'a clean indoor work floor with natural ambient lighting',
            'all-day indoor standing, light outdoor chores, and ergonomic casual comfort'
        )
    else:
        return (
            'a wet paved road after monsoon rain with natural water puddle reflections',
            'general wet-weather, all-season splash protection, and everyday outdoor utility'
        )

def generate_prompts(sku, title, category, color, material, sole, brand, existing_desc=''):
    clean_title = title.split(' - ')[0].strip() if ' - ' in title else title.strip()
    clean_brand = brand.strip() if (brand and brand.strip()) else 'AP Boots'
    
    if clean_title.lower().startswith(clean_brand.lower()):
        full_display_name = clean_title
    else:
        full_display_name = f"{clean_brand} {clean_title}"
        
    detected_color = detect_color_from_title(title, color)
    clean_material = material.strip() if material else 'Heavy-duty waterproof PVC'
    clean_sole = sole.strip() if sole else 'Anti-slip grooved rubber lug sole'
    
    scene, purpose = get_contextual_scene(category, clean_title)
    
    has_existing = bool(existing_desc and str(existing_desc).strip() not in ['', 'nan', 'None'])
    if not has_existing:
        auto_desc = (
            f"{full_display_name} is a premium waterproof footwear engineered for {purpose}. "
            f"Constructed from high-grade {clean_material} with an advanced {clean_sole} outsole, "
            f"it delivers superior slip resistance, ergonomic comfort, and long-lasting durability."
        )
        final_desc = auto_desc
    else:
        auto_desc = ''
        final_desc = str(existing_desc).strip()
        
    p1_hero = (
        f"Using the attached reference photos, create a professional e-commerce commercial studio product photograph of {full_display_name}. "
        f"Color: {detected_color}. Material: {clean_material} waterproof upper with {clean_sole} outsole. "
        f"Front 3/4 angle, standing upright, centered, occupying roughly 85% of frame. "
        f"Seamless pure white background (RGB 255,255,255), soft even studio lighting, subtle natural contact shadow only underneath. "
        f"Sharp focus, ultra-high detail, square 1:1 ratio. No text, no watermark, no extraneous props."
    )
    
    p2_side = (
        f"Using the attached reference photos, create a clean e-commerce product photograph of {full_display_name} ({detected_color}) "
        f"from a straight 90-degree side profile view. Highlighting the shaft height, waterproof seamless contour, and sole thickness. "
        f"Seamless pure white background (RGB 255,255,255), soft studio lighting, centered, 85% frame, square 1:1 ratio, sharp focus, no text, no watermark."
    )
    
    p3_sole = (
        f"Using the attached reference photos, create a high-definition commercial product photo of {full_display_name} "
        f"showcasing the bottom outsole tread pattern and {clean_sole} traction lugs. "
        f"Crisp texture, deep tread channels, pure white seamless background (RGB 255,255,255), studio lighting, square 1:1 ratio, sharp focus, no text, no watermark."
    )
    
    p4_usage = (
        f"Using the attached reference photos, create a realistic documentary-style photograph of {full_display_name} ({detected_color}) "
        f"being actively worn in {scene}. Lower-body framing from the knees down with focal point on the footwear; no visible human faces. "
        f"Natural realistic lighting, shallow depth of field on background, square 1:1 ratio, photorealistic 8k, no text, no watermark."
    )
    
    return final_desc, auto_desc, p1_hero, p2_side, p3_sole, p4_usage, detected_color

def process_template_csv(tokopedia_map):
    if not os.path.exists(INPUT_TEMPLATE_CSV):
        print(f"[!] File template {INPUT_TEMPLATE_CSV} tidak ditemukan.")
        return
        
    print(f"[*] Membaca file input template: {INPUT_TEMPLATE_CSV}")
    with open(INPUT_TEMPLATE_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    results = []
    for r in rows:
        sku = r.get('SKU code', '').strip()
        title = r.get('* Product title', '').strip()
        category = r.get('Category', '').strip()
        img1 = r.get('* Product image 1', '').strip()
        desc = r.get('Description', '').strip()
        color = r.get('Color', '').strip()
        mat = r.get('Material', '').strip()
        sole = r.get('Sole', '').strip()
        brand = r.get('Branding', '').strip()
        
        # Cari gambar Tokopedia jika ada
        matched_tokopedia_img = (
            tokopedia_map.get(sku.upper()) or 
            tokopedia_map.get(title.upper()) or 
            tokopedia_map.get(title.split(' - ')[0].strip().upper())
        )
        if matched_tokopedia_img:
            img1 = matched_tokopedia_img
        elif not img1 or 'example.com' in img1:
            # Fallback ke sampel gambar AP Boots S5 jika example.com
            img1 = tokopedia_map.get('APB-016', img1)
            
        final_desc, auto_desc, p1, p2, p3, p4, detected_c = generate_prompts(
            sku, title, category, color, mat, sole, brand, desc
        )
        
        results.append({
            'SKU code': sku,
            '* Product title': title,
            'Category': category,
            '* Product image 1': img1,
            'Description': final_desc,
            'Color': color or detected_c,
            'Material': mat or 'Heavy-duty waterproof PVC',
            'Sole': sole or 'Anti-slip grooved rubber lug sole',
            'Branding': brand or 'AP Boots',
            'Auto_Generated_Description': auto_desc,
            'Prompt_Slot1_Hero_WhiteBG': p1,
            'Prompt_Slot2_Side_Profile': p2,
            'Prompt_Slot3_Outsole_Tread': p3,
            'Prompt_Slot4_Contextual_Usage': p4
        })
        
    with open(OUTPUT_EXPANDED_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_FIELDS)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"[+] Berhasil generate: {OUTPUT_EXPANDED_CSV} ({len(results)} baris)")

def process_master_database(tokopedia_map):
    if not os.path.exists(DB_PATH):
        print(f"[!] Database alibaba_master.db tidak ditemukan di {DB_PATH}")
        return
        
    print(f"[*] Membaca 106 SKU dari database master: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT sku, product_title, category_group, image_1, color, upper_material, outsole_material, brand_name FROM products ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    
    results = []
    tokopedia_count = 0
    for r in rows:
        sku, title, cat_group, img1, color, mat, sole, brand = r
        clean_sku = (sku or '').strip().upper()
        
        # Prioritas utama: GUNAKAN LINK FOTO TOKOPEDIA
        tokopedia_url = (
            tokopedia_map.get(clean_sku) or 
            tokopedia_map.get(title.upper()) or 
            tokopedia_map.get(title.split(' - ')[0].strip().upper())
        )
        if tokopedia_url:
            final_img = tokopedia_url
            tokopedia_count += 1
        else:
            final_img = img1 or ''
            
        final_desc, auto_desc, p1, p2, p3, p4, detected_c = generate_prompts(
            sku or '',
            title or '',
            cat_group or '',
            color or 'Black',
            mat or 'PVC',
            sole or 'PVC / Rubber',
            brand or 'AP Boots',
            ''
        )
        
        results.append({
            'SKU code': sku,
            '* Product title': title,
            'Category': cat_group,
            '* Product image 1': final_img,
            'Description': final_desc,
            'Color': detected_c,
            'Material': mat or 'PVC',
            'Sole': sole or 'PVC / Rubber',
            'Branding': brand or 'AP Boots',
            'Auto_Generated_Description': auto_desc,
            'Prompt_Slot1_Hero_WhiteBG': p1,
            'Prompt_Slot2_Side_Profile': p2,
            'Prompt_Slot3_Outsole_Tread': p3,
            'Prompt_Slot4_Contextual_Usage': p4
        })
        
    with open(OUTPUT_MASTER_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_FIELDS)
        writer.writeheader()
        writer.writerows(results)
        
    print(f"[+] Berhasil mengekspor 106 SKU ke: {OUTPUT_MASTER_CSV} (Semua {tokopedia_count} SKU menggunakan link Tokopedia!)")

def create_blank_template(tokopedia_map):
    sample_tokopedia_url = tokopedia_map.get('APB-016', 'https://p16-images-comn-sg.tokopedia-static.net/tos-alisg-i-aphluv4xwc-sg/5356ff5360e94c33a851e64e4963efec~tplv-aphluv4xwc-white-pad-v1:1600:1600.jpeg')
    
    with open(OUTPUT_BLANK_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_FIELDS)
        writer.writeheader()
        writer.writerow({
            'SKU code': 'APB-016',
            '* Product title': 'AP Boots S5 Kuning',
            'Category': 'Safety Boots',
            '* Product image 1': sample_tokopedia_url,
            'Description': '', # Biarkan KOSONG jika ingin otomatis digenerate AI!
            'Color': 'Kuning',
            'Material': 'PVC Matte',
            'Sole': 'Anti-slip Steel Toe',
            'Branding': 'AP Boots',
            'Auto_Generated_Description': '',
            'Prompt_Slot1_Hero_WhiteBG': '',
            'Prompt_Slot2_Side_Profile': '',
            'Prompt_Slot3_Outsole_Tread': '',
            'Prompt_Slot4_Contextual_Usage': ''
        })
    print(f"[+] Template input kosong dibuat di: {OUTPUT_BLANK_CSV}")

    # Perbarui juga file Alibaba_Bulk_Template.csv agar link contoh memakai Tokopedia
    sample_row = [
        'APB-016',
        'AP Boots S5 Kuning',
        'Safety Boots',
        sample_tokopedia_url,
        '', # Dikosongkan agar sesuai kasus pengguna
        'Kuning',
        'PVC Matte',
        'Anti-slip Steel Toe',
        'AP Boots'
    ]
    with open(INPUT_TEMPLATE_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['SKU code', '* Product title', 'Category', '* Product image 1', 'Description', 'Color', 'Material', 'Sole', 'Branding'])
        w.writerow(sample_row)
    print(f"[+] File {INPUT_TEMPLATE_CSV} diperbarui dengan link gambar Tokopedia default!")

if __name__ == '__main__':
    print("=== PHOTOBANK IMAGE GENERATION TEMPLATE GENERATOR ===")
    tokopedia_images = load_tokopedia_image_map()
    process_template_csv(tokopedia_images)
    process_master_database(tokopedia_images)
    create_blank_template(tokopedia_images)
    print("=== SELESAI ===")
