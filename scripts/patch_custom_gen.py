# -*- coding: utf-8 -*-
"""
Upgrade App/photobank_api_bridge.py with generate_product_variations_custom & batch_generate_products_custom.
Allows user to pick exact slots [1, 2, 3, 4], resolution (1000, 1200, 1600), fill ratio, and storage targets without any MCP.
"""
import sys

def main():
    with open('App/photobank_api_bridge.py', 'r', encoding='utf-8') as f:
        content = f.read()

    new_functions = '''
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
'''

    # Replace generate_sample_4_variations to wrap generate_product_variations_custom
    target_start = 'def generate_sample_4_variations(sku: str = "SHP-001", folder_name: str = "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC") -> Dict[str, Any]:'
    
    # We will insert new_functions before def generate_sample_4_variations, and redefine generate_sample_4_variations to call generate_product_variations_custom
    if 'def generate_product_variations_custom' not in content:
        content = content.replace(target_start, new_functions + '\n\ndef generate_sample_4_variations(sku: str = "SHP-001", folder_name: str = "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC") -> Dict[str, Any]:\n    return generate_product_variations_custom(sku=sku, folder_name=folder_name, slots=[1, 2, 3, 4], target_size=1000, fill_ratio=0.85, save_to_shopee=True, save_to_flow=True, save_to_photobank=True)\n\ndef _legacy_generate_sample_4_variations(sku: str = "SHP-001", folder_name: str = "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC") -> Dict[str, Any]:', 1)
        print("Inserted generate_product_variations_custom and batch_generate_products_custom successfully!")
    else:
        print("Already contains generate_product_variations_custom")

    with open('App/photobank_api_bridge.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()

