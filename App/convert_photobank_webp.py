import os
import re
import csv
from PIL import Image

BASE_DIR = r"d:\Work\Hots\Product Input"
SRC_DIR = os.path.join(BASE_DIR, "Image Flow")
OUT_DIR = os.path.join(BASE_DIR, "Output", "Photobank_WebP")
MAPPING_CSV = os.path.join(BASE_DIR, "Output", "photobank_webp_mapping.csv")

os.makedirs(OUT_DIR, exist_ok=True)

def generate_clean_name(f):
    # Check if it was an img_*.webp filename
    m_img = re.match(r'(img_[a-f0-9\.]+)\.webp', f, re.I)
    if m_img:
        return f"{m_img.group(1)}.webp"
        
    # Remove timestamp suffix like _20261008180527 or _20261009122945
    base = re.sub(r'_\d{14}(_\d+)?(\(\d+\))?(\.jpg|\.png)?$', '', f, flags=re.I)
    base = re.sub(r'\.(jpg|png|jpeg|webp)$', '', base, flags=re.I)
    base = re.sub(r'\.(jpg|png|jpeg|webp)$', '', base, flags=re.I)
    
    # Clean symbols
    base = re.sub(r'[^a-zA-Z0-9_\-]', '_', base)
    base = re.sub(r'_+', '_', base).strip('_').lower()
    return base

def main():
    print("=" * 65)
    print("      CONVERTING IMAGE FLOW TO WEBP FOR HOTSTRADING PHOTOBANK")
    print("=" * 65)
    print(f"Source Directory : {SRC_DIR}")
    print(f"Output Directory : {OUT_DIR}")

    files = [
        f for f in os.listdir(SRC_DIR)
        if not f.endswith('.zip') and not f.endswith('.mp4') and not f.startswith('Imported_')
    ]
    print(f"Total candidate source files: {len(files)}")

    stems = {}
    for f in files:
        stem = generate_clean_name(f)
        if stem not in stems:
            stems[stem] = []
        stems[stem].append(f)

    final_names = {}
    for stem, f_list in sorted(stems.items()):
        if stem.startswith('img_'):
            for f in f_list:
                final_names[f] = f"{stem}.webp"
        elif len(f_list) == 1:
            final_names[f_list[0]] = f"{stem}.webp"
        else:
            for idx, f in enumerate(sorted(f_list), 1):
                final_names[f] = f"{stem}_{idx:02d}.webp"

    records = []
    success_count = 0
    fail_count = 0

    for orig_file, webp_name in sorted(final_names.items()):
        src_path = os.path.join(SRC_DIR, orig_file)
        dest_path = os.path.join(OUT_DIR, webp_name)
        public_url = f"https://hotstrading.com/backend/uploads/{webp_name}"

        try:
            with Image.open(src_path) as img:
                # Convert palette or RGBA if saving to RGB WebP, or keep RGBA
                if img.mode in ('RGBA', 'LA'):
                    # Save with alpha channel
                    img.save(dest_path, 'WEBP', quality=90, method=6)
                elif img.mode == 'P':
                    img = img.convert('RGBA')
                    img.save(dest_path, 'WEBP', quality=90, method=6)
                else:
                    img = img.convert('RGB')
                    img.save(dest_path, 'WEBP', quality=90, method=6)

            records.append({
                'original_file': orig_file,
                'webp_filename': webp_name,
                'photobank_url': public_url,
                'file_size_kb': round(os.path.getsize(dest_path) / 1024, 1)
            })
            success_count += 1
        except Exception as e:
            print(f"  [!] Failed to convert {orig_file}: {e}")
            fail_count += 1

    # Save mapping CSV
    with open(MAPPING_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['original_file', 'webp_filename', 'photobank_url', 'file_size_kb'])
        writer.writeheader()
        writer.writerows(records)

    print("\n" + "=" * 65)
    print(f"Conversion Complete!")
    print(f"Successfully converted : {success_count} files")
    if fail_count > 0:
        print(f"Failed conversions     : {fail_count} files")
    print(f"WebP output directory  : {OUT_DIR}")
    print(f"Mapping index CSV      : {MAPPING_CSV}")
    print("=" * 65)

if __name__ == '__main__':
    main()
