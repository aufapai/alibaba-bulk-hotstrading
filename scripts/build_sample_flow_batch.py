# -*- coding: utf-8 -*-
"""
Generate sample_3_products_for_flow_tool.json with Base64 reference images.
"""
import os
import json
import base64

PRODUCTS = [
    ("SHP-001", "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC"),
    ("SHP-002", "AP_Boots_2003_Hijau_TRICOLOUR_Sepatu_Boot_PVC"),
    ("SHP-009", "AP_Boots_2015_Ultimate_Hitam_Sepatu_PVC")
]

def to_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
        ext = os.path.splitext(path)[1].lower().replace(".", "")
        mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
        return f"data:{mime};base64,{b64}"

output_data = []

for sku, folder in PRODUCTS:
    json_path = os.path.join("Shopee_Product_Assets", folder, f"{folder}.json")
    hero_path = os.path.join("Shopee_Product_Assets", folder, f"hero_{folder}.webp")
    side_path = os.path.join("Shopee_Product_Assets", folder, f"side_{folder}.webp")
    
    prod_dict = {}
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as jf:
            prod_dict = json.load(jf)
            
    prod_dict["reference_images"] = {
        "hero_data_url": to_base64(hero_path),
        "side_data_url": to_base64(side_path)
    }
    output_data.append(prod_dict)

out_file = os.path.join("Flow_Tool_React_App", "sample_3_products_for_flow_tool.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Generated {out_file} with {len(output_data)} products successfully!")

