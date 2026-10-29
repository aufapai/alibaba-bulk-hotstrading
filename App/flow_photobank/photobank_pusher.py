# -*- coding: utf-8 -*-
"""
Photobank Pusher & File Organizer
Pushes generated product photos into official Photobank category folders and updates manifest.
Target website: https://admin.hotstrading.com/photo-bank
"""

import os
import csv
import json
import shutil
from typing import Dict, Any, Optional
from PIL import Image
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
PHOTOBANK_ROOT = os.path.join(PROJECT_ROOT, "Output", "Photobank_Siap_Upload")
MANIFEST_CSV = os.path.join(PHOTOBANK_ROOT, "DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv")

def ensure_photobank_folders():
    """Memastikan folder root Photobank dan sub-folder 11 kategori tersedia."""
    os.makedirs(PHOTOBANK_ROOT, exist_ok=True)
    categories = [
        "01_Safety_Boots", "02_Terra_Series", "03_Orca_Series", "04_Chef_Series",
        "05_Medic_Series", "06_Biker_Casual", "07_Classic_Boots", "08_Kids_Boots",
        "09_Sandals_Clogs", "10_Kasual_Sneakers", "11_General_Lifestyle_Boots"
    ]
    for c in categories:
        os.makedirs(os.path.join(PHOTOBANK_ROOT, c), exist_ok=True)

def process_and_save_webp(source_img_path: str, dest_folder: str, filename: str, target_size: int = 1600, quality: int = 90) -> str:
    """
    Mengonversi gambar menjadi format WebP beresolusi tinggi (standar e-commerce / Alibaba 1600x1600).
    """
    ensure_photobank_folders()
    target_dir = os.path.join(PHOTOBANK_ROOT, dest_folder)
    os.makedirs(target_dir, exist_ok=True)
    
    if not filename.lower().endswith(".webp"):
        filename = f"{os.path.splitext(filename)[0]}.webp"

    dest_path = os.path.join(target_dir, filename)

    try:
        with Image.open(source_img_path) as img:
            img = img.convert("RGB")
            
            # Jika rasio kotak dan perlu resize
            w, h = img.size
            if max(w, h) > target_size:
                img.thumbnail((target_size, target_size), Image.Resampling.LANCZOS)
            
            img.save(dest_path, "WEBP", quality=quality, method=6)
            return dest_path
    except Exception as e:
        print(f"[!] Gagal konversi WebP ({source_img_path}): {e}")
        # Fallback copy
        shutil.copy2(source_img_path, dest_path)
        return dest_path

def append_to_photobank_manifest(original_name: str, new_name: str, sku: str, product_name: str, 
                                 category_group: str, folder_name: str, file_path: str):
    """
    Menambahkan entri ke DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv
    """
    file_size_kb = 0.0
    if os.path.exists(file_path):
        file_size_kb = round(os.path.getsize(file_path) / 1024.0, 1)

    file_exists = os.path.exists(MANIFEST_CSV)
    
    existing_files = set()
    if file_exists:
        try:
            with open(MANIFEST_CSV, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for r in reader:
                    if len(r) > 1:
                        existing_files.add(r[1])
        except Exception:
            pass

    # Jangan tulis duplikat jika file sudah terdaftar
    if new_name in existing_files:
        return

    with open(MANIFEST_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["original_filename", "new_filename", "sku_prefix", "product_name", "category_group", "folder_name", "file_size_kb"])
        writer.writerow([original_name, new_name, sku, product_name, category_group, folder_name, file_size_kb])

class PhotobankPusher:
    def __init__(self, photobank_dir: str = PHOTOBANK_ROOT):
        self.photobank_dir = photobank_dir
        ensure_photobank_folders()

    def push_job_result(self, job_dict: Dict[str, Any], source_image_path: str) -> Dict[str, Any]:
        """
        Menerima hasil generate gambar dari Flow MCP dan langsung mendorongnya ke folder Photobank yang tepat.
        """
        sku = job_dict.get("sku", "APB-GEN")
        prod_name = job_dict.get("product_name", "AP Boots")
        folder = job_dict.get("target_folder", "11_General_Lifestyle_Boots")
        group_name = job_dict.get("category_group", "General & Lifestyle")
        target_filename = job_dict.get("target_filename", f"{sku}_img.webp")
        orig_filename = os.path.basename(source_image_path)

        saved_path = process_and_save_webp(
            source_img_path=source_image_path,
            dest_folder=folder,
            filename=target_filename
        )

        append_to_photobank_manifest(
            original_name=orig_filename,
            new_name=os.path.basename(saved_path),
            sku=sku,
            product_name=prod_name,
            category_group=group_name,
            folder_name=folder,
            file_path=saved_path
        )

        file_size_kb = round(os.path.getsize(saved_path) / 1024.0, 1)

        result = {
            "success": True,
            "sku": sku,
            "product_name": prod_name,
            "category_folder": folder,
            "category_group": group_name,
            "saved_file": saved_path,
            "filename": os.path.basename(saved_path),
            "file_size_kb": file_size_kb,
            "photobank_ready": True
        }
        return result

    def upload_to_admin_server(self, file_path: str, sku: str, product_name: str, 
                               api_endpoint: str = "https://admin.hotstrading.com/api/photobank/upload",
                               session_cookie: Optional[str] = None) -> Dict[str, Any]:
        """
        Push langsung via HTTP POST multipart ke admin.hotstrading.com/photo-bank
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File tidak ditemukan: {file_path}"}

        headers = {}
        if session_cookie:
            headers["Cookie"] = session_cookie

        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f, "image/webp")}
                data = {
                    "sku": sku,
                    "product_name": product_name,
                    "category": "product"
                }
                res = requests.post(api_endpoint, files=files, data=data, headers=headers, timeout=60)
                if res.status_code == 200:
                    return {"success": True, "response": res.json() if "json" in res.headers.get("content-type", "") else res.text}
                return {"success": False, "status_code": res.status_code, "error": res.text[:200]}
        except Exception as e:
            return {"success": False, "error": str(e)}
