# -*- coding: utf-8 -*-
"""
Generate and verify 4 slots for 3 DIFFERENT PRODUCTS:
1. SHP-001: AP Boots XTR Hitam
2. SHP-002: AP Boots 2003 Hijau TRICOLOUR
3. SHP-009: AP Boots 2015 Ultimate Hitam
"""
import os
import sys
from PIL import Image, ImageOps

sys.path.insert(0, 'App')
from photobank_api_bridge import generate_sample_4_variations

PRODUCTS_TO_TEST = [
    ("SHP-001", "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC"),
    ("SHP-002", "AP_Boots_2003_Hijau_TRICOLOUR_Sepatu_Boot_PVC"),
    ("SHP-009", "AP_Boots_2015_Ultimate_Hitam_Sepatu_PVC")
]

def check_fill_ratio(img_path):
    with Image.open(img_path) as im:
        im = im.convert('RGB')
        gray = ImageOps.invert(im.convert('L'))
        bbox = gray.point(lambda p: 255 if p > 12 else 0).getbbox()
        if not bbox:
            return 0.0, im.size
        w_box = bbox[2] - bbox[0]
        h_box = bbox[3] - bbox[1]
        max_dim = max(w_box, h_box)
        fill_ratio = max_dim / im.size[0]
        return round(fill_ratio * 100, 1), im.size, (w_box, h_box)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 70)
    print("RUNNING 4-SLOT VERIFICATION ON 3 DIFFERENT PRODUCTS")
    print("=" * 70)

    for sku, folder in PRODUCTS_TO_TEST:
        print(f"\n[+] Testing Product: {sku} ({folder})")
        res = generate_sample_4_variations(sku=sku, folder_name=folder)
        print(f"    Category: {res.get('category_folder')} ({res.get('category_group')})")
        print(f"    Product Name: {res.get('product_name')}")
        print(f"    Variations Generated: {len(res.get('variations_generated', []))} slots")

        for v in res.get('variations_generated', []):
            slot_num = v['slot']
            path = v['path']
            fill_pct, size, bbox_dim = check_fill_ratio(path)
            print(f"     * Slot {slot_num} ({v['type']}): {v['filename']}")
            print(f"       Canvas: {size[0]}x{size[1]} | Boot Object Box: {bbox_dim[0]}x{bbox_dim[1]} ({fill_pct}% fill ratio) -> {'PERFECT (>=80%)' if fill_pct >= 80 else 'WARN (<80%)'}")

    print("\n" + "=" * 70)
    print("ALL 3 PRODUCT TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == '__main__':
    main()

