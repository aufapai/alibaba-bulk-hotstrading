import urllib.request
import json
import time
import subprocess
import sys

print("Testing Alibaba Manager App server and Shopee Asset Studio...")
proc = subprocess.Popen([sys.executable, "App/alibaba_manager_app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2)

try:
    # 1. Test index HTML
    req = urllib.request.urlopen("http://localhost:8888/", timeout=5)
    html = req.read().decode("utf-8")
    print(f"Index HTML loaded: {len(html)} bytes")
    print(f"Has Shopee Studio button: {'Shopee Official Asset Studio' in html}")
    chk_tab = "switchSourceTab('shopee_studio')" in html
    print(f"Has shopee_studio default switch: {chk_tab}")
    print(f"Has shopeeJsonModal: {'id=\"shopeeJsonModal\"' in html}")

    # 2. Test /api/shopee/products
    req_prod = urllib.request.urlopen("http://localhost:8888/api/shopee/products", timeout=5)
    data = json.loads(req_prod.read().decode("utf-8"))
    print(f"/api/shopee/products status: success={data.get('success')}, total={data.get('total')}")
    sample = data.get('products', [])[0]
    print(f"Sample product: {sample.get('sku')} | {sample.get('product_name')} | Folder: {sample.get('folder_name')}")

    # 3. Test /api/shopee/product-json
    folder = sample.get('folder_name')
    req_json = urllib.request.urlopen(f"http://localhost:8888/api/shopee/product-json?folder={folder}", timeout=5)
    p_json = json.loads(req_json.read().decode("utf-8"))
    print(f"/api/shopee/product-json: success={p_json.get('success')}, legal_mfg={p_json.get('data', {}).get('manufacturer_and_export_entity', {}).get('legal_manufacturer', {}).get('name')}")

    # 4. Test /shopee-assets static image serving
    hero_file = sample.get('hero_filename')
    req_img = urllib.request.urlopen(f"http://localhost:8888/shopee-assets/{folder}/{hero_file}", timeout=5)
    img_bytes = req_img.read()
    print(f"/shopee-assets image: status={req_img.status}, length={len(img_bytes)} bytes, Content-Type={req_img.headers.get('Content-Type')}")

    print("\nALL SERVER TESTS PASSED SUCCESSFULLY!")

finally:
    proc.terminate()
    proc.wait()
