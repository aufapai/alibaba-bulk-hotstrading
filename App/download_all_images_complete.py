import openpyxl
import os
import re
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = r"d:\Work\Hots\Product Input"
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
ROOT_IMAGES_DIR = os.path.join(BASE_DIR, "Images_Tokopedia")
OUTPUT_IMAGES_DIR = os.path.join(OUTPUT_DIR, "Images_Tokopedia")

os.makedirs(ROOT_IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)

# Load Shopee for image fallback
swb = openpyxl.load_workbook(os.path.join(BASE_DIR, 'Input', 'shopee-co-id-2026-09-23.xlsx'), data_only=True)
s_rows = list(swb.active.iter_rows(values_only=True))
shopee_lookup = {}
for sr in s_rows[1:]:
    s_name = sr[4]
    if s_name:
        # Shopee: hanya main image sr[11] yang di-load; non-main image sr[12..14] jangan di-load
        s_imgs = [sr[11]] if sr[11] else []
        clean_s = re.sub(r'[^a-z0-9]', '', str(s_name).lower())
        shopee_lookup[clean_s] = s_imgs

def to_public_url(raw_url):
    if not raw_url or not isinstance(raw_url, str):
        return None
    url = raw_url.strip()
    if not url.startswith('http'):
        return None
        
    if '.net/' in url:
        path = url.split('.net/')[1].split('?')[0]
    elif '.com/' in url:
        path = url.split('.com/')[1].split('?')[0]
    else:
        path = url.split('?')[0]
        
    if 'tos-maliva' in path:
        return f"https://p16-oec-va.ibyteimg.com/{path}"
    elif 'tos-alisg' in path:
        return f"https://p16-images-comn-sg.tokopedia-static.net/{path}"
    return url

def categorize_product(name):
    name_l = name.lower()
    if "terra" in name_l:
        return "01_AP_Terra_Series"
    elif "orca" in name_l:
        return "02_AP_Orca_Series"
    elif "chef" in name_l or "medic" in name_l:
        return "03_AP_Chef_Medical_Series"
    elif any(x in name_l for x in ["2003", "2005", "2007", "2011", "2015", "2017", "2018", "9506"]):
        return "04_AP_Boots_Green_Series"
    elif any(x in name_l for x in ["9905", "white", "putih", "black", "hitam", "ap 1 "]) and "terra" not in name_l and "star" not in name_l and "chef" not in name_l:
        return "05_AP_Boots_Black_White_Series"
    elif "safety" in name_l or "metaguard" in name_l or "s4" in name_l or "s5" in name_l:
        return "06_AP_Safety_Boots"
    elif "star" in name_l:
        return "07_AP_Kasual_Sneakers"
    elif "allbike" in name_l or "moto" in name_l or "hobby" in name_l:
        return "08_AP_Biker_Casual_Shoes"
    elif "kids" in name_l:
        return "09_AP_Kids_Boots"
    elif "clogs" in name_l or "995" in name_l or "sandal" in name_l or "selop" in name_l:
        return "10_AP_Sandals_Clogs"
    elif "bola" in name_l or "pantofel" in name_l or "977" in name_l or "insole" in name_l:
        return "11_AP_Specialty_Sports"
    else:
        return "12_AP_General_Boots"

def sanitize_folder_name(name):
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name)
    cleaned = re.sub(r'\s+', " ", cleaned).strip()
    return cleaned[:70]

def download_file(url, save_path):
    if os.path.exists(save_path) and os.path.getsize(save_path) > 2048:
        return True, "Already Exists"
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tokopedia.com/'
    }
    
    # Try public URL first
    pub_url = to_public_url(url)
    urls_to_try = [pub_url, url]
    if pub_url and 'p16-images-comn-sg' in pub_url:
        urls_to_try.append(pub_url.replace('p16-images-comn-sg', 'p19-images-comn-sg'))
    if pub_url and 'p16-oec-va' in pub_url:
        urls_to_try.append(pub_url.replace('p16-oec-va', 'p19-oec-va'))

    for u in urls_to_try:
        if not u: continue
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = resp.read()
                if len(data) > 1024:
                    with open(save_path, 'wb') as f:
                        f.write(data)
                    return True, f"Success ({len(data)} bytes)"
        except Exception:
            continue
            
    return False, "Failed all URL variations"

def main():
    print("Loading Tokopedia scraped dictionary...")
    from analyze_marketplace_inputs import tokopedia_dict
    
    print(f"Total Products to process: {len(tokopedia_dict)}")
    
    download_queue = []
    
    for idx, (url, prod) in enumerate(tokopedia_dict.items(), 1):
        raw_name = prod.get('name') or f"AP_Boots_{idx:03d}"
        category = categorize_product(raw_name)
        folder_name = sanitize_folder_name(raw_name)
        
        # Directories in both root and Output
        root_prod_dir = os.path.join(ROOT_IMAGES_DIR, category, folder_name)
        out_prod_dir = os.path.join(OUTPUT_IMAGES_DIR, category, folder_name)
        os.makedirs(root_prod_dir, exist_ok=True)
        os.makedirs(out_prod_dir, exist_ok=True)
        
        # Find all available image URLs for this product
        img_urls = []
        if prod.get('main_img'):
            img_urls.append(prod['main_img'])
            
        gallery = prod.get('gallery', '')
        if gallery:
            for line in gallery.split('\n'):
                line = line.strip()
                if line.startswith('http') and line not in img_urls:
                    img_urls.append(line)
                    
        # Fallback to Shopee main image if empty (non-main Shopee images excluded)
        clean_key = re.sub(r'[^a-z0-9]', '', raw_name.lower())
        for sk, sv in shopee_lookup.items():
            if sk in clean_key or clean_key[:12] in sk:
                if not img_urls and sv:
                    img_urls.append(sv[0])
                break
                
        # Queue downloads
        for img_i, img_u in enumerate(img_urls[:5], 1):
            filename = f"01_main_1600x1600.jpg" if img_i == 1 else f"{img_i:02d}_gallery.jpg"
            save_path = os.path.join(root_prod_dir, filename)
            save_path_out = os.path.join(out_prod_dir, filename)
            download_queue.append((img_u, save_path, save_path_out, raw_name, filename))

    print(f"Total download tasks queued: {len(download_queue)}")
    
    success = 0
    skipped = 0
    failed = 0
    
    # Run with 4 concurrent workers to avoid rate limits
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(download_file, item[0], item[1]): item for item in download_queue}
        for fut in as_completed(futures):
            item = futures[fut]
            try:
                ok, msg = fut.result()
                if ok:
                    # Sync to output folder
                    try:
                        shutil.copy2(item[1], item[2])
                    except Exception:
                        pass
                    if "Already" in msg:
                        skipped += 1
                    else:
                        success += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

    print("\n==========================================")
    print("DOWNLOAD COMPLETE!")
    print(f"Newly Downloaded: {success}")
    print(f"Already Existed: {skipped}")
    print(f"Failed: {failed}")
    print(f"Root Folder: {ROOT_IMAGES_DIR}")
    print(f"Output Folder: {OUTPUT_IMAGES_DIR}")
    print("==========================================")

if __name__ == '__main__':
    main()
