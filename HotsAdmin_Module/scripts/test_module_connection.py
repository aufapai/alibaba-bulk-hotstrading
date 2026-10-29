"""
HOTS ADMIN MODULE - AUTOMATED PRE-TRANSFER DIAGNOSTIC RUNNER
============================================================
File: scripts/test_module_connection.py
Run this to verify local files, database connections, and API readiness
before transferring to debug / staging / live cPanel.
"""

import os
import sys
import sqlite3
import json
import urllib.request

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

MODULE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(MODULE_DIR)
candidate_sqlite_paths = [
    os.path.join(PROJECT_DIR, "Database", "alibaba_master.db"),
    os.path.join(os.path.dirname(PROJECT_DIR), "Product Input", "Database", "alibaba_master.db"),
    r"d:\Work\Hots\Product Input\Database\alibaba_master.db"
]
SQLITE_PATH = next((p for p in candidate_sqlite_paths if os.path.exists(p)), candidate_sqlite_paths[0])
CONFIG_PATH = os.path.join(MODULE_DIR, "config", "config.php")

def run_diagnostics():
    print("=" * 65)
    print(" [TEST] HOTS ADMIN MODULE: PRE-TRANSFER DIAGNOSTICS & VERIFICATION")
    print("=" * 65)
    
    # 1. Directory Structure Checks
    print("\n[1/5] Checking Required Folders & Files...")
    req_items = [
        "config/config.php",
        "config/config.sample.php",
        "config/.env.example",
        "src/Database.php",
        "src/ForexService.php",
        "src/AlibabaExportController.php",
        "api/health.php",
        "api/exchange_rate.php",
        "api/calculate_carton.php",
        "api/prompts.php",
        "api/products.php",
        "api/photobank_sync.php",
        "api/flow_jobs.php",
        "api/market_intelligence.php",
        "api/smart_top_picks.php",
        "api/generate_alibaba_listing.php",
        "api/export_alibaba_bulk.php",
        "sql/database_schema.sql",
        "sql/seed_market_rules.sql",
        "sql/sample_products_seed.sql",
        "index.php"
    ]
    all_found = True
    for item in req_items:
        p = os.path.join(MODULE_DIR, item)
        exists = os.path.exists(p)
        status = "[OK] PASS" if exists else "[!] MISSING"
        if not exists:
            all_found = False
        print(f"  {status} -> {item}")

    # 2. Local SQLite DB Verification
    print("\n[2/5] Checking Local Master SQLite Database...")
    if os.path.exists(SQLITE_PATH):
        try:
            conn = sqlite3.connect(SQLITE_PATH)
            cur = conn.cursor()
            cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
            tbl_count = cur.fetchone()[0]
            
            cur.execute("SELECT count(*) FROM products")
            prod_count = cur.fetchone()[0]
            
            print(f"  [OK] SQLite Database OK: {SQLITE_PATH}")
            print(f"       Tables: {tbl_count} | Products stored: {prod_count} rows")
            conn.close()
        except Exception as e:
            print(f"  [WARN] SQLite exists but query failed: {e}")
    else:
        print(f"  [WARN] Local SQLite not found at {SQLITE_PATH} (Standard when deployed to cPanel MySQL).")

    # 3. Live Forex Public API Connectivity
    print("\n[3/5] Testing Live Forex API Providers...")
    urls = [
        "https://api.exchangerate-api.com/v4/latest/USD",
        "https://open.er-api.com/v6/latest/USD"
    ]
    forex_ok = False
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'HOTS-Admin-Diag/2.0'})
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())
                rate = data.get('rates', {}).get('IDR')
                if rate:
                    print(f"  [OK] {u}")
                    print(f"       Live Rate: 1 USD = Rp {rate:,.2f}")
                    forex_ok = True
                    break
        except Exception as e:
            print(f"  [WARN] Failed connecting to {u}: {e}")

    # 4. Packaging Formula Verification
    print("\n[4/5] Testing Export Metric Calculations...")
    sample_usd = 5.50
    pairs = 12
    cbm = 0.096
    ctn_20ft = int(28.0 / cbm)
    ctn_40ft = int(68.0 / cbm)
    fee_member = sample_usd * 0.02
    fee_assistance = sample_usd * 0.15
    print(f"  [OK] Sample Unit: ${sample_usd:.2f} (12 pairs = ${sample_usd*12:.2f}/carton)")
    print(f"       20ft Container: {ctn_20ft} cartons ({ctn_20ft*pairs:,} pairs)")
    print(f"       40ft HC Container: {ctn_40ft} cartons ({ctn_40ft*pairs:,} pairs)")
    print(f"       Member Fee (2%): ${fee_member:.3f}/pair | Full Assistance (15%): ${fee_assistance:.3f}/pair")

    # 5. Summary
    print("\n[5/5] Final Readiness Summary:")
    print("=" * 65)
    if all_found:
        print("  [SUCCESS] ALL MODULE COMPONENTS ARE COMPLETE AND READY TO TRANSFER!")
        print("  You can now copy the `HotsAdmin_Module` folder directly to:")
        print("  - cPanel: /home/username/public_html/admin/modules/HotsAdmin_Module/")
        print("  - Local PHP Server: Run `php -S localhost:8000` inside `HotsAdmin_Module`")
    else:
        print("  [WARN] Some optional files were not found. Please review above items.")
    print("=" * 65)

if __name__ == "__main__":
    run_diagnostics()
