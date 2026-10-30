# -*- coding: utf-8 -*-
"""
Photobank API Bridge & Google Flow Sample Automation
Target Web: https://admin.hotstrading.com/photo-bank
Google Flow Project: https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c
Google Account: aufahots@gmail.com
"""

import os
import sys
import json
import csv
import re
import shutil
from typing import Dict, Any, List, Optional
from PIL import Image, ImageOps, ImageFilter
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTOBANK_DIR = os.path.join(BASE_DIR, "Output", "Photobank_Siap_Upload")
MANIFEST_CSV = os.path.join(PHOTOBANK_DIR, "DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv")
SHOPEE_ASSETS_DIR = os.path.join(BASE_DIR, "Shopee_Product_Assets")
FLOW_DIR = os.path.join(BASE_DIR, "Flow")
CATALOG_IMAGES_DIR = os.path.join(BASE_DIR, "Images_Produk_Katalog")

FLOW_PROJECT_ID = "5a88c3fd-477c-4eed-a126-f812ccfb079c"
FLOW_PROJECT_URL = f"https://flow.google.com/project/{FLOW_PROJECT_ID}"
FLOW_ACCOUNT_EMAIL = "aufahots@gmail.com"

PHOTOBANK_CATEGORIES = [
    ("01_Safety_Boots", "AP Safety Boots", ["SAFETY", "S4", "S5", "METAGUARD", "STRENGTH", "ULTIMATE", "PHENOM", "ERGOS"]),
    ("02_Terra_Series", "AP Terra Series", ["TERRA"]),
    ("03_Orca_Series", "AP Orca Series", ["ORCA"]),
    ("04_Chef_Series", "AP Chef Series", ["CHEF"]),
    ("05_Medic_Series", "AP Medic Series", ["MEDIC"]),
    ("06_Biker_Casual", "AP Biker & Casual", ["ALLBIKE", "MOTO", "BIKER"]),
    ("07_Classic_Boots", "AP Classic Boots", ["AP 1", "2003", "2005", "2006", "2007", "2011", "2017", "2018", "9303", "9506", "CLASSIC", "PRO GREEN", "XTR", "TRICOLOUR"]),
    ("08_Kids_Boots", "AP Kids Boots", ["KIDS", "ANAK", "SAFARI"]),
    ("09_Sandals_Clogs", "AP Sandals & Clogs", ["CLOGS", "SANDAL", "SELOP", "SLOP", "987", "989", "991", "995", "997", "999", "1001", "1003"]),
    ("10_Kasual_Sneakers", "AP Kasual Sneakers", ["STAR", "963", "967", "969"]),
    ("11_General_Lifestyle_Boots", "General & Lifestyle", [])
]


def fit_to_studio_canvas(img: Image.Image, target_size=(1000, 1000), fill_ratio=0.85, bg_color=(255, 255, 255), enhance=True) -> Image.Image:
    """
    Fits and centers an object image onto a pure white square canvas.
    Trims excessive white margins and ensures the boot/shoe occupies fill_ratio (default 85%) of canvas.
    Applies high-quality Lanczos resampling and subtle unsharp masking for sharp details.
    """
    img = img.convert('RGB')
    gray = ImageOps.invert(img.convert('L'))
    # Threshold out noise near pure white (pixel values > 12)
    gray_thresh = gray.point(lambda p: 255 if p > 12 else 0)
    bbox = gray_thresh.getbbox()
    if bbox:
        # Give a 2% margin around detected bbox
        w_box = bbox[2] - bbox[0]
        h_box = bbox[3] - bbox[1]
        pad_x = int(w_box * 0.02)
        pad_y = int(h_box * 0.02)
        crop_box = (
            max(0, bbox[0] - pad_x),
            max(0, bbox[1] - pad_y),
            min(img.width, bbox[2] + pad_x),
            min(img.height, bbox[3] + pad_y)
        )
        cropped = img.crop(crop_box)
    else:
        cropped = img

    max_w = int(target_size[0] * fill_ratio)
    max_h = int(target_size[1] * fill_ratio)

    cw, ch = cropped.size
    ratio = min(max_w / max(1, cw), max_h / max(1, ch))
    new_w = max(1, int(cw * ratio))
    new_h = max(1, int(ch * ratio))

    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    if enhance and ratio > 1.3:
        resized = resized.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))

    canvas = Image.new('RGB', target_size, bg_color)
    paste_x = (target_size[0] - new_w) // 2
    paste_y = (target_size[1] - new_h) // 2
    canvas.paste(resized, (paste_x, paste_y))
    return canvas

def find_catalog_candidate(product_name: str, slot_suffix: str = "03") -> Optional[str]:
    """Finds matching catalog photo for outsole tread (03) or contextual usage (04)."""
    if not os.path.exists(CATALOG_IMAGES_DIR):
        return None
        
    p_lower = product_name.lower().replace("_", " ")
    cat_files = [f for f in os.listdir(CATALOG_IMAGES_DIR) if f.endswith(f"_{slot_suffix}.jpg")]
    
    # 1. Check model numbers (e.g., 2003, 2015, 2005, 9303, 9506, 1001, etc.)
    numbers = re.findall(r'\b\d{3,4}\b', p_lower)
    for num in numbers:
        for f in cat_files:
            if num in f:
                return os.path.join(CATALOG_IMAGES_DIR, f)
                
    # 2. Check special model series names
    special_models = ["ultimate", "xtr", "terra", "orca", "chef", "medic", "moto", "allbike", "safari", "tricolour"]
    for sm in special_models:
        if sm in p_lower:
            for f in cat_files:
                if sm in f.lower():
                    return os.path.join(CATALOG_IMAGES_DIR, f)
                    
    # 3. Default fallback to standard AP 1 catalog angle
    fallback = os.path.join(CATALOG_IMAGES_DIR, f"Black_White_AP 1 Hitam_{slot_suffix}.jpg")
    if os.path.exists(fallback):
        return fallback
        
    return None

def resolve_category(title: str) -> tuple:
    """Resolve official 11 Photobank category folder and group name."""
    t_up = title.upper()
    for folder, group, keywords in PHOTOBANK_CATEGORIES:
        if any(kw in t_up for kw in keywords):
            return folder, group
    return "11_General_Lifestyle_Boots", "General & Lifestyle"

def ensure_photobank_storage():
    """Ensure Photobank output directory and subfolders exist."""
    os.makedirs(PHOTOBANK_DIR, exist_ok=True)
    for folder, _, _ in PHOTOBANK_CATEGORIES:
        os.makedirs(os.path.join(PHOTOBANK_DIR, folder), exist_ok=True)

def append_manifest_record(original_name: str, new_name: str, sku: str, product_name: str, 
                           category_group: str, folder_name: str, file_path: str):
    """Append entry to Photobank manifest CSV."""
    ensure_photobank_storage()
    file_size_kb = round(os.path.getsize(file_path) / 1024.0, 1) if os.path.exists(file_path) else 0.0
    file_exists = os.path.exists(MANIFEST_CSV)
    
    # Check duplicate
    existing = set()
    if file_exists:
        try:
            with open(MANIFEST_CSV, "r", encoding="utf-8") as f:
                r = csv.reader(f)
                next(r, None)
                for row in r:
                    if len(row) > 1:
                        existing.add(row[1])
        except Exception:
            pass

    if new_name in existing:
        return

    with open(MANIFEST_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["original_filename", "new_filename", "sku_prefix", "product_name", "category_group", "folder_name", "file_size_kb"])
        w.writerow([original_name, new_name, sku, product_name, category_group, folder_name, file_size_kb])

def get_photobank_summary() -> Dict[str, Any]:
    """Get overview of ready Photobank files and category distribution."""
    ensure_photobank_storage()
    category_stats = {}
    total_files = 0
    
    for folder, group, _ in PHOTOBANK_CATEGORIES:
        path = os.path.join(PHOTOBANK_DIR, folder)
        files = [f for f in os.listdir(path) if f.lower().endswith(".webp")]
        category_stats[folder] = {
            "group_name": group,
            "count": len(files),
            "sample_files": files[:3]
        }
        total_files += len(files)

    manifest_count = 0
    if os.path.exists(MANIFEST_CSV):
        try:
            with open(MANIFEST_CSV, "r", encoding="utf-8") as f:
                manifest_count = max(0, sum(1 for _ in f) - 1)
        except Exception:
            pass

    return {
        "success": True,
        "total_photobank_files": total_files,
        "manifest_entries": manifest_count,
        "categories": category_stats,
        "target_website": "https://admin.hotstrading.com/photo-bank",
        "api_endpoint": "https://admin.hotstrading.com/api/photobank/upload",
        "google_flow_target": {
            "account": FLOW_ACCOUNT_EMAIL,
            "project_id": FLOW_PROJECT_ID,
            "project_url": FLOW_PROJECT_URL
        }
    }


def generate_product_variations_custom(
    sku: str = "SHP-001",
    folder_name: str = "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC",
    slots: Optional[List[int]] = None,
    target_size: int = 1000,
    fill_ratio: float = 0.85,
    save_to_shopee: bool = True,
    save_to_flow: bool = True,
    save_to_photobank: bool = True
) -> Dict[str, Any]:
    """
    Generate customized product image variations without MCP.
    Allows selecting which slots to generate (e.g. [1, 2, 3, 4] or [1, 2] or [3] or [4]),
    target canvas size (1000, 1200, 1600), fill ratio, and output destinations.
    """
    if slots is None or len(slots) == 0:
        slots = [1, 2, 3, 4]
        
    ensure_photobank_storage()
    
    prod_folder = os.path.join(SHOPEE_ASSETS_DIR, folder_name)
    if not os.path.exists(prod_folder):
        return {"success": False, "error": f"Folder {folder_name} tidak ditemukan di {SHOPEE_ASSETS_DIR}"}

    hero_src = os.path.join(prod_folder, f"hero_{folder_name}.webp")
    side_src = os.path.join(prod_folder, f"side_{folder_name}.webp")
    json_src = os.path.join(prod_folder, f"{folder_name}.json")

    # Read JSON
    prod_info = {}
    if os.path.exists(json_src):
        try:
            with open(json_src, "r", encoding="utf-8") as jf:
                prod_info = json.load(jf)
        except Exception:
            pass

    raw_title = prod_info.get("product_identification", {}).get("product_name_shopee") or folder_name.replace("_", " ")
    brand = prod_info.get("product_identification", {}).get("brand", "AP Boots")
    target_category_folder, target_group = resolve_category(raw_title)

    # Standard clean SKU filename base
    clean_sku = sku.replace("-", "_")
    base_name = f"{clean_sku}_{folder_name[:25]}"

    dest_cat_dir = os.path.join(PHOTOBANK_DIR, target_category_folder)
    if save_to_photobank:
        os.makedirs(dest_cat_dir, exist_ok=True)

    results = []

    # Slot 1: Hero White BG (1:1 Studio)
    if 1 in slots:
        slot1_name = f"{base_name}_slot_1_hero.webp"
        slot1_dest = os.path.join(dest_cat_dir, slot1_name) if save_to_photobank else os.path.join(prod_folder, slot1_name)
        if os.path.exists(hero_src):
            with Image.open(hero_src) as h_img:
                fitted_hero = fit_to_studio_canvas(h_img, target_size=(target_size, target_size), fill_ratio=fill_ratio)
                fitted_hero.save(slot1_dest, "WEBP", quality=92)
        else:
            img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
            img.save(slot1_dest, "WEBP", quality=90)
            
        if save_to_shopee:
            shutil.copy2(slot1_dest, os.path.join(prod_folder, f"hero_{folder_name}.webp"))
        if save_to_flow:
            shutil.copy2(slot1_dest, os.path.join(FLOW_DIR, f"hero_{folder_name}.webp"))
        if save_to_photobank:
            append_manifest_record(os.path.basename(hero_src) if os.path.exists(hero_src) else "hero_white_bg", slot1_name, sku, raw_title, target_group, target_category_folder, slot1_dest)
        results.append({"slot": 1, "type": "hero_white_bg", "filename": slot1_name, "path": slot1_dest})

    # Slot 2: Side Profile 90-degree Lateral
    if 2 in slots:
        slot2_name = f"{base_name}_slot_2_side.webp"
        slot2_dest = os.path.join(dest_cat_dir, slot2_name) if save_to_photobank else os.path.join(prod_folder, slot2_name)
        side_source_file = side_src if os.path.exists(side_src) else (hero_src if os.path.exists(hero_src) else None)
        if side_source_file and os.path.exists(side_source_file):
            with Image.open(side_source_file) as s_img:
                fitted_side = fit_to_studio_canvas(s_img, target_size=(target_size, target_size), fill_ratio=fill_ratio)
                fitted_side.save(slot2_dest, "WEBP", quality=92)
        else:
            img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
            img.save(slot2_dest, "WEBP", quality=90)
            
        if save_to_shopee:
            shutil.copy2(slot2_dest, os.path.join(prod_folder, f"side_{folder_name}.webp"))
        if save_to_flow:
            shutil.copy2(slot2_dest, os.path.join(FLOW_DIR, f"side_{folder_name}.webp"))
        if save_to_photobank:
            append_manifest_record(os.path.basename(side_src) if os.path.exists(side_src) else "side_profile_90deg", slot2_name, sku, raw_title, target_group, target_category_folder, slot2_dest)
        results.append({"slot": 2, "type": "side_profile_90deg", "filename": slot2_name, "path": slot2_dest})

    # Slot 3: Outsole Tread Detail
    if 3 in slots:
        slot3_name = f"{base_name}_slot_3_tread.webp"
        slot3_dest = os.path.join(dest_cat_dir, slot3_name) if save_to_photobank else os.path.join(prod_folder, slot3_name)
        tread_candidate = find_catalog_candidate(raw_title, "03") or find_catalog_candidate(folder_name, "03")
        tread_ratio = min(0.92, fill_ratio + 0.03)
        if tread_candidate and os.path.exists(tread_candidate):
            with Image.open(tread_candidate) as t_img:
                fitted_tread = fit_to_studio_canvas(t_img, target_size=(target_size, target_size), fill_ratio=tread_ratio, enhance=True)
                fitted_tread.save(slot3_dest, "WEBP", quality=92)
        elif os.path.exists(hero_src):
            with Image.open(hero_src) as h_img:
                w, h = h_img.size
                sole_crop = h_img.crop((0, int(h * 0.62), w, h))
                fitted_tread = fit_to_studio_canvas(sole_crop, target_size=(target_size, target_size), fill_ratio=tread_ratio, enhance=True)
                fitted_tread.save(slot3_dest, "WEBP", quality=92)
        else:
            img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
            img.save(slot3_dest, "WEBP", quality=90)
            
        if save_to_shopee:
            shutil.copy2(slot3_dest, os.path.join(prod_folder, f"tread_{folder_name}.webp"))
        if save_to_flow:
            shutil.copy2(slot3_dest, os.path.join(FLOW_DIR, f"tread_{folder_name}.webp"))
        if save_to_photobank:
            append_manifest_record("outsole_tread_detail", slot3_name, sku, raw_title, target_group, target_category_folder, slot3_dest)
        results.append({"slot": 3, "type": "outsole_tread_cleats", "filename": slot3_name, "path": slot3_dest})

    # Slot 4: Contextual In-Use Outdoor
    if 4 in slots:
        slot4_name = f"{base_name}_slot_4_usage.webp"
        slot4_dest = os.path.join(dest_cat_dir, slot4_name) if save_to_photobank else os.path.join(prod_folder, slot4_name)
        usage_candidate = find_catalog_candidate(raw_title, "04") or find_catalog_candidate(folder_name, "04")
        if usage_candidate and os.path.exists(usage_candidate):
            with Image.open(usage_candidate) as u_img:
                fitted_usage = fit_to_studio_canvas(u_img, target_size=(target_size, target_size), fill_ratio=fill_ratio, enhance=True)
                fitted_usage.save(slot4_dest, "WEBP", quality=92)
        elif os.path.exists(hero_src):
            with Image.open(hero_src) as h_img:
                fitted_usage = fit_to_studio_canvas(h_img, target_size=(target_size, target_size), fill_ratio=fill_ratio, enhance=True)
                fitted_usage.save(slot4_dest, "WEBP", quality=92)
        else:
            img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
            img.save(slot4_dest, "WEBP", quality=90)
            
        if save_to_shopee:
            shutil.copy2(slot4_dest, os.path.join(prod_folder, f"usage_{folder_name}.webp"))
        if save_to_flow:
            shutil.copy2(slot4_dest, os.path.join(FLOW_DIR, f"usage_{folder_name}.webp"))
        if save_to_photobank:
            append_manifest_record("contextual_in_use", slot4_name, sku, raw_title, target_group, target_category_folder, slot4_dest)
        results.append({"slot": 4, "type": "contextual_in_use", "filename": slot4_name, "path": slot4_dest})

    # Update product JSON with slots metadata
    slot1_name_val = f"{base_name}_slot_1_hero.webp"
    slot2_name_val = f"{base_name}_slot_2_side.webp"
    slot3_name_val = f"{base_name}_slot_3_tread.webp"
    slot4_name_val = f"{base_name}_slot_4_usage.webp"
    
    flow_payload = {
        "google_flow_target": {
            "account": FLOW_ACCOUNT_EMAIL,
            "project_id": FLOW_PROJECT_ID,
            "project_url": FLOW_PROJECT_URL
        },
        "slots_generated": {
            "slot_1_hero": {
                "file": slot1_name_val,
                "type": "Hero White BG 1:1",
                "prompt": f"Using the attached reference photos, create a professional e-commerce commercial studio product photograph of {raw_title}. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (RGB 255,255,255), soft even studio lighting, subtle contact shadow. 8k clarity, square 1:1 ratio, no text."
            },
            "slot_2_side": {
                "file": slot2_name_val,
                "type": "Side Profile 90-degree Lateral 1:1",
                "prompt": f"Using the attached reference photos, create a clean e-commerce commercial product photograph of {raw_title} from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (RGB 255,255,255), square 1:1 ratio, no text."
            },
            "slot_3_tread": {
                "file": slot3_name_val,
                "type": "Outsole Tread Cleat Detail 1:1",
                "prompt": f"Using the attached reference photos, create a high-definition commercial product photo of {raw_title} showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (RGB 255,255,255), square 1:1 ratio, sharp focus."
            },
            "slot_4_usage": {
                "file": slot4_name_val,
                "type": "Contextual In-Use Field Scene 1:1",
                "prompt": f"Using the attached reference photos, create a realistic photograph of {raw_title} being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
            }
        },
        "photobank_ready": {
            "category_folder": target_category_folder,
            "category_group": target_group,
            "manifest_file": MANIFEST_CSV,
            "all_4_slots_ready": len(results) >= 4 or (1 in slots and 2 in slots and 3 in slots and 4 in slots)
        }
    }

    prod_info["google_flow_and_photobank_slots"] = flow_payload
    with open(json_src, "w", encoding="utf-8") as jf:
        json.dump(prod_info, jf, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "sku": sku,
        "product_name": raw_title,
        "folder_name": folder_name,
        "category_folder": target_category_folder,
        "category_group": target_group,
        "slots_requested": slots,
        "target_size": target_size,
        "fill_ratio": fill_ratio,
        "variations_generated": results,
        "photobank_manifest": MANIFEST_CSV
    }

def batch_generate_products_custom(
    items: List[Dict[str, str]],
    slots: Optional[List[int]] = None,
    target_size: int = 1000,
    fill_ratio: float = 0.85,
    save_to_shopee: bool = True,
    save_to_flow: bool = True,
    save_to_photobank: bool = True
) -> Dict[str, Any]:
    """Batch generate image variations for multiple selected products."""
    results = []
    errors = []
    
    for item in items:
        sku = item.get("sku", "")
        folder = item.get("folder", "")
        if not folder:
            continue
        try:
            res = generate_product_variations_custom(
                sku=sku,
                folder_name=folder,
                slots=slots,
                target_size=target_size,
                fill_ratio=fill_ratio,
                save_to_shopee=save_to_shopee,
                save_to_flow=save_to_flow,
                save_to_photobank=save_to_photobank
            )
            if res.get("success"):
                results.append(res)
            else:
                errors.append({"sku": sku, "folder": folder, "error": res.get("error")})
        except Exception as e:
            errors.append({"sku": sku, "folder": folder, "error": str(e)})

    return {
        "success": True,
        "total_requested": len(items),
        "total_processed": len(results),
        "errors": errors,
        "items": results
    }


def generate_sample_4_variations(sku: str = "SHP-001", folder_name: str = "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC") -> Dict[str, Any]:
    return generate_product_variations_custom(sku=sku, folder_name=folder_name, slots=[1, 2, 3, 4], target_size=1000, fill_ratio=0.85, save_to_shopee=True, save_to_flow=True, save_to_photobank=True)

def _legacy_generate_sample_4_variations(sku: str = "SHP-001", folder_name: str = "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC") -> Dict[str, Any]:
    """
    Generate 4 complete photo variations for 1 sample product:
    Slot 1: Hero White BG (1:1)
    Slot 2: Side Profile 90-degree Lateral (1:1)
    Slot 3: Outsole Tread Cleats Detail (1:1)
    Slot 4: Contextual In-Use Outdoor/Workplace (1:1)
    """
    ensure_photobank_storage()
    
    prod_folder = os.path.join(SHOPEE_ASSETS_DIR, folder_name)
    if not os.path.exists(prod_folder):
        return {"success": False, "error": f"Folder {folder_name} tidak ditemukan di {SHOPEE_ASSETS_DIR}"}

    hero_src = os.path.join(prod_folder, f"hero_{folder_name}.webp")
    side_src = os.path.join(prod_folder, f"side_{folder_name}.webp")
    json_src = os.path.join(prod_folder, f"{folder_name}.json")

    # Read JSON
    prod_info = {}
    if os.path.exists(json_src):
        try:
            with open(json_src, "r", encoding="utf-8") as jf:
                prod_info = json.load(jf)
        except Exception:
            pass

    raw_title = prod_info.get("product_identification", {}).get("product_name_shopee") or folder_name.replace("_", " ")
    brand = prod_info.get("product_identification", {}).get("brand", "AP Boots")
    target_category_folder, target_group = resolve_category(raw_title)

    # Standard clean SKU filename base
    clean_sku = sku.replace("-", "_")
    base_name = f"{clean_sku}_{folder_name[:25]}"

    dest_cat_dir = os.path.join(PHOTOBANK_DIR, target_category_folder)
    os.makedirs(dest_cat_dir, exist_ok=True)

    results = []

    # Slot 1: Hero White BG (Scaled & Fitted 85% Frame)
    slot1_name = f"{base_name}_slot_1_hero.webp"
    slot1_path = os.path.join(dest_cat_dir, slot1_name)
    if os.path.exists(hero_src):
        with Image.open(hero_src) as h_img:
            fitted_hero = fit_to_studio_canvas(h_img, target_size=(1000, 1000), fill_ratio=0.85)
            fitted_hero.save(slot1_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot1_path, "WEBP", quality=90)
    append_manifest_record(os.path.basename(hero_src), slot1_name, sku, raw_title, target_group, target_category_folder, slot1_path)
    results.append({"slot": 1, "type": "hero_white_bg", "filename": slot1_name, "path": slot1_path})

    # Slot 2: Side Profile 90-degree Lateral (Scaled & Fitted 85% Frame)
    slot2_name = f"{base_name}_slot_2_side.webp"
    slot2_path = os.path.join(dest_cat_dir, slot2_name)
    side_source_file = side_src if os.path.exists(side_src) else (hero_src if os.path.exists(hero_src) else None)
    if side_source_file and os.path.exists(side_source_file):
        with Image.open(side_source_file) as s_img:
            fitted_side = fit_to_studio_canvas(s_img, target_size=(1000, 1000), fill_ratio=0.85)
            fitted_side.save(slot2_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot2_path, "WEBP", quality=90)
    append_manifest_record(os.path.basename(side_src), slot2_name, sku, raw_title, target_group, target_category_folder, slot2_path)
    results.append({"slot": 2, "type": "side_profile_90deg", "filename": slot2_name, "path": slot2_path})

    # Slot 3: Outsole Tread Detail (Model-Specific Match or Crisp Sole Crop, 88% Frame)
    slot3_name = f"{base_name}_slot_3_tread.webp"
    slot3_path = os.path.join(dest_cat_dir, slot3_name)
    tread_candidate = find_catalog_candidate(raw_title, "03") or find_catalog_candidate(folder_name, "03")
    if tread_candidate and os.path.exists(tread_candidate):
        with Image.open(tread_candidate) as t_img:
            fitted_tread = fit_to_studio_canvas(t_img, target_size=(1000, 1000), fill_ratio=0.88, enhance=True)
            fitted_tread.save(slot3_path, "WEBP", quality=92)
    elif os.path.exists(hero_src):
        with Image.open(hero_src) as h_img:
            # Crop lower 38% sole area as high-res sole close-up
            w, h = h_img.size
            sole_crop = h_img.crop((0, int(h * 0.62), w, h))
            fitted_tread = fit_to_studio_canvas(sole_crop, target_size=(1000, 1000), fill_ratio=0.88, enhance=True)
            fitted_tread.save(slot3_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot3_path, "WEBP", quality=90)
    append_manifest_record("outsole_tread_detail", slot3_name, sku, raw_title, target_group, target_category_folder, slot3_path)
    results.append({"slot": 3, "type": "outsole_tread_cleats", "filename": slot3_name, "path": slot3_path})

    # Slot 4: Contextual In-Use (Model-Specific Action Match or Field Framing, 85% Frame)
    slot4_name = f"{base_name}_slot_4_usage.webp"
    slot4_path = os.path.join(dest_cat_dir, slot4_name)
    usage_candidate = find_catalog_candidate(raw_title, "04") or find_catalog_candidate(folder_name, "04")
    if usage_candidate and os.path.exists(usage_candidate):
        with Image.open(usage_candidate) as u_img:
            fitted_usage = fit_to_studio_canvas(u_img, target_size=(1000, 1000), fill_ratio=0.85, enhance=True)
            fitted_usage.save(slot4_path, "WEBP", quality=92)
    elif os.path.exists(hero_src):
        with Image.open(hero_src) as h_img:
            fitted_usage = fit_to_studio_canvas(h_img, target_size=(1000, 1000), fill_ratio=0.85, enhance=True)
            fitted_usage.save(slot4_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot4_path, "WEBP", quality=90)
    append_manifest_record("contextual_in_use", slot4_name, sku, raw_title, target_group, target_category_folder, slot4_path)
    results.append({"slot": 4, "type": "contextual_in_use", "filename": slot4_name, "path": slot4_path})

    # Mirror Slot 3 & Slot 4 into product folder and Flow folder
    shutil.copy2(slot3_path, os.path.join(prod_folder, f"tread_{folder_name}.webp"))
    shutil.copy2(slot4_path, os.path.join(prod_folder, f"usage_{folder_name}.webp"))
    shutil.copy2(slot3_path, os.path.join(FLOW_DIR, f"tread_{folder_name}.webp"))
    shutil.copy2(slot4_path, os.path.join(FLOW_DIR, f"usage_{folder_name}.webp"))

    # Update product JSON with 4 slots and Flow Payload
    flow_payload = {
        "google_flow_target": {
            "account": FLOW_ACCOUNT_EMAIL,
            "project_id": FLOW_PROJECT_ID,
            "project_url": FLOW_PROJECT_URL
        },
        "slots_generated": {
            "slot_1_hero": {
                "file": slot1_name,
                "type": "Hero White BG 1:1",
                "prompt": f"Using the attached reference photos, create a professional e-commerce commercial studio product photograph of {raw_title}. Front 3/4 angle, standing upright, centered, occupying 85% frame. Seamless pure white background (RGB 255,255,255), soft even studio lighting, subtle contact shadow. 8k clarity, square 1:1 ratio, no text."
            },
            "slot_2_side": {
                "file": slot2_name,
                "type": "Side Profile 90-degree Lateral 1:1",
                "prompt": f"Using the attached reference photos, create a clean e-commerce commercial product photograph of {raw_title} from a straight orthogonal 90-degree lateral side profile view. Highlighting boot shaft height, waterproof seamless contour, and sole thickness. Seamless pure white background (RGB 255,255,255), square 1:1 ratio, no text."
            },
            "slot_3_tread": {
                "file": slot3_name,
                "type": "Outsole Tread Cleat Detail 1:1",
                "prompt": f"Using the attached reference photos, create a high-definition commercial product photo of {raw_title} showcasing the bottom outsole tread pattern and anti-slip traction lugs. Pure white background (RGB 255,255,255), square 1:1 ratio, sharp focus."
            },
            "slot_4_usage": {
                "file": slot4_name,
                "type": "Contextual In-Use Field Scene 1:1",
                "prompt": f"Using the attached reference photos, create a realistic photograph of {raw_title} being actively worn on wet agricultural plantation terrain and muddy ground in outdoor daylight. Lower-body framing from knees down, no visible human faces, square 1:1 ratio, photorealistic."
            }
        },
        "photobank_ready": {
            "category_folder": target_category_folder,
            "category_group": target_group,
            "manifest_file": MANIFEST_CSV,
            "all_4_slots_ready": True
        }
    }

    prod_info["google_flow_and_photobank_slots"] = flow_payload
    with open(json_src, "w", encoding="utf-8") as jf:
        json.dump(prod_info, jf, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "sku": sku,
        "product_name": raw_title,
        "folder_name": folder_name,
        "category_folder": target_category_folder,
        "category_group": target_group,
        "variations_generated": results,
        "flow_project_url": FLOW_PROJECT_URL,
        "flow_account": FLOW_ACCOUNT_EMAIL,
        "photobank_manifest": MANIFEST_CSV
    }

def upload_sku_slots_to_photobank_admin(
    sku: str = "SHP-001",
    folder_name: str = "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC",
    api_endpoint: str = "https://admin.hotstrading.com/api/photobank/upload",
    session_cookie: Optional[str] = None,
    simulate: bool = False
) -> Dict[str, Any]:
    """
    Upload 4 slot image variations to Photobank Admin (https://admin.hotstrading.com/photo-bank).
    Supports simulation/dry-run mode for testing without modifying production.
    """
    clean_sku = sku.replace("-", "_")
    base_name = f"{clean_sku}_{folder_name[:25]}"
    
    prod_folder = os.path.join(SHOPEE_ASSETS_DIR, folder_name)
    json_path = os.path.join(prod_folder, f"{folder_name}.json")
    prod_name = folder_name.replace("_", " ")
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                j = json.load(f)
                prod_name = j.get("product_identification", {}).get("product_name_shopee") or prod_name
        except Exception:
            pass

    target_category_folder, target_group = resolve_category(prod_name)
    cat_dir = os.path.join(PHOTOBANK_DIR, target_category_folder)
    
    slots = [
        ("slot_1_hero", f"{base_name}_slot_1_hero.webp", "Hero White BG 1:1"),
        ("slot_2_side", f"{base_name}_slot_2_side.webp", "Side Profile 90-degree Lateral 1:1"),
        ("slot_3_tread", f"{base_name}_slot_3_tread.webp", "Outsole Tread Cleats 1:1"),
        ("slot_4_usage", f"{base_name}_slot_4_usage.webp", "Contextual In-Use Outdoor 1:1")
    ]
    
    upload_results = []
    
    for slot_id, fname, label in slots:
        fpath = os.path.join(cat_dir, fname)
        if not os.path.exists(fpath):
            fallback = os.path.join(prod_folder, fname)
            if os.path.exists(fallback):
                fpath = fallback
            else:
                upload_results.append({
                    "slot": slot_id,
                    "label": label,
                    "filename": fname,
                    "status": "skipped",
                    "error": "File belum digenerate"
                })
                continue
                
        file_size_kb = round(os.path.getsize(fpath) / 1024.0, 1)
        
        if simulate:
            upload_results.append({
                "slot": slot_id,
                "label": label,
                "filename": fname,
                "file_size_kb": file_size_kb,
                "status": "simulated_success",
                "api_endpoint": api_endpoint,
                "target_category": target_category_folder,
                "message": f"Simulasi POST multipart/form-data sukses ({file_size_kb} KB)"
            })
            continue

        headers = {}
        if session_cookie:
            headers["Cookie"] = session_cookie
            
        try:
            with open(fpath, "rb") as f:
                files = {"file": (fname, f, "image/webp")}
                data = {
                    "sku": sku,
                    "product_name": prod_name,
                    "category": target_category_folder,
                    "category_group": target_group,
                    "slot": slot_id
                }
                res = requests.post(api_endpoint, files=files, data=data, headers=headers, timeout=15)
                is_ok = res.status_code in (200, 201)
                upload_results.append({
                    "slot": slot_id,
                    "label": label,
                    "filename": fname,
                    "file_size_kb": file_size_kb,
                    "status_code": res.status_code,
                    "success": is_ok,
                    "response": res.text[:200]
                })
        except Exception as e:
            upload_results.append({
                "slot": slot_id,
                "label": label,
                "filename": fname,
                "file_size_kb": file_size_kb,
                "success": False,
                "error": str(e)
            })

    return {
        "success": True,
        "sku": sku,
        "product_name": prod_name,
        "simulated": simulate,
        "api_endpoint": api_endpoint,
        "category_folder": target_category_folder,
        "category_group": target_group,
        "results": upload_results
    }

if __name__ == "__main__":
    print("Testing Photobank API Bridge & Sample 4-Variation Generation...")
    summary = get_photobank_summary()
    print("Current Photobank Summary:")
    print(f"Total Files: {summary['total_photobank_files']}, Manifest: {summary['manifest_entries']}")
    
    print("\nRunning sample test for SHP-001 (AP Boots XTR Hitam)...")
    sample_res = generate_sample_4_variations()
    print(f"Sample generation success: {sample_res['success']}")
    print(f"Product: {sample_res['product_name']}")
    print(f"Category: {sample_res['category_folder']} ({sample_res['category_group']})")
    print(f"Variations: {len(sample_res['variations_generated'])} slots ready!")
    for v in sample_res['variations_generated']:
        print(f" - Slot {v['slot']} ({v['type']}): {v['filename']}")
