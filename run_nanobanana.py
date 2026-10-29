import os
import sys
import time
import json
import base64
import requests
import pandas as pd
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# 1. Load API Key dari file .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Bro, GEMINI_API_KEY belum dipasang di file .env!")

# Konfigurasi Folder & File
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "products.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "products_completed.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_images")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Endpoint Google Gemini API untuk Image Generation (Nano Banana)
MODEL_NAME = "gemini-2.5-flash-image"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

def download_image_as_base64(url):
    """Mengunduh gambar dari URL dan mengonversinya menjadi Base64 + MIME Type."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # Validasi dengan PIL Image
        img = Image.open(BytesIO(response.content))
        mime_type = "image/jpeg" if img.format == "JPEG" else "image/png"
        b64_data = base64.b64encode(response.content).decode("utf-8")
        return b64_data, mime_type
    except Exception as e:
        print(f"  [!] Gagal download gambar dari URL ({url[:60]}...): {e}")
        return None, None

def call_nano_banana_api(b64_img, mime_type, prompt):
    """Mengirim gambar referensi + prompt ke Gemini Nano Banana API."""
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": b64_img
                        }
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE"]
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        res_json = response.json()
        candidates = res_json.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            for p in parts:
                if "inlineData" in p:
                    img_bytes = base64.b64decode(p["inlineData"]["data"])
                    return True, img_bytes, "OK"
        return False, None, "No inlineData in response"
    elif response.status_code == 429:
        err_msg = response.text
        if "limit: 0" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
            return False, None, "QUOTA_LIMIT_0: Model Nano Banana (image gen) membutuhkan Billing aktif pada project Google AI Studio/GCP (Pay-as-you-go)."
        return False, None, f"RATE_LIMIT_429: {err_msg[:120]}"
    else:
        return False, None, f"HTTP_{response.status_code}: {response.text[:150]}"

def process_product_slot(prod_id, prod_name, img_url, slot_name, prompt):
    """Memproses 1 slot foto produk dengan Nano Banana."""
    print(f"  [*] Mengenerate [{slot_name}] untuk {prod_name}...")
    
    b64_img, mime_type = download_image_as_base64(img_url)
    if not b64_img:
        return None, "FAILED_IMAGE_DOWNLOAD"
        
    success, img_bytes, msg = call_nano_banana_api(b64_img, mime_type, prompt)
    if success:
        out_name = f"{prod_id}_{slot_name}.png"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"    [+] Sukses! Tersimpan di: {out_path}")
        return out_path, "SUCCESS"
    else:
        print(f"    [!] Gagal ({msg})")
        return None, msg

def main():
    print("===================================================================")
    print("      NANO BANANA AI PRODUCT IMAGE GENERATION (ALIBABA SOP)")
    print("           PT Indo Sukses Semesta - AP Boots Indonesia")
    print("===================================================================")
    print(f"Model       : {MODEL_NAME}")
    print(f"Database    : {INPUT_CSV}")
    print(f"Output Dir  : {OUTPUT_DIR}")
    print("===================================================================\n")

    if not os.path.exists(INPUT_CSV):
        print(f"[!] File {INPUT_CSV} tidak ditemukan. Jalankan App/prepare_products_csv.py terlebih dahulu.")
        return

    df = pd.read_csv(INPUT_CSV)
    print(f"[*] Ditemukan {len(df)} produk di {INPUT_CSV}.")

    # Pilihan slot foto sesuai alibaba-product-photo-guide.md
    slots = [
        ("01_hero", "slot_1_hero_prompt"),
        ("02_side_a", "slot_2_side_prompt"),
        ("03_side_b", "slot_3_detail_prompt"),
        ("04_usage", "slot_4_usage_prompt")
    ]

    results = []

    for idx, row in df.iterrows():
        prod_id = row['id']
        prod_name = row['product_name']
        img_url = row['source_image_url']
        
        print(f"\n[{idx+1}/{len(df)}] Memproses Produk: [{prod_id}] {prod_name}")
        
        row_res = row.to_dict()
        
        for slot_code, prompt_col in slots:
            prompt = row.get(prompt_col)
            if not prompt or pd.isna(prompt):
                continue
                
            saved_path, status = process_product_slot(prod_id, prod_name, img_url, slot_code, prompt)
            row_res[f"{slot_code}_path"] = saved_path or ""
            row_res[f"{slot_code}_status"] = status
            
            # Jika kuota 0 (perlu billing), hentikan agar tidak looping error
            if "QUOTA_LIMIT_0" in status:
                print("\n===================================================================")
                print("[!] CATATAN KUOTA PENTING:")
                print("    Google AI Studio menerapkan kuota limit: 0 (Free Tier) untuk fitur")
                print("    IMAGE GENERATION (gemini-2.5-flash-image / Nano Banana).")
                print("    Untuk membuka akses generate gambar, aktifkan Billing Pay-as-you-go")
                print("    pada project Google AI Studio Anda di:")
                print("    -> https://aistudio.google.com/app/plan_and_billing")
                print("===================================================================\n")
                results.append(row_res)
                # Save partial progress
                out_df = pd.DataFrame(results)
                out_df.to_csv(OUTPUT_CSV, index=False)
                return

            time.sleep(2) # Safe delay between requests

        results.append(row_res)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[OK] Selesai! Hasil tercatat di {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
