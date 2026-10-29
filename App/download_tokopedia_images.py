import openpyxl
import os
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = r"d:\Work\Hots\Product Input"
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
IMAGES_BASE = os.path.join(OUTPUT_DIR, "Images_Tokopedia")
os.makedirs(IMAGES_BASE, exist_ok=True)

# Helper to convert signed CDN to public CDN
def get_public_cdn_url(url):
    if not url or not isinstance(url, str):
        return None
    url = url.strip()
    if not url.startswith('http'):
        return None
    
    # Clean query parameters
    path = url.split('.net/')[1].split('?')[0] if '.net/' in url else url.split('?')[0]
    
    # If it's a Tokopedia CDN URL
    if 'tokopedia-static.net' in url or 'tokopedia.net' in url:
        if 'p19-' in url:
            return f"https://p19-images-comn-sg.tokopedia-static.net/{path}"
        return f"https://p16-images-comn-sg.tokopedia-static.net/{path}"
    
    return url

def categorize_product(name, desc=""):
    name_l = name.lower()
    desc_l = desc.lower() if desc else ""
    
    if "terra" in name_l:
        return "01_AP_Terra_Series"
    elif "orca" in name_l:
        return "02_AP_Orca_Series"
    elif "chef" in name_l or "medic" in name_l:
        return "03_AP_Chef_Medical_Series"
    elif any(x in name_l for x in ["2003", "2005", "2007", "2011", "2015", "2017", "2018", "9506"]):
        return "04_AP_Boots_Green_Series"
    elif any(x in name_l for x in ["9905", "white", "putih", "black (", "hitam (", "ap 1 "]):
        return "05_AP_Boots_Black_White_Series"
    elif "safety" in name_l or "metaguard" in name_l or "s4" in name_l or "s5" in name_l or "max" in name_l:
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
    # Keep alphanumeric and simple dash/underscore
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name)
    cleaned = re.sub(r'\s+', " ", cleaned).strip()
    return cleaned[:60]

def download_single_image(url, save_path):
    if os.path.exists(save_path) and os.path.getsize(save_path) > 1024:
        return True, save_path, "Already Exists"
    
    pub_url = get_public_cdn_url(url)
    if not pub_url:
        return False, save_path, "Invalid URL"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.tokopedia.com/'
    }
    
    # Try public host first
    try_urls = [pub_url]
    if 'p16-' in pub_url:
        try_urls.append(pub_url.replace('p16-', 'p19-'))
    elif 'p19-' in pub_url:
        try_urls.append(pub_url.replace('p19-', 'p16-'))
    try_urls.append(url) # fallback to original url
    
    for u in try_urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                if len(data) > 500:
                    with open(save_path, 'wb') as f:
                        f.write(data)
                    return True, save_path, f"Downloaded ({len(data)} bytes)"
        except Exception:
            continue
            
    return False, save_path, "Failed all attempts"

def main():
    print("Loading Tokopedia scraped products...")
    from analyze_marketplace_inputs import tokopedia_dict
    
    download_tasks = []
    
    print(f"Total canonical products to organize: {len(tokopedia_dict)}")
    
    for idx, (url, prod) in enumerate(tokopedia_dict.items(), 1):
        name = prod.get('name') or f"AP_Boots_Product_{idx}"
        desc = prod.get('desc', '')
        category = categorize_product(name, desc)
        
        # Product subfolder
        clean_name = sanitize_folder_name(name)
        prod_folder = os.path.join(IMAGES_BASE, category, clean_name)
        os.makedirs(prod_folder, exist_ok=True)
        
        # 1. Main image
        main_img = prod.get('main_img')
        if main_img:
            dest_main = os.path.join(prod_folder, "01_main_1600x1600.jpg")
            download_tasks.append((main_img, dest_main, name, "main"))
            
        # 2. Gallery images from image_17
        gallery_str = prod.get('gallery', '')
        if gallery_str:
            lines = [l.strip() for l in gallery_str.split('\n') if l.strip().startswith('http')]
            for g_i, g_url in enumerate(lines[:5], 2):
                dest_g = os.path.join(prod_folder, f"{g_i:02d}_gallery.jpg")
                download_tasks.append((g_url, dest_g, name, f"gallery_{g_i}"))
                
    print(f"Total image download tasks queued: {len(download_tasks)}")
    
    success_cnt = 0
    fail_cnt = 0
    exist_cnt = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_map = {executor.submit(download_single_image, item[0], item[1]): item for item in download_tasks}
        for future in as_completed(future_map):
            item = future_map[future]
            try:
                ok, path, msg = future.result()
                if ok:
                    if "Already" in msg:
                        exist_cnt += 1
                    else:
                        success_cnt += 1
                else:
                    fail_cnt += 1
            except Exception as e:
                fail_cnt += 1

    print("\n=== DOWNLOAD PROCESS COMPLETE ===")
    print(f"Newly Downloaded: {success_cnt}")
    print(f"Already Existed: {exist_cnt}")
    print(f"Failed: {fail_cnt}")
    print(f"Total Handled: {len(download_tasks)}")
    print(f"Images Root Folder: {IMAGES_BASE}")

if __name__ == '__main__':
    main()
