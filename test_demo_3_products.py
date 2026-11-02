import os
import sys
import json
import time

sys.path.append(os.path.abspath('App'))
from photobank_api_bridge import generate_product_variations_custom
from PIL import Image

products = [
    {
        "sku": "SHP-001",
        "folder": "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC",
        "name": "AP Boots XTR Hitam - Sepatu Boot PVC"
    },
    {
        "sku": "SHP-002",
        "folder": "AP_Boots_TERRA_ECO_3_Hitam_Sepatu_Boot_PVC",
        "name": "AP Boots TERRA ECO 3 Hitam - Sepatu Boot PVC"
    },
    {
        "sku": "SHP-003",
        "folder": "AP_Boots_AP_1_Hitam_Sepatu_Boots_PVC",
        "name": "AP Boots AP 1 Hitam - Sepatu Boots PVC"
    }
]

print("=" * 60)
print(" DEMO TEST: 4-SLOT IMAGE GENERATION FOR 3 PRODUCTS")
print(" Engine: Actual AI Diffusion (FLUX) + Smart Studio Framing")
print(" Target Resolution: 1000x1000 Square (Pure White & In-Use)")
print("=" * 60)

summary_results = []

for i, prod in enumerate(products, 1):
    print(f"\n[{i}/3] Processing: {prod['sku']} - {prod['name']}")
    start_t = time.time()
    
    res = generate_product_variations_custom(
        sku=prod["sku"],
        folder_name=prod["folder"],
        slots=[1, 2, 3, 4],
        target_size=1000,
        fill_ratio=0.85,
        save_to_shopee=True,
        save_to_flow=True,
        save_to_photobank=True,
        engine="ai_flux"
    )
    
    duration = round(time.time() - start_t, 2)
    success = res.get("success", False)
    variations = res.get("variations_generated", [])
    
    print(f" -> Result: {'SUCCESS' if success else 'FAILED'} (Time: {duration}s)")
    print(f" -> Category: {res.get('category_folder')}")
    
    slots_info = []
    for v in variations:
        path = v.get("path")
        file_exists = os.path.exists(path) if path else False
        img_size = "N/A"
        if file_exists:
            try:
                with Image.open(path) as img:
                    img_size = f"{img.width}x{img.height}"
            except Exception:
                pass
        
        file_size_kb = round(os.path.getsize(path)/1024, 1) if file_exists else 0
        ai_badge = "AI FLUX" if v.get("ai_generated") else "Studio Canvas"
        
        print(f"    Slot {v.get('slot')} ({v.get('type')}): {v.get('filename')} | Dim: {img_size} | Size: {file_size_kb} KB | Engine: {ai_badge}")
        slots_info.append({
            "slot": v.get("slot"),
            "type": v.get("type"),
            "filename": v.get("filename"),
            "dimension": img_size,
            "size_kb": file_size_kb,
            "engine": ai_badge,
            "path": path
        })
        
    summary_results.append({
        "sku": prod["sku"],
        "folder": prod["folder"],
        "name": prod["name"],
        "duration_sec": duration,
        "success": success,
        "slots": slots_info
    })

print("\n" + "=" * 60)
print(" DEMO EXECUTION COMPLETE!")
print("=" * 60)

with open("demo_test_results.json", "w", encoding="utf-8") as out:
    json.dump(summary_results, out, indent=2)
print("Summary report saved to: demo_test_results.json")
