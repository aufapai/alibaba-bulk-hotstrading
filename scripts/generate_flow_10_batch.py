# -*- coding: utf-8 -*-
"""
Autonomous Batch Visual Generation for 10 Products (Always Approve Mode)
PT Waru Gunung / HOTS Trading (aufahots@gmail.com)
Target Flow: https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c
"""

import os
import sys
import json
import time

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "App"))

from photobank_api_bridge import (
    generate_product_variations_custom, get_flow_10_bundle, create_flow_batch_zip
)
from PIL import Image

def run_10_product_batch():
    print("=" * 70)
    print(" 🚀 GOOGLE FLOW 10-PRODUCT BATCH VISUAL GENERATOR (ALWAYS APPROVE)")
    print(" Target Project : https://flow.google.com/project/5a88c3fd-477c-4eed-a126-f812ccfb079c")
    print(" Account        : aufahots@gmail.com")
    print(" Output Mode    : 4 Slots per Product (10 x 4 = 40 Square 1:1 Images)")
    print("=" * 70)

    # 1. Get the bundle metadata
    bundle = get_flow_10_bundle(max_products=10)
    prods = bundle["coupled_products"]
    total = len(prods)
    print(f"\n[INFO] Loaded {total} products for batch processing.")

    # Save prompt file for user convenience
    doc_out = os.path.join(BASE_DIR, "Doc", "FLOW_10_PRODUCTS_AGENT_PROMPT.md")
    with open(doc_out, "w", encoding="utf-8") as pf:
        pf.write(f"# GOOGLE FLOW 10-PRODUCT AGENT MASTER PROMPT\n\n```text\n{bundle['agent_prompt']}\n```\n")
    print(f"[INFO] Master Agent Prompt saved to: {doc_out}")

    batch_summary = []
    total_slots = 0

    for idx, p in enumerate(prods, 1):
        sku = p["sku"]
        folder = p["folder_name"]
        name = p["product_name"]
        print(f"\n[{idx}/{total}] Processing {sku}: {name} ({folder})...")
        t0 = time.time()

        res = generate_product_variations_custom(
            sku=sku,
            folder_name=folder,
            slots=[1, 2, 3, 4],
            target_size=1000,
            fill_ratio=0.85,
            save_to_shopee=True,
            save_to_flow=True,
            save_to_photobank=True,
            engine="ai_flux"
        )
        elapsed = round(time.time() - t0, 2)
        vars_gen = res.get("variations_generated", [])
        total_slots += len(vars_gen)

        print(f" -> Completed in {elapsed}s | Created {len(vars_gen)} slots (Category: {res.get('category_folder')})")
        for v in vars_gen:
            ai_tag = "AI FLUX" if v.get("ai_generated") else "Studio Canvas"
            print(f"    - Slot {v.get('slot')} ({v.get('type')}): {v.get('filename')} [{ai_tag}]")

        batch_summary.append({
            "sku": sku,
            "folder": folder,
            "name": name,
            "duration_sec": elapsed,
            "slots": vars_gen
        })

    # Create ZIP archive
    zip_bytes = create_flow_batch_zip(max_products=10)
    out_dir = os.path.join(BASE_DIR, "Output")
    os.makedirs(out_dir, exist_ok=True)
    zip_path = os.path.join(out_dir, "Flow_10_Products_Assets_HOTS.zip")
    with open(zip_path, "wb") as zf:
        zf.write(zip_bytes)

    print("\n" + "=" * 70)
    print(f" 🎉 BATCH COMPLETED! Total: {total_slots} images created across {total} products.")
    print(f" 📦 ZIP Package created : {zip_path} ({round(len(zip_bytes)/(1024*1024), 2)} MB)")
    print("=" * 70)

if __name__ == "__main__":
    run_10_product_batch()
