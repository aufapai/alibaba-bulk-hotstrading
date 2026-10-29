# -*- coding: utf-8 -*-
"""
HOTS Trading - Flow MCP to Photobank Pipeline CLI
Integrates Product Input -> Google Flow AI Image Generation -> Photobank Auto Push (https://admin.hotstrading.com/photo-bank)
"""

import sys
import os
import json
import argparse

# Pastikan encoding UTF-8 di Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Tambahkan App ke sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "App"))

from flow_photobank.pipeline import FlowPhotobankPipeline
from flow_photobank.product_json_exporter import load_products_data, build_product_jobs, export_jobs_to_json
from flow_photobank.photobank_pusher import PhotobankPusher

def main():
    parser = argparse.ArgumentParser(
        description="Integrasi Google Flow MCP dengan Product Input & Push ke Photobank Admin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh Penggunaan:
  1. Ekspor seluruh Product Input ke format JSON:
     python run_flow_photobank.py --export-json

  2. Ekspor untuk 1 SKU tertentu (misal: APB-016):
     python run_flow_photobank.py --export-json --sku APB-016

  3. Cek status server Flow MCP & kuota akun Google Flow:
     python run_flow_photobank.py --status

  4. Push file gambar yang sudah ada ke folder Photobank yang tepat:
     python run_flow_photobank.py --push-existing "Image Flow"
        """
    )
    parser.add_argument("--export-json", action="store_true", help="Ekspor daftar prompt produk ke file JSON")
    parser.add_argument("--output", type=str, default=None, help="Lokasi file output JSON (default: Output/flow_product_input_jobs.json)")
    parser.add_argument("--status", action="store_true", help="Cek status koneksi Google Flow MCP")
    parser.add_argument("--sku", type=str, default=None, help="Filter berdasarkan SKU produk tertentu")
    parser.add_argument("--limit", type=int, default=None, help="Batasi jumlah produk yang diproses")
    parser.add_argument("--push-existing", type=str, default=None, help="Folder berisi gambar jadi untuk langsung didorong ke kategori Photobank")

    args = parser.parse_args()
    pipeline = FlowPhotobankPipeline()

    # 1. Cek Status Flow MCP
    if args.status:
        status = pipeline.get_system_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return

    # 2. Push gambar yang sudah ada ke folder Photobank
    if args.push_existing:
        source_dir = os.path.abspath(args.push_existing)
        if not os.path.exists(source_dir):
            print(json.dumps({"error": f"Folder sumber tidak ditemukan: {source_dir}"}, indent=2))
            return
        
        pusher = PhotobankPusher()
        df = load_products_data()
        jobs = build_product_jobs(df)
        
        # Buat pemetaan target berdasarkan nama file atau SKU
        print(f"[*] Memproses file gambar dari: {source_dir} ke Photobank...")
        files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        results = []
        
        for f in files:
            file_path = os.path.join(source_dir, f)
            matched_job = None
            f_lower = f.lower()
            
            # Cocokkan dengan job SKU
            for j in jobs:
                sku_clean = j["sku"].lower().replace("-", "")
                prod_slug = j["product_name"].lower()
                if sku_clean in f_lower or j["sku"].lower() in f_lower or prod_slug in f_lower:
                    matched_job = j
                    break
            
            if matched_job:
                res = pusher.push_job_result(matched_job, file_path)
                results.append(res)
            else:
                # Default push to General
                dummy_job = {
                    "sku": "APB-GEN",
                    "product_name": "AP Boots General Industrial",
                    "target_folder": "11_General_Lifestyle_Boots",
                    "category_group": "General & Lifestyle",
                    "target_filename": f"APB-GEN_{f.split('.')[0]}.webp"
                }
                res = pusher.push_job_result(dummy_job, file_path)
                results.append(res)

        print(json.dumps({
            "status": "success",
            "total_processed": len(results),
            "destination": "Output/Photobank_Siap_Upload",
            "sample_results": results[:5]
        }, indent=2, ensure_ascii=False))
        return

    # 3. Default atau --export-json: Ekspor Product Input ke JSON
    out_file = args.output or os.path.join(BASE_DIR, "Output", "flow_product_input_jobs.json")
    print(f"[*] Membaca data Product Input & menyusun 4-slot photo prompts...")
    result = pipeline.generate_jobs_json(sku_filter=args.sku, limit=args.limit, output_file=out_file)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\n[✓] Berhasil mengekspor {result['total_jobs']} jobs ke:")
    print(f"    {result['output_file']}")

if __name__ == "__main__":
    main()
