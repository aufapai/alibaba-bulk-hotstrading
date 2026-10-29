import openpyxl
import sqlite3
import glob
import os
import re

BASE_DIR = r"d:\Work\Hots\Product Input"
DB_PATH = os.path.join(BASE_DIR, "Database", "alibaba_master.db") if os.path.exists(os.path.join(BASE_DIR, "Database", "alibaba_master.db")) else os.path.join(BASE_DIR, "alibaba_master.db")
OUTPUT_PADI = os.path.join(BASE_DIR, "Output_PadiUMKM")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT sku, product_title, image_1, image_2, image_3, image_4, image_5 FROM products")
db_rows = cursor.fetchall()

def get_best_images_and_sku(prod_name):
    p_lower = prod_name.lower()
    
    # 1. Clogs
    if 'clogs' in p_lower:
        if 'white' in p_lower or 'pink' in p_lower:
            target_skus = ['APB-056', 'APB-057', 'APB-058', 'APB-059']
        else:
            target_skus = ['APB-046', 'APB-047', 'APB-048']
    # 2. Allbike
    elif 'allbike 2' in p_lower:
        target_skus = ['APB-070', 'APB-071', 'APB-104']
    elif 'allbike' in p_lower:
        if 'grey' in p_lower or 'abu' in p_lower:
            target_skus = ['APB-069']
        else:
            target_skus = ['APB-105', 'APB-106', 'APB-001']
    # 3. Moto
    elif 'moto' in p_lower:
        if '(i)' in p_lower or 'moto 1' in p_lower:
            target_skus = ['APB-097']
        elif '(ii)' in p_lower or 'moto 2' in p_lower:
            target_skus = ['APB-098']
        elif '(iii)' in p_lower or 'moto 3' in p_lower:
            target_skus = ['APB-099']
        else:
            target_skus = ['APB-097', 'APB-098', 'APB-099']
    # 4. Safety S4 / S5 / Metaguard
    elif 'safety s5' in p_lower or 's5' in p_lower:
        target_skus = ['APB-073', 'APB-096']
    elif 'safety s4' in p_lower or 's4' in p_lower:
        target_skus = ['APB-081', 'APB-095']
    elif 'metaguard' in p_lower:
        target_skus = ['APB-074']
    # 5. Chef & Medic
    elif 'chef' in p_lower:
        target_skus = ['APB-038', 'APB-051']
    elif 'medic' in p_lower:
        target_skus = ['APB-036', 'APB-037', 'APB-063', 'APB-064']
    # 6. Star
    elif 'star' in p_lower:
        target_skus = ['APB-054', 'APB-055']
    # 7. Terra series
    elif 'terra army' in p_lower:
        target_skus = ['APB-052']
    elif 'terra forest' in p_lower:
        target_skus = ['APB-053']
    elif 'terra gp' in p_lower:
        target_skus = ['APB-083']
    elif 'terra eco 2' in p_lower:
        target_skus = ['APB-040']
    elif 'terra eco 3' in p_lower:
        target_skus = ['APB-007', 'APB-008', 'APB-009', 'APB-010']
    elif 'terra eco 5' in p_lower or 'terra 5' in p_lower:
        target_skus = ['APB-076', 'APB-080']
    elif 'terra 3' in p_lower:
        target_skus = ['APB-041', 'APB-072']
    elif 'terra 2' in p_lower:
        target_skus = ['APB-075']
    elif 'terra' in p_lower:
        target_skus = ['APB-007', 'APB-040', 'APB-075']
    # 8. Kids & Safari
    elif 'safari' in p_lower:
        target_skus = ['APB-042', 'APB-043', 'APB-044']
    elif 'jasmine' in p_lower or '2012' in p_lower or 'anak' in p_lower or 'kids' in p_lower or '2001 w' in p_lower or '9307 w' in p_lower or 'grandprix' in p_lower:
        target_skus = ['APB-049', 'APB-050', 'APB-065', 'APB-066', 'APB-079']
    # 9. Pantofel & Sandal (961, 963, 967, 969, 977, 985, 987, 989, 991, 995, 997, 999, 1001, 1003)
    elif any(k in p_lower for k in ['977', 'pantofel', 'vantopel']):
        target_skus = ['APB-039']
    elif '963' in p_lower:
        target_skus = ['APB-082']
    elif any(k in p_lower for k in ['967', '961', '969', 'bola']):
        target_skus = ['APB-086', 'APB-082']
    elif any(k in p_lower for k in ['1001', '1003']):
        target_skus = ['APB-084']
    elif any(k in p_lower for k in ['991', '989', '987', '985']):
        target_skus = ['APB-085', 'APB-087']
    elif any(k in p_lower for k in ['995', '999', '997']):
        target_skus = ['APB-088', 'APB-089', 'APB-090']
    # 10. Orca & Max & XT
    elif 'orca' in p_lower:
        target_skus = ['APB-027']
    elif 'max' in p_lower:
        target_skus = ['APB-033']
    elif 'xt' in p_lower:
        target_skus = ['APB-025']
    # 11. Numbered boots
    elif '2005' in p_lower:
        if 'motif' in p_lower or 'root' in p_lower:
            target_skus = ['APB-004']
        else:
            target_skus = ['APB-005']
    elif '2003' in p_lower:
        target_skus = ['APB-006']
    elif '2006' in p_lower:
        target_skus = ['APB-103']
    elif '2007' in p_lower:
        target_skus = ['APB-102']
    elif '2011' in p_lower:
        target_skus = ['APB-045']
    elif '2015' in p_lower:
        target_skus = ['APB-091', 'APB-092', 'APB-093', 'APB-094']
    elif '2017' in p_lower:
        target_skus = ['APB-002', 'APB-003']
    elif '2018' in p_lower:
        target_skus = ['APB-062', 'APB-100', 'APB-101']
    elif '9303' in p_lower:
        target_skus = ['APB-017']
    elif '9506' in p_lower:
        target_skus = ['APB-028']
    elif '9905' in p_lower:
        target_skus = ['APB-078']
    elif any(k in p_lower for k in ['black', 'white', 'ap 3', 'hitam', 'putih']):
        target_skus = ['APB-077']
    else:
        target_skus = ['APB-001']

    imgs = []
    for r in db_rows:
        if r[0] in target_skus:
            for col_idx in range(2, 7):
                url = r[col_idx]
                if url and url.startswith('http') and url not in imgs:
                    # Shopee: non-main image jangan di-load (hanya slot utama yang boleh jika belum ada foto)
                    if 'susercontent.com' in str(url) and len(imgs) > 0:
                        continue
                    imgs.append(url)
                    
    primary_sku = target_skus[0] if target_skus else 'APB-001'
    return primary_sku, imgs

def update_excel_file(filepath):
    print(f"\nProcessing: {filepath}")
    wb = openpyxl.load_workbook(filepath)
    ws = wb['Isian Template Upload Barang']
    
    updated_count = 0
    for r in range(4, ws.max_row + 1):
        name = ws.cell(r, 3).value
        if not name:
            continue
            
        matched_sku, imgs = get_best_images_and_sku(name)
        
        # Populate SKU if currently empty
        current_sku = ws.cell(r, 33).value
        if not current_sku:
            ws.cell(r, 33, matched_sku)
            
        # Update Foto_Produk_1 to 5 (Columns 16, 17, 18, 19, 20)
        # Shopee: non-main image jangan di-load (hanya img1 / main image yang tetap)
        img1 = imgs[0] if len(imgs) > 0 else None
        img2 = imgs[1] if len(imgs) > 1 and 'susercontent.com' not in str(imgs[1]) else None
        img3 = imgs[2] if len(imgs) > 2 and 'susercontent.com' not in str(imgs[2]) else None
        img4 = imgs[3] if len(imgs) > 3 and 'susercontent.com' not in str(imgs[3]) else None
        img5 = imgs[4] if len(imgs) > 4 and 'susercontent.com' not in str(imgs[4]) else None
        
        ws.cell(r, 16).value = img1
        ws.cell(r, 17).value = img2
        ws.cell(r, 18).value = img3
        ws.cell(r, 19).value = img4
        ws.cell(r, 20).value = img5
        
        updated_count += 1
        print(f"  Row {r:2d} | SKU: {ws.cell(r, 33).value} | Name: {name[:35]:<35} | Img1: {str(img1)[:60]}")
        
    wb.save(filepath)
    print(f"Successfully saved {updated_count} products in {filepath}")

if __name__ == '__main__':
    # Process files in Output_PadiUMKM
    padi_files = sorted(glob.glob(os.path.join(OUTPUT_PADI, "PadiUMKM_Bulk_Upload_Batch_*.xlsx")))
    for pf in padi_files:
        update_excel_file(pf)

    # Process files in Output (AP Boots version)
    out_files = sorted(glob.glob(os.path.join(OUTPUT_DIR, "PadiUMKM_Bulk_Upload_AP_Boots_Batch_*.xlsx")))
    for of in out_files:
        update_excel_file(of)

    print("\n=== ALL PA DI UMKM EXCEL BATCHES UPDATED WITH TOKOPEDIA CDN IMAGES SUCCESSFULLY ===")
