# -*- coding: utf-8 -*-
"""
Upgrade App/photobank_api_bridge.py with fit_to_studio_canvas and intelligent catalog candidate matcher.
Ensures boots fill 85% - 90% of frame, crisp Lanczos upscaling, and pure white studio backgrounds.
"""
import re

with open('App/photobank_api_bridge.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update imports
old_import = "from PIL import Image"
new_import = "from PIL import Image, ImageOps, ImageFilter"
if old_import in code and "ImageOps" not in code:
    code = code.replace(old_import, new_import, 1)

# 2. Add fit_to_studio_canvas and find_catalog_candidate functions
helpers_code = '''
def fit_to_studio_canvas(img: Image.Image, target_size=(1000, 1000), fill_ratio=0.85, bg_color=(255, 255, 255), enhance=True) -> Image.Image:
    """
    Fits and centers an object image onto a pure white square canvas.
    Trims excessive white margins and ensures the boot/shoe occupies fill_ratio (default 85%) of canvas.
    Applies high-quality Lanczos resampling and subtle unsharp masking for sharp details.
    """
    img = img.convert('RGB')
    gray = ImageOps.invert(img.convert('L'))
    # Threshold out noise near pure white (pixel values > 12)
    gray_thresh = gray.point(lambda p: 255 if p > 12 else 0)
    bbox = gray_thresh.getbbox()
    if bbox:
        # Give a 2% margin around detected bbox
        w_box = bbox[2] - bbox[0]
        h_box = bbox[3] - bbox[1]
        pad_x = int(w_box * 0.02)
        pad_y = int(h_box * 0.02)
        crop_box = (
            max(0, bbox[0] - pad_x),
            max(0, bbox[1] - pad_y),
            min(img.width, bbox[2] + pad_x),
            min(img.height, bbox[3] + pad_y)
        )
        cropped = img.crop(crop_box)
    else:
        cropped = img

    max_w = int(target_size[0] * fill_ratio)
    max_h = int(target_size[1] * fill_ratio)

    cw, ch = cropped.size
    ratio = min(max_w / max(1, cw), max_h / max(1, ch))
    new_w = max(1, int(cw * ratio))
    new_h = max(1, int(ch * ratio))

    resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    if enhance and ratio > 1.3:
        resized = resized.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=2))

    canvas = Image.new('RGB', target_size, bg_color)
    paste_x = (target_size[0] - new_w) // 2
    paste_y = (target_size[1] - new_h) // 2
    canvas.paste(resized, (paste_x, paste_y))
    return canvas

def find_catalog_candidate(product_name: str, slot_suffix: str = "03") -> Optional[str]:
    """Finds matching catalog photo for outsole tread (03) or contextual usage (04)."""
    if not os.path.exists(CATALOG_IMAGES_DIR):
        return None
        
    p_lower = product_name.lower().replace("_", " ")
    cat_files = [f for f in os.listdir(CATALOG_IMAGES_DIR) if f.endswith(f"_{slot_suffix}.jpg")]
    
    # 1. Check model numbers (e.g., 2003, 2015, 2005, 9303, 9506, 1001, etc.)
    numbers = re.findall(r'\\b\\d{3,4}\\b', p_lower)
    for num in numbers:
        for f in cat_files:
            if num in f:
                return os.path.join(CATALOG_IMAGES_DIR, f)
                
    # 2. Check special model series names
    special_models = ["ultimate", "xtr", "terra", "orca", "chef", "medic", "moto", "allbike", "safari", "tricolour"]
    for sm in special_models:
        if sm in p_lower:
            for f in cat_files:
                if sm in f.lower():
                    return os.path.join(CATALOG_IMAGES_DIR, f)
                    
    # 3. Default fallback to standard AP 1 catalog angle
    fallback = os.path.join(CATALOG_IMAGES_DIR, f"Black_White_AP 1 Hitam_{slot_suffix}.jpg")
    if os.path.exists(fallback):
        return fallback
        
    return None
'''

if "def fit_to_studio_canvas" not in code:
    code = code.replace("def resolve_category(title: str) -> tuple:", helpers_code + "\ndef resolve_category(title: str) -> tuple:", 1)

# 3. Replace slot generation logic inside generate_sample_4_variations
old_slots_gen = '''    # Slot 1: Hero
    slot1_name = f"{base_name}_slot_1_hero.webp"
    slot1_path = os.path.join(dest_cat_dir, slot1_name)
    if os.path.exists(hero_src):
        shutil.copy2(hero_src, slot1_path)
    else:
        # Create blank studio square
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot1_path, "WEBP", quality=90)
    append_manifest_record(os.path.basename(hero_src), slot1_name, sku, raw_title, target_group, target_category_folder, slot1_path)
    results.append({"slot": 1, "type": "hero_white_bg", "filename": slot1_name, "path": slot1_path})

    # Slot 2: Side Profile
    slot2_name = f"{base_name}_slot_2_side.webp"
    slot2_path = os.path.join(dest_cat_dir, slot2_name)
    if os.path.exists(side_src):
        shutil.copy2(side_src, slot2_path)
    elif os.path.exists(hero_src):
        shutil.copy2(hero_src, slot2_path)
    append_manifest_record(os.path.basename(side_src), slot2_name, sku, raw_title, target_group, target_category_folder, slot2_path)
    results.append({"slot": 2, "type": "side_profile_90deg", "filename": slot2_name, "path": slot2_path})

    # Slot 3: Outsole Tread Detail
    slot3_name = f"{base_name}_slot_3_tread.webp"
    slot3_path = os.path.join(dest_cat_dir, slot3_name)
    # Check catalog for a sole/tread photo fallback
    tread_candidate = os.path.join(CATALOG_IMAGES_DIR, "Black_White_AP 1 Hitam_03.jpg")
    if os.path.exists(tread_candidate):
        with Image.open(tread_candidate) as t_img:
            t_img = t_img.convert("RGB")
            t_canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))
            t_img.thumbnail((900, 900), Image.Resampling.LANCZOS)
            x = (1000 - t_img.width) // 2
            y = (1000 - t_img.height) // 2
            t_canvas.paste(t_img, (x, y))
            t_canvas.save(slot3_path, "WEBP", quality=90)
    else:
        t_canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))
        t_canvas.save(slot3_path, "WEBP", quality=90)
    append_manifest_record("outsole_tread_detail", slot3_name, sku, raw_title, target_group, target_category_folder, slot3_path)
    results.append({"slot": 3, "type": "outsole_tread_cleats", "filename": slot3_name, "path": slot3_path})

    # Slot 4: Contextual In-Use
    slot4_name = f"{base_name}_slot_4_usage.webp"
    slot4_path = os.path.join(dest_cat_dir, slot4_name)
    usage_candidate = os.path.join(CATALOG_IMAGES_DIR, "Black_White_AP 1 Hitam_04.jpg")
    if os.path.exists(usage_candidate):
        with Image.open(usage_candidate) as u_img:
            u_img = u_img.convert("RGB")
            u_canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))
            u_img.thumbnail((900, 900), Image.Resampling.LANCZOS)
            x = (1000 - u_img.width) // 2
            y = (1000 - u_img.height) // 2
            u_canvas.paste(u_img, (x, y))
            u_canvas.save(slot4_path, "WEBP", quality=90)
    else:
        u_canvas = Image.new("RGB", (1000, 1000), (255, 255, 255))
        u_canvas.save(slot4_path, "WEBP", quality=90)
    append_manifest_record("contextual_in_use", slot4_name, sku, raw_title, target_group, target_category_folder, slot4_path)
    results.append({"slot": 4, "type": "contextual_in_use", "filename": slot4_name, "path": slot4_path})'''

new_slots_gen = '''    # Slot 1: Hero White BG (Scaled & Fitted 85% Frame)
    slot1_name = f"{base_name}_slot_1_hero.webp"
    slot1_path = os.path.join(dest_cat_dir, slot1_name)
    if os.path.exists(hero_src):
        with Image.open(hero_src) as h_img:
            fitted_hero = fit_to_studio_canvas(h_img, target_size=(1000, 1000), fill_ratio=0.85)
            fitted_hero.save(slot1_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot1_path, "WEBP", quality=90)
    append_manifest_record(os.path.basename(hero_src), slot1_name, sku, raw_title, target_group, target_category_folder, slot1_path)
    results.append({"slot": 1, "type": "hero_white_bg", "filename": slot1_name, "path": slot1_path})

    # Slot 2: Side Profile 90-degree Lateral (Scaled & Fitted 85% Frame)
    slot2_name = f"{base_name}_slot_2_side.webp"
    slot2_path = os.path.join(dest_cat_dir, slot2_name)
    side_source_file = side_src if os.path.exists(side_src) else (hero_src if os.path.exists(hero_src) else None)
    if side_source_file and os.path.exists(side_source_file):
        with Image.open(side_source_file) as s_img:
            fitted_side = fit_to_studio_canvas(s_img, target_size=(1000, 1000), fill_ratio=0.85)
            fitted_side.save(slot2_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot2_path, "WEBP", quality=90)
    append_manifest_record(os.path.basename(side_src), slot2_name, sku, raw_title, target_group, target_category_folder, slot2_path)
    results.append({"slot": 2, "type": "side_profile_90deg", "filename": slot2_name, "path": slot2_path})

    # Slot 3: Outsole Tread Detail (Model-Specific Match or Crisp Sole Crop, 88% Frame)
    slot3_name = f"{base_name}_slot_3_tread.webp"
    slot3_path = os.path.join(dest_cat_dir, slot3_name)
    tread_candidate = find_catalog_candidate(raw_title, "03") or find_catalog_candidate(folder_name, "03")
    if tread_candidate and os.path.exists(tread_candidate):
        with Image.open(tread_candidate) as t_img:
            fitted_tread = fit_to_studio_canvas(t_img, target_size=(1000, 1000), fill_ratio=0.88, enhance=True)
            fitted_tread.save(slot3_path, "WEBP", quality=92)
    elif os.path.exists(hero_src):
        with Image.open(hero_src) as h_img:
            # Crop lower 38% sole area as high-res sole close-up
            w, h = h_img.size
            sole_crop = h_img.crop((0, int(h * 0.62), w, h))
            fitted_tread = fit_to_studio_canvas(sole_crop, target_size=(1000, 1000), fill_ratio=0.88, enhance=True)
            fitted_tread.save(slot3_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot3_path, "WEBP", quality=90)
    append_manifest_record("outsole_tread_detail", slot3_name, sku, raw_title, target_group, target_category_folder, slot3_path)
    results.append({"slot": 3, "type": "outsole_tread_cleats", "filename": slot3_name, "path": slot3_path})

    # Slot 4: Contextual In-Use (Model-Specific Action Match or Field Framing, 85% Frame)
    slot4_name = f"{base_name}_slot_4_usage.webp"
    slot4_path = os.path.join(dest_cat_dir, slot4_name)
    usage_candidate = find_catalog_candidate(raw_title, "04") or find_catalog_candidate(folder_name, "04")
    if usage_candidate and os.path.exists(usage_candidate):
        with Image.open(usage_candidate) as u_img:
            fitted_usage = fit_to_studio_canvas(u_img, target_size=(1000, 1000), fill_ratio=0.85, enhance=True)
            fitted_usage.save(slot4_path, "WEBP", quality=92)
    elif os.path.exists(hero_src):
        with Image.open(hero_src) as h_img:
            fitted_usage = fit_to_studio_canvas(h_img, target_size=(1000, 1000), fill_ratio=0.85, enhance=True)
            fitted_usage.save(slot4_path, "WEBP", quality=92)
    else:
        img = Image.new("RGB", (1000, 1000), (255, 255, 255))
        img.save(slot4_path, "WEBP", quality=90)
    append_manifest_record("contextual_in_use", slot4_name, sku, raw_title, target_group, target_category_folder, slot4_path)
    results.append({"slot": 4, "type": "contextual_in_use", "filename": slot4_name, "path": slot4_path})'''

if old_slots_gen in code:
    code = code.replace(old_slots_gen, new_slots_gen, 1)
    print("Replaced slot generation logic with fit_to_studio_canvas & model matcher successfully!")
else:
    print("WARNING: Old slots gen block not matched!")

with open('App/photobank_api_bridge.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("photobank_api_bridge.py successfully updated!")

