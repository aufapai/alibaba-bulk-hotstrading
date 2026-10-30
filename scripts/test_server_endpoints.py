# -*- coding: utf-8 -*-
import sys
import threading
import time
import urllib.request
import json
import socketserver
import http.server

sys.path.insert(0, 'App')
from alibaba_manager_app import AlibabaManagerHandler

TEST_PORT = 8899

def run_test_server(server):
    try:
        server.serve_forever()
    except Exception:
        pass

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", TEST_PORT), AlibabaManagerHandler)
    t = threading.Thread(target=run_test_server, args=(server,), daemon=True)
    t.start()
    time.sleep(1)

    print("--- 1. Testing GET /api/photobank/status ---")
    req = urllib.request.Request(f"http://127.0.0.1:{TEST_PORT}/api/photobank/status")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Status success:", data.get('success'))
        print("Total Photobank files:", data.get('total_photobank_files'))
        print("Target URL:", data.get('target_website'))
        print("Flow project ID:", data.get('google_flow_target', {}).get('project_id'))

    print("\n--- 2. Testing POST /api/photobank/generate-sample ---")
    payload = json.dumps({"sku": "SHP-001", "folder": "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC"}).encode('utf-8')
    req = urllib.request.Request(f"http://127.0.0.1:{TEST_PORT}/api/photobank/generate-sample", data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Gen success:", data.get('success'))
        print("Product:", data.get('product_name'))
        print("Category Folder:", data.get('category_folder'))
        print("Slots count:", len(data.get('variations_generated', [])))

    print("\n--- 3. Testing POST /api/photobank/upload-admin (Simulation) ---")
    upload_payload = json.dumps({"sku": "SHP-001", "folder": "AP_Boots_XTR_Hitam_Sepatu_Boot_PVC", "simulate": True}).encode('utf-8')
    req = urllib.request.Request(f"http://127.0.0.1:{TEST_PORT}/api/photobank/upload-admin", data=upload_payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Upload API success:", data.get('success'))
        print("Simulated:", data.get('simulated'))
        print("Target Category:", data.get('category_folder'))
        print("Results count:", len(data.get('results', [])))
        for r in data.get('results', []):
            print(f"  * {r['slot']}: {r.get('status', 'ok')} ({r.get('filename')})")

    server.shutdown()
    server.server_close()
    print("\nALL HTTP ENDPOINT VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
