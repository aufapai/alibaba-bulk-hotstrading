# -*- coding: utf-8 -*-
"""
Build Consolidated Flow Folder from Shopee Product Assets
Copies all hero images, side images, and enriched JSON metadata into a dedicated 'Flow' folder,
and creates master Flow generation prompt manifests.
"""

import os
import sys
import shutil
import json
import re

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "Shopee_Product_Assets")
TARGET_FLOW_DIR = os.path.join(BASE_DIR, "Flow")
INNER_FLOW_DIR = os.path.join(ASSETS_DIR, "Flow")

def ensure_dirs():
    os.makedirs(TARGET_FLOW_DIR, exist_ok=True)

def generate_flow_prompts(product_name, brand, color_guess="Black", material="PVC", is_safety=False):
    """Generate high-quality Google Flow / Image Gen prompts for Slot 1 Hero and Slot 2 Side Profile."""
    clean_title = product_name.split(' - ')[0].strip() if ' - ' in product_name else product_name.strip()
    full_display_name = clean_title if clean_title.lower().startswith(brand.lower()) else f"{brand} {clean_title}"
    
    toe_str = "with impact-resistant steel toe cap reinforcement" if is_safety else "flexible ergonomic plain toe"
    sole_str = "heavy-duty slip-resistant cleated lug rubber sole"
    mat_str = "high-grade injection-molded waterproof PVC"
    
    p1_hero = (
        f"Using the attached reference photos, create a professional e-commerce commercial studio product photograph of {full_display_name}. "
        f"Color: {color_guess}. Construction: {mat_str} with {toe_str} and {sole_str}. "
        f"Front 3/4 hero perspective angle, standing upright, centered, occupying roughly 85% of frame. "
        f"Seamless pure white background (RGB 255,255,255), soft even studio lighting, subtle natural contact shadow only underneath. "
        f"Ultra-sharp focus, commercial catalogue 8k clarity, square 1:1 ratio. No text, no watermark, no extraneous props."
    )
    
    p2_side = (
        f"Using the attached reference photos, create a clean e-commerce commercial product photograph of {full_display_name} ({color_guess}) "
        f"from a straight orthogonal 90-degree lateral side profile view. "
        f"Highlighting the boot shaft height, waterproof seamless contour, vamp curve, and {sole_str} thickness. "
        f"Seamless pure white background (RGB 255,255,255), studio lighting, centered, 85% frame, square 1:1 ratio, sharp focus, no text, no watermark."
    )
    
    return p1_hero, p2_side

def run_build():
    ensure_dirs()
    print("=================================================================")
    print(" BUILDING CONSOLIDATED 'Flow' FOLDER FROM SHOPEE PRODUCT ASSETS")
    print(f" Source: {ASSETS_DIR}")
    print(f" Target: {TARGET_FLOW_DIR}")
    print("=================================================================")

    subfolders = [
        d for d in os.listdir(ASSETS_DIR) 
        if os.path.isdir(os.path.join(ASSETS_DIR, d)) and d != "Flow"
    ]
    subfolders.sort()
    print(f"Found {len(subfolders)} product folders in Shopee_Product_Assets.")

    copied_hero = 0
    copied_side = 0
    copied_json = 0
    master_records = []

    for idx, folder in enumerate(subfolders):
        folder_path = os.path.join(ASSETS_DIR, folder)
        files = os.listdir(folder_path)
        
        hero_file = next((f for f in files if f.startswith("hero_") and f.endswith(".webp")), None)
        side_file = next((f for f in files if f.startswith("side_") and f.endswith(".webp")), None)
        json_file = next((f for f in files if f.endswith(".json")), None)
        
        # Load existing JSON metadata
        json_data = {}
        if json_file:
            try:
                with open(os.path.join(folder_path, json_file), "r", encoding="utf-8") as jf:
                    json_data = json.load(jf)
            except Exception as e:
                print(f"[!] Error reading JSON in {folder}: {e}")

        prod_id = json_data.get("product_identification", {})
        prod_name = prod_id.get("product_name_shopee") or folder.replace("_", " ")
        brand = prod_id.get("brand") or ("Petrova" if "petrova" in folder.lower() else "AP Boots")
        sku = prod_id.get("sku") or f"SHP-{idx+1:03d}"
        
        # Detect color
        colors = ['Hitam', 'Black', 'Kuning', 'Yellow', 'Hijau', 'Green', 'Putih', 'White', 'Abu', 'Grey', 'Orange', 'Biru', 'Blue', 'Pink', 'Tosca', 'Coklat', 'Brown']
        detected_c = "Black"
        for c in colors:
            if c.lower() in prod_name.lower():
                detected_c = c
                break
                
        is_safety = any(s in prod_name.upper() for s in ['SAFETY', 'S4', 'S5', 'METAGUARD', 'STRENGTH', 'ULTIMATE', 'PHENOM', 'ERGOS'])
        
        p1_prompt, p2_side_prompt = generate_flow_prompts(prod_name, brand, detected_c, "PVC", is_safety)
        
        # 1. Copy Hero image
        dest_hero = None
        if hero_file:
            src_hero_path = os.path.join(folder_path, hero_file)
            dest_hero_path = os.path.join(TARGET_FLOW_DIR, hero_file)
            shutil.copy2(src_hero_path, dest_hero_path)
            copied_hero += 1
            dest_hero = hero_file

        # 2. Copy Side image
        dest_side = None
        if side_file:
            src_side_path = os.path.join(folder_path, side_file)
            dest_side_path = os.path.join(TARGET_FLOW_DIR, side_file)
            shutil.copy2(src_side_path, dest_side_path)
            copied_side += 1
            dest_side = side_file

        # 3. Enrich & Copy JSON
        enriched_json = dict(json_data)
        enriched_json["flow_ai_generation_prompts"] = {
            "flow_prompt_slot1_hero": p1_prompt,
            "flow_prompt_slot2_side": p2_side_prompt,
            "flow_settings": {
                "aspect_ratio": "1:1",
                "resolution": "1080p",
                "engine": "Google Flow / Flow MCP (flow_agent_images)",
                "credits_cost": 0,
                "background_specification": "Pure White (#FFFFFF, RGB 255, 255, 255)",
                "hero_reference_file": dest_hero,
                "side_reference_file": dest_side
            }
        }
        
        dest_json_name = json_file if json_file else f"{folder}.json"
        dest_json_path = os.path.join(TARGET_FLOW_DIR, dest_json_name)
        with open(dest_json_path, "w", encoding="utf-8") as out_j:
            json.dump(enriched_json, out_j, indent=2, ensure_ascii=False)
        copied_json += 1

        master_records.append({
            "index": idx + 1,
            "sku": sku,
            "brand": brand,
            "product_name": prod_name,
            "folder_name": folder,
            "hero_image": dest_hero,
            "side_image": dest_side,
            "json_file": dest_json_name,
            "prompt_slot1_hero": p1_prompt,
            "prompt_slot2_side": p2_side_prompt,
            "b2b_title": enriched_json.get("product_title_b2b", prod_name)
        })

    # 4. Generate Master Flow Catalog JSON in Flow/
    master_json_path = os.path.join(TARGET_FLOW_DIR, "flow_all_products_master.json")
    with open(master_json_path, "w", encoding="utf-8") as mf:
        json.dump({
            "catalog_name": "Shopee Official Catalog - Flow Master Asset & Prompt Pack",
            "total_products": len(master_records),
            "generated_date": "2026-10-29",
            "manufacturer": "PT Waru Gunung",
            "export_partner": "PT Indo Sukses Semesta",
            "products": master_records
        }, mf, indent=2, ensure_ascii=False)

    # 5. Generate Markdown Reference Cheatsheet in Flow/
    master_md_path = os.path.join(TARGET_FLOW_DIR, "flow_prompts_cheatsheet.md")
    with open(master_md_path, "w", encoding="utf-8") as md:
        md.write("# 🟧 MASTER FLOW PROMPTS & ASSETS (123 SKU SHOPEE RESMI)\n")
        md.write("**Direktori:** `d:\\Work\\Hots\\Product Input\\Flow\\`  \n")
        md.write("**Legal Manufacturer:** PT Waru Gunung (Surabaya)  \n")
        md.write("**Export Partner:** PT Indo Sukses Semesta (HOTS Trading)  \n")
        md.write(f"**Total Produk:** {len(master_records)} SKU (AP Boots & Petrova)  \n\n---\n\n")
        
        for r in master_records:
            md.write(f"## {r['index']}. [{r['sku']}] {r['product_name']} ({r['brand']})\n")
            md.write(f"* **Hero Image:** `{r['hero_image']}`\n")
            md.write(f"* **Side Image:** `{r['side_image']}`\n")
            md.write(f"* **JSON Metadata:** `{r['json_file']}`\n\n")
            md.write("### 🌟 Prompt Slot 1 - Hero White BG (1:1)\n")
            md.write(f"```text\n{r['prompt_slot1_hero']}\n```\n\n")
            md.write("### 📐 Prompt Slot 2 - Side Profile 90° (1:1)\n")
            md.write(f"```text\n{r['prompt_slot2_side']}\n```\n\n---\n\n")

    # 6. Mirror to Shopee_Product_Assets/Flow
    try:
        os.makedirs(INNER_FLOW_DIR, exist_ok=True)
        # copy master files into INNER_FLOW_DIR as well
        shutil.copy2(master_json_path, os.path.join(INNER_FLOW_DIR, "flow_all_products_master.json"))
        shutil.copy2(master_md_path, os.path.join(INNER_FLOW_DIR, "flow_prompts_cheatsheet.md"))
        print(f"[+] Mirrored master manifests to {INNER_FLOW_DIR}")
    except Exception as e:
        print(f"[!] Warning mirroring to inner flow: {e}")

    print("\n-----------------------------------------------------------------")
    print(" FLOW BUILD SUMMARY:")
    print(f" - Hero Images Copied: {copied_hero} files")
    print(f" - Side Images Copied: {copied_side} files")
    print(f" - JSON Specs Enriched & Copied: {copied_json} files")
    print(f" - Master Flow JSON: {master_json_path}")
    print(f" - Master Flow Markdown: {master_md_path}")
    print(f" - Total Files in Flow directory: {len(os.listdir(TARGET_FLOW_DIR))}")
    print("=================================================================")

if __name__ == "__main__":
    run_build()
