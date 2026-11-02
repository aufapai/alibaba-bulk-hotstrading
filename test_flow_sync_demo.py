import os
import sys
import json
import base64
from PIL import Image

sys.path.append(os.path.abspath('App'))
from shopee_asset_manager import save_uploaded_product_image

print("=" * 60)
print(" DEMO TEST: GOOGLE FLOW SYNC TO LOCAL PRODUCT FOLDERS")
print(" Simulating Flow Tool 'Sync to Local Manager (:8888)'")
print("=" * 60)

test_products = [
    {
        "folder": "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC",
        "sku": "SHP-001",
        "name": "AP Boots XTR Hitam"
    },
    {
        "folder": "AP_Boots_TERRA_ECO_3_Hitam_Sepatu_Boot_PVC",
        "sku": "SHP-002",
        "name": "AP Boots TERRA ECO 3 Hitam"
    },
    {
        "folder": "AP_Boots_AP_1_Hitam_Sepatu_Boots_PVC",
        "sku": "SHP-003",
        "name": "AP Boots AP 1 Hitam"
    }
]

for p in test_products:
    folder = p["folder"]
    folder_path = os.path.join("Shopee_Product_Assets", folder)
    print(f"\nVerifying folder: {folder_path}")
    
    # Check all 4 files
    slots_found = {}
    for slot_type in ["hero", "side", "tread", "usage"]:
        fname = f"{slot_type}_{folder}.webp"
        fpath = os.path.join(folder_path, fname)
        if os.path.exists(fpath):
            with Image.open(fpath) as img:
                slots_found[slot_type] = {
                    "filename": fname,
                    "dimensions": f"{img.width}x{img.height}",
                    "size_kb": round(os.path.getsize(fpath) / 1024, 1)
                }
        else:
            slots_found[slot_type] = None

    print(f"[{p['sku']}] {p['name']}:")
    for st, info in slots_found.items():
        if info:
            print(f"  [OK] {st.upper():5} Slot: {info['filename']} ({info['dimensions']}, {info['size_kb']} KB)")
        else:
            print(f"  [--] {st.upper():5} Slot: Not found")
            
    # Check JSON inventory
    json_path = os.path.join(folder_path, f"{folder}.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as jf:
            jdata = json.load(jf)
        inv = jdata.get("local_assets_inventory", {})
        print(f"  [JSON] local_assets_inventory: {inv}")
    else:
        print(f"  [--] JSON file missing: {json_path}")

print("\n" + "=" * 60)
print(" FLOW SYNC VERIFICATION COMPLETE!")
print("=" * 60)
