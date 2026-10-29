# -*- coding: utf-8 -*-
"""
Product Input to JSON Exporter for Flow MCP & Photobank
Converts master product catalogs into structured JSON jobs ready for Google Flow generation.
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from .category_mapper import resolve_photobank_category, generate_photobank_filename

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DEFAULT_INPUT_CSV = os.path.join(PROJECT_ROOT, "photobank generator", "Alibaba_Master_106_SKU_ImageGen_Ready.csv")
FALLBACK_INPUT_CSV = os.path.join(PROJECT_ROOT, "products.csv")

SLOT_DEFINITIONS = [
    {
        "slot_key": "slot_1_hero",
        "slot_label": "Slot 1 - Hero White BG",
        "csv_col": "Prompt_Slot1_Hero_WhiteBG",
        "alt_csv_col": "slot_1_hero_prompt",
        "aspect": "1:1",
        "technique": "product_hero_white_bg"
    },
    {
        "slot_key": "slot_2_side",
        "slot_label": "Slot 2 - Side Profile",
        "csv_col": "Prompt_Slot2_Side_Profile",
        "alt_csv_col": "slot_2_side_prompt",
        "aspect": "1:1",
        "technique": "product_side_profile"
    },
    {
        "slot_key": "slot_3_tread",
        "slot_label": "Slot 3 - Outsole Tread",
        "csv_col": "Prompt_Slot3_Outsole_Tread",
        "alt_csv_col": "slot_3_detail_prompt",
        "aspect": "1:1",
        "technique": "outsole_cleat_detail"
    },
    {
        "slot_key": "slot_4_contextual",
        "slot_label": "Slot 4 - Contextual In-Use",
        "csv_col": "Prompt_Slot4_Contextual_Usage",
        "alt_csv_col": "slot_4_usage_prompt",
        "aspect": "1:1",
        "technique": "commercial_in_use"
    }
]

def load_products_data(csv_path: Optional[str] = None) -> pd.DataFrame:
    """Memuat data produk dari file CSV master."""
    if not csv_path or not os.path.exists(csv_path):
        if os.path.exists(DEFAULT_INPUT_CSV):
            csv_path = DEFAULT_INPUT_CSV
        elif os.path.exists(FALLBACK_INPUT_CSV):
            csv_path = FALLBACK_INPUT_CSV
        else:
            raise FileNotFoundError(f"File produk tidak ditemukan di {DEFAULT_INPUT_CSV} maupun {FALLBACK_INPUT_CSV}")

    df = pd.read_csv(csv_path, dtype=str).fillna("")
    return df

def build_product_jobs(df: pd.DataFrame, sku_filter: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Mengubah baris tabel produk menjadi daftar job JSON siap kirim ke Flow MCP.
    """
    jobs = []
    
    # Deteksi nama kolom secara fleksibel
    sku_col = 'SKU code' if 'SKU code' in df.columns else ('id' if 'id' in df.columns else 'sku')
    title_col = '* Product title' if '* Product title' in df.columns else ('product_name' if 'product_name' in df.columns else 'name')
    img_col = '* Product image 1' if '* Product image 1' in df.columns else ('source_image_url' if 'source_image_url' in df.columns else 'image_url')
    cat_col = 'Category' if 'Category' in df.columns else ('category' if 'category' in df.columns else '')

    processed_count = 0
    for idx, row in df.iterrows():
        sku = str(row.get(sku_col, "")).strip()
        title = str(row.get(title_col, "")).strip()
        ref_image = str(row.get(img_col, "")).strip()
        category_str = str(row.get(cat_col, "")).strip() if cat_col else ""

        if not sku or not title:
            continue

        if sku_filter and sku_filter.upper() not in sku.upper():
            continue

        folder_name, group_name, clean_prod_name = resolve_photobank_category(sku, title, category_str)

        # Build each of the 4 slots
        product_slots = []
        for slot_def in SLOT_DEFINITIONS:
            slot_key = slot_def["slot_key"]
            prompt = str(row.get(slot_def["csv_col"], "")).strip()
            if not prompt and slot_def["alt_csv_col"] in row:
                prompt = str(row.get(slot_def["alt_csv_col"], "")).strip()

            target_filename = generate_photobank_filename(sku, clean_prod_name, slot_key, "webp")

            # Standar Payload Flow MCP
            flow_job = {
                "job_id": f"{sku}_{slot_key}",
                "sku": sku,
                "product_name": clean_prod_name,
                "full_title": title,
                "slot_key": slot_key,
                "slot_label": slot_def["slot_label"],
                "target_folder": folder_name,
                "category_group": group_name,
                "target_filename": target_filename,
                "reference_image": ref_image,
                "prompt": prompt,
                "flow_payload": {
                    "prompt": prompt,
                    "type": "image",
                    "aspect": slot_def["aspect"],
                    "resolution": "1080p",
                    "reference_images": [ref_image] if ref_image.startswith("http") else [],
                    "max_credits": 0  # 0 credits for free stills / Agent batch
                },
                "status": "ready"
            }
            product_slots.append(flow_job)
            jobs.append(flow_job)

        processed_count += 1
        if limit and processed_count >= limit:
            break

    return jobs

def export_jobs_to_json(jobs: List[Dict[str, Any]], output_file: str) -> str:
    """Menyimpan seluruh job ke dalam file JSON."""
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "total_jobs": len(jobs),
            "total_products": len({j["sku"] for j in jobs}),
            "jobs": jobs
        }, f, indent=2, ensure_ascii=False)
    return output_file
