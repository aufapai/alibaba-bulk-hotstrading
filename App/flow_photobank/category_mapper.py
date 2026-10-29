# -*- coding: utf-8 -*-
"""
Category & SKU Mapper for Photobank (https://admin.hotstrading.com/photo-bank)
Maps SKU and product titles to the 11 official Photobank categories and generates standardized filenames.
"""

import re
import os

PHOTOBANK_CATEGORIES = {
    "01_Safety_Boots": {
        "folder": "01_Safety_Boots",
        "group_name": "AP Safety Boots",
        "keywords": ["safety", "s5", "s4", "metaguard", "max", "steel toe", "industrial safety"]
    },
    "02_Terra_Series": {
        "folder": "02_Terra_Series",
        "group_name": "AP Terra Series",
        "keywords": ["terra", "kebun", "tani", "agri", "eco", "terra gp", "terra 1", "terra 2", "terra 3", "terra 5"]
    },
    "03_Orca_Series": {
        "folder": "03_Orca_Series",
        "group_name": "AP Orca Series",
        "keywords": ["orca", "tambang", "heavy duty", "proyek"]
    },
    "04_Chef_Series": {
        "folder": "04_Chef_Series",
        "group_name": "AP Chef Series",
        "keywords": ["chef", "dapur", "culinary", "restaurant", "food hygiene"]
    },
    "05_Medic_Series": {
        "folder": "05_Medic_Series",
        "group_name": "AP Medic Series",
        "keywords": ["medic", "medis", "hospital", "clinic", "anti-microbial", "white doctor"]
    },
    "06_Biker_Casual": {
        "folder": "06_Biker_Casual",
        "group_name": "AP Biker & Casual",
        "keywords": ["allbike", "moto", "hobby", "biker", "riding", "work & hobby"]
    },
    "07_Classic_Boots": {
        "folder": "07_Classic_Boots",
        "group_name": "AP Classic Boots",
        "keywords": ["2003", "2005", "2017", "9303", "9506", "classic", "tricolour", "roots n leaves", "green lime"]
    },
    "08_Kids_Boots": {
        "folder": "08_Kids_Boots",
        "group_name": "AP Kids Boots",
        "keywords": ["kids", "anak", "safari", "2012", "toddler", "rain boots kids"]
    },
    "09_Sandals_Clogs": {
        "folder": "09_Sandals_Clogs",
        "group_name": "AP Sandals & Clogs",
        "keywords": ["clogs", "sandal", "selop", "slippers", "slide"]
    },
    "10_Kasual_Sneakers": {
        "folder": "10_Kasual_Sneakers",
        "group_name": "AP Kasual Sneakers",
        "keywords": ["bola", "969", "sneaker", "sport", "star series", "pantofel", "vantopel"]
    },
    "11_General_Lifestyle_Boots": {
        "folder": "11_General_Lifestyle_Boots",
        "group_name": "General & Lifestyle",
        "keywords": ["general", "lifestyle", "boots", "pvc"]
    }
}

# Known SKU prefix overrides based on official mapping
SKU_PREFIX_MAP = {
    "APB-001": ("06_Biker_Casual", "AP ALLBIKE"),
    "APB-002": ("07_Classic_Boots", "AP Boots 2017 Green"),
    "APB-003": ("07_Classic_Boots", "AP Boots 2017 Green"),
    "APB-004": ("07_Classic_Boots", "AP Boots 2005 ROOTS N LEAVES"),
    "APB-005": ("07_Classic_Boots", "AP Boots 2005 Hijau"),
    "APB-006": ("07_Classic_Boots", "AP Boots 2003 Hijau Tricolour"),
    "APB-007": ("02_Terra_Series", "AP Terra Eco 3"),
    "APB-008": ("02_Terra_Series", "AP Terra Eco 3"),
    "APB-009": ("02_Terra_Series", "AP Terra Eco 3"),
    "APB-010": ("02_Terra_Series", "AP Terra Eco 3"),
    "APB-011": ("09_Sandals_Clogs", "AP CLOGS"),
    "APB-013": ("06_Biker_Casual", "AP ALLBIKE 2"),
    "APB-014": ("10_Kasual_Sneakers", "AP 969 / Bola Series"),
    "APB-015": ("02_Terra_Series", "AP Terra GP"),
    "APB-016": ("01_Safety_Boots", "AP MAX / S5"),
    "APB-017": ("08_Kids_Boots", "AP Kids Safari Series"),
    "APB-018": ("08_Kids_Boots", "AP Kids 2012"),
    "APB-019": ("01_Safety_Boots", "AP METAGUARD"),
    "APB-021": ("04_Chef_Series", "AP Chef Series"),
    "APB-022": ("05_Medic_Series", "AP Medic Series"),
    "APB-023": ("02_Terra_Series", "AP Terra 1 Putih"),
    "APB-024": ("03_Orca_Series", "AP Orca Industrial"),
    "APB-026": ("02_Terra_Series", "AP Terra 1"),
    "APB-027": ("02_Terra_Series", "AP Terra Eco"),
    "APB-028": ("06_Biker_Casual", "AP Moto Series"),
    "APB-030": ("06_Biker_Casual", "AP Moto 1"),
    "APB-031": ("06_Biker_Casual", "AP Hobby N Work"),
    "APB-032": ("09_Sandals_Clogs", "AP CLOGS / Sandal Series"),
    "APB-033": ("10_Kasual_Sneakers", "AP Star Series"),
    "APB-034": ("07_Classic_Boots", "AP Boots 9303"),
    "APB-035": ("07_Classic_Boots", "AP Boots 9506"),
}

def clean_slug(text: str) -> str:
    """Mengubah teks menjadi slug bersih ramah nama file."""
    text = text.lower()
    text = re.sub(r'[\/\\:\*\?"<>\|\(\)]', ' ', text)
    text = re.sub(r'[^a-z0-9\s_-]', '', text)
    text = re.sub(r'\s+', '_', text.strip())
    text = re.sub(r'_+', '_', text)
    return text[:40].strip('_')

def resolve_photobank_category(sku: str, title: str, category_str: str = ""):
    """
    Menentukan folder kategori resmi dan nama grup kategori Photobank.
    Returns: (folder_name, category_group, clean_product_name)
    """
    sku_upper = str(sku).strip().upper()
    
    # 1. Direct SKU prefix lookup
    for prefix, (folder, prod_name) in SKU_PREFIX_MAP.items():
        if sku_upper.startswith(prefix):
            group_name = PHOTOBANK_CATEGORIES[folder]["group_name"]
            return folder, group_name, prod_name
            
    # 2. Text keyword matching
    combined = f"{sku} {title} {category_str}".lower()
    
    for folder_key, data in PHOTOBANK_CATEGORIES.items():
        if folder_key == "11_General_Lifestyle_Boots":
            continue
        for kw in data["keywords"]:
            if re.search(r'\b' + re.escape(kw) + r'\b', combined):
                # Clean title for display
                short_title = title.split(' - ')[0].strip() if ' - ' in title else title[:30].strip()
                return folder_key, data["group_name"], short_title

    # 3. Fallback to General
    short_title = title.split(' - ')[0].strip() if ' - ' in title else title[:30].strip()
    return "11_General_Lifestyle_Boots", "General & Lifestyle", short_title

def generate_photobank_filename(sku: str, product_name: str, slot_name: str, ext: str = "webp") -> str:
    """
    Membuat nama file standar untuk Photobank: [SKU]_[Slug]_[Slot].[ext]
    Contoh: APB-016_ap_max_s5_slot1_hero.webp
    """
    sku_prefix = str(sku).strip()
    slug = clean_slug(product_name)
    slot_clean = clean_slug(slot_name)
    if not ext.startswith('.'):
        ext = f".{ext}"
    return f"{sku_prefix}_{slug}_{slot_clean}{ext}"
