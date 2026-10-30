# -*- coding: utf-8 -*-
"""
Patch App/alibaba_manager_app.py with custom and batch image generation endpoints.
"""
with open('App/alibaba_manager_app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update imports
old_imp = """from photobank_api_bridge import (
    get_photobank_summary, generate_sample_4_variations,
    upload_sku_slots_to_photobank_admin, PHOTOBANK_DIR,
    FLOW_PROJECT_ID, FLOW_PROJECT_URL, FLOW_ACCOUNT_EMAIL
)"""

new_imp = """from photobank_api_bridge import (
    get_photobank_summary, generate_sample_4_variations,
    generate_product_variations_custom, batch_generate_products_custom,
    upload_sku_slots_to_photobank_admin, PHOTOBANK_DIR,
    FLOW_PROJECT_ID, FLOW_PROJECT_URL, FLOW_ACCOUNT_EMAIL
)"""

if old_imp in code:
    code = code.replace(old_imp, new_imp, 1)

# 2. Add endpoints to do_POST
post_target = """        elif path == "/api/photobank/upload-admin":
            try:
                sku = data.get("sku", "SHP-001")
                folder = data.get("folder", "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC")
                simulate = data.get("simulate", True)
                api_endpoint = data.get("api_endpoint", "https://admin.hotstrading.com/api/photobank/upload")
                cookie = data.get("session_cookie", None)
                res = upload_sku_slots_to_photobank_admin(
                    sku=sku,
                    folder_name=folder,
                    api_endpoint=api_endpoint,
                    session_cookie=cookie,
                    simulate=simulate
                )
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return"""

new_post_endpoints = """        elif path == "/api/photobank/upload-admin":
            try:
                sku = data.get("sku", "SHP-001")
                folder = data.get("folder", "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC")
                simulate = data.get("simulate", True)
                api_endpoint = data.get("api_endpoint", "https://admin.hotstrading.com/api/photobank/upload")
                cookie = data.get("session_cookie", None)
                res = upload_sku_slots_to_photobank_admin(
                    sku=sku,
                    folder_name=folder,
                    api_endpoint=api_endpoint,
                    session_cookie=cookie,
                    simulate=simulate
                )
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/custom-generate":
            try:
                sku = data.get("sku", "SHP-001")
                folder = data.get("folder", "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC")
                slots = data.get("slots", [1, 2, 3, 4])
                target_size = int(data.get("target_size", 1000))
                fill_ratio = float(data.get("fill_ratio", 0.85))
                save_to_shopee = bool(data.get("save_to_shopee", True))
                save_to_flow = bool(data.get("save_to_flow", True))
                save_to_photobank = bool(data.get("save_to_photobank", True))
                
                res = generate_product_variations_custom(
                    sku=sku,
                    folder_name=folder,
                    slots=slots,
                    target_size=target_size,
                    fill_ratio=fill_ratio,
                    save_to_shopee=save_to_shopee,
                    save_to_flow=save_to_flow,
                    save_to_photobank=save_to_photobank
                )
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return

        elif path == "/api/photobank/batch-generate":
            try:
                items = data.get("items", [])
                slots = data.get("slots", [1, 2, 3, 4])
                target_size = int(data.get("target_size", 1000))
                fill_ratio = float(data.get("fill_ratio", 0.85))
                save_to_shopee = bool(data.get("save_to_shopee", True))
                save_to_flow = bool(data.get("save_to_flow", True))
                save_to_photobank = bool(data.get("save_to_photobank", True))

                res = batch_generate_products_custom(
                    items=items,
                    slots=slots,
                    target_size=target_size,
                    fill_ratio=fill_ratio,
                    save_to_shopee=save_to_shopee,
                    save_to_flow=save_to_flow,
                    save_to_photobank=save_to_photobank
                )
                self.send_json(res)
            except Exception as e:
                self.send_json({"success": False, "error": str(e)}, status=500)
            return"""

if post_target in code:
    code = code.replace(post_target, new_post_endpoints, 1)
    print("Patched do_POST endpoints successfully!")
else:
    print("WARNING: post_target not matched!")

with open('App/alibaba_manager_app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("alibaba_manager_app.py successfully updated!")

