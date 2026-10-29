import sqlite3
import csv
import os

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db")
OUTPUT_CSV = os.path.join(BASE_DIR, "products.csv")

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT sku, product_title, category_group, color, image_1 FROM products WHERE image_1 LIKE 'http%' LIMIT 10")
    rows = cur.fetchall()
    conn.close()

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'id', 'product_name', 'category', 'color', 'source_image_url',
            'slot_1_hero_prompt', 'slot_2_side_prompt', 'slot_3_detail_prompt', 'slot_4_usage_prompt'
        ])
        
        for r in rows:
            sku, title, cat, color, img = r
            clean_name = title.split(' - ')[0].strip() if ' - ' in title else title.strip()
            clean_color = color.split(';')[0].strip() if color else 'Black'
            
            # Contextual usage scene based on Alibaba guide section 6.5
            cat_l = (cat or '').lower()
            if 'safety' in cat_l:
                scene = 'an industrial warehouse floor with concrete and yellow safety markings'
            elif 'biker' in cat_l or 'allbike' in clean_name.lower():
                scene = 'a wet city street after rain with asphalt reflections'
            elif 'chef' in cat_l:
                scene = 'a clean commercial kitchen with a wet tiled floor'
            elif 'terra' in cat_l or 'orca' in cat_l:
                scene = 'a muddy agricultural plantation ground in outdoor daylight'
            elif 'kids' in cat_l:
                scene = 'a rainy sidewalk with fallen autumn leaves'
            else:
                scene = 'a wet paved street after monsoon rain with water puddle reflections'
                
            p1 = (
                f"Using the attached reference photos, create a professional e-commerce product photo "
                f"of the exact same {clean_color} {clean_name}. Keep the product exactly identical to the "
                f"reference: same shape, proportions, sole pattern, stitching, logo placement and color. "
                f"Single product, 3/4 front angle, standing upright, centered, filling about 85% of the frame. "
                f"Pure white seamless background (RGB 255,255,255), soft studio lighting, subtle natural contact shadow only. "
                f"Sharp focus, true-to-life color. Square 1:1, high resolution. No text, no watermark, no props."
            )
            p2 = (
                f"Using the attached reference photos, create a product photo of the exact same "
                f"{clean_color} {clean_name} from a straight side profile view. Keep the product exactly "
                f"identical to the reference. Pure white background (RGB 255,255,255), soft even studio lighting, "
                f"product centered and filling about 85% of the frame, subtle natural shadow. "
                f"Square 1:1, sharp focus, no text, no watermark, no props."
            )
            p3 = (
                f"Using the attached reference photos, create a product photo of the exact same "
                f"{clean_color} {clean_name} showing the bottom tread pattern and anti-slip outsole cleat structure. "
                f"Keep the product exactly identical to the reference. Pure white background (RGB 255,255,255), "
                f"soft studio lighting, centered, about 85% of the frame. Square 1:1, sharp focus, no text, no props."
            )
            p4 = (
                f"Using the attached reference photos, create a realistic photo of the exact same "
                f"{clean_color} {clean_name} being worn in {scene}. Frame from the knees down so the boots are the "
                f"clear focal point; no visible face. Keep the product exactly identical to the reference: "
                f"same shape, sole, stitching, logo placement and color. Natural lighting, realistic environment, "
                f"shallow depth of field on the background. Square 1:1, high resolution. No text, no watermark."
            )
            
            writer.writerow([sku, clean_name, cat, clean_color, img, p1, p2, p3, p4])

    print(f"Successfully generated {OUTPUT_CSV} with {len(rows)} products mapped to 4 photo slots!")

if __name__ == '__main__':
    main()
