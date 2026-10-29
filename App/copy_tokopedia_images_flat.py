import os
import re
import shutil

source_base = r"d:\Work\Hots\Product Input\Images_Tokopedia"
target_dir = r"d:\Work\Hots\Product Input\Images_Produk_Katalog"

os.makedirs(target_dir, exist_ok=True)

cat_map = {
    "01_AP_Terra_Series": "Terra",
    "02_AP_Orca_Series": "Orca",
    "03_AP_Chef_Medical_Series": "Chef_Medical",
    "04_AP_Boots_Green_Series": "Green_Series",
    "05_AP_Boots_Black_White_Series": "Black_White",
    "06_AP_Safety_Boots": "Safety",
    "07_AP_Kasual_Sneakers": "Sneakers",
    "08_AP_Biker_Casual_Shoes": "Biker",
    "09_AP_Kids_Boots": "Kids",
    "10_AP_Sandals_Clogs": "Clogs",
    "11_AP_Specialty_Sports": "Specialty_Sports",
    "12_AP_General_Boots": "General"
}

def clean_product_name(folder_name):
    # Remove control characters
    s = re.sub(r'[\r\n\t]+', ' ', folder_name).strip()
    
    # Split by hyphen if it has marketplace description
    parts = s.split(' - ')
    main_part = parts[0].strip()
    
    # Normalize "AP Boots" or "Ap Boots"
    main_part = re.sub(r'^AP\s*Boots\s+AP\s+', 'AP ', main_part, flags=re.IGNORECASE)
    main_part = re.sub(r'^Ap\s*Boots\s+', 'AP ', main_part, flags=re.IGNORECASE)
    main_part = re.sub(r'^AP\s*Boots\s*', 'AP ', main_part, flags=re.IGNORECASE)
    
    # Remove illegal windows characters
    main_part = re.sub(r'[\\/*?:"<>|]', '', main_part)
    # Remove trailing commas or dots
    main_part = main_part.strip(' ,.-')
    main_part = re.sub(r'\s+', ' ', main_part).strip()
    
    return main_part

copied_files = []
skipped_files = []

for series in sorted(os.listdir(source_base)):
    sp = os.path.join(source_base, series)
    if not os.path.isdir(sp):
        continue
    
    cat_prefix = cat_map.get(series, series)
    
    subs = [d for d in os.listdir(sp) if os.path.isdir(os.path.join(sp, d))]
    for sub in sorted(subs):
        sub_path = os.path.join(sp, sub)
        cname = clean_product_name(sub)
        
        # Get all image files sorted
        files = [f for f in os.listdir(sub_path) if os.path.isfile(os.path.join(sub_path, f))]
        # Sort files so 01_main comes first, then 02_gallery, etc.
        files.sort()
        
        for idx, fname in enumerate(files, 1):
            src_file = os.path.join(sub_path, fname)
            ext = os.path.splitext(fname)[1].lower()
            if not ext:
                ext = ".jpg"
            elif ext not in [".jpg", ".jpeg", ".png", ".webp"]:
                ext = ".jpg"
                
            new_filename = f"{cat_prefix}_{cname}_{idx:02d}{ext}"
            
            # Destination path
            dest_file = os.path.join(target_dir, new_filename)
            
            # Handle rare collision
            counter = idx
            while os.path.exists(dest_file):
                counter += 1
                new_filename = f"{cat_prefix}_{cname}_{counter:02d}{ext}"
                dest_file = os.path.join(target_dir, new_filename)
            
            shutil.copy2(src_file, dest_file)
            copied_files.append((src_file, dest_file, new_filename))

print(f"SUCCESS: Copied {len(copied_files)} files into '{target_dir}'.")
print("\nSample 10 copied files:")
for item in copied_files[:10]:
    print(" ", item[2])
