"""
HOTS UNIFIED DATABASE ADAPTER
=============================
File: scripts/hots_db_adapter.py
Bridge layer connecting:
- Local SQLite (`Database/alibaba_master.db`)
- Live cPanel MySQL/MariaDB (`hotj4796_hotstrading`)

Provides a unified interface for querying products, syncing catalog,
and inserting Alibaba export listings.
"""

import os
import sys
import sqlite3
import json
from datetime import datetime

# Base Directory Resolution
MODULE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(MODULE_DIR)
SQLITE_PATH = os.path.join(PROJECT_DIR, "Database", "alibaba_master.db")

class HotsDatabaseAdapter:
    def __init__(self, mode="sqlite", mysql_config=None):
        self.mode = mode
        self.mysql_config = mysql_config or {
            "host": os.environ.get("DB_HOST", "localhost"),
            "user": os.environ.get("DB_USERNAME", "hotj4796_user"),
            "password": os.environ.get("DB_PASSWORD", ""),
            "database": os.environ.get("DB_DATABASE", "hotj4796_hotstrading"),
            "port": int(os.environ.get("DB_PORT", 3306))
        }

    def get_connection(self):
        if self.mode == "mysql":
            try:
                import pymysql
                conn = pymysql.connect(
                    host=self.mysql_config["host"],
                    user=self.mysql_config["user"],
                    password=self.mysql_config["password"],
                    database=self.mysql_config["database"],
                    port=self.mysql_config["port"],
                    cursorclass=pymysql.cursors.DictCursor
                )
                return conn
            except Exception as e:
                print(f"[WARN] MySQL connection failed ({e}), falling back to SQLite local.")
                self.mode = "sqlite"

        # SQLite Connection (Local Default)
        if not os.path.exists(SQLITE_PATH):
            raise FileNotFoundError(f"SQLite database not found at: {SQLITE_PATH}")

        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def get_all_products(self, limit=100, source_filter=None):
        conn = self.get_connection()
        cur = conn.cursor()
        
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        if source_filter and source_filter != 'all':
            query += " AND source = ?"
            params.append(source_filter)
        
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        
        result = [dict(r) for r in rows]
        conn.close()
        return result

    def get_product_by_sku(self, sku):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE sku = ? OR model_number = ? LIMIT 1", (sku, sku))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def upsert_alibaba_export_listing(self, data):
        """
        Saves or updates an Accio-optimized listing into alibaba_export_listings or products.
        """
        conn = self.get_connection()
        cur = conn.cursor()
        
        sku = data.get("sku")
        title = data.get("alibaba_product_title")
        usd = data.get("fob_price_usd", 5.50)
        idr = data.get("base_price_idr", 99000)
        
        cur.execute("""
        UPDATE products SET
            product_title = ?,
            price_usd = ?,
            price_idr = ?,
            keywords = ?,
            industry_angle = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE sku = ?
        """, (
            title, usd, idr,
            ", ".join(data.get("primary_keywords", [])),
            data.get("target_industry_angle", "Heavy Industrial & Construction"),
            sku
        ))
        
        conn.commit()
        conn.close()
        return True

if __name__ == "__main__":
    print("=" * 60)
    print("HOTS DATABASE ADAPTER - TEST & DIAGNOSTICS")
    print("=" * 60)
    adapter = HotsDatabaseAdapter()
    try:
        prods = adapter.get_all_products(limit=5)
        print(f"[OK] Successfully queried products. Retrieved {len(prods)} rows.")
        for p in prods:
            sku = p.get('sku') or p.get('product_code') or 'N/A'
            name = p.get('product_title') or p.get('name') or 'N/A'
            print(f" - [{sku}] {name[:40]}")
    except Exception as err:
        print(f"[FAIL] Error querying database: {err}")
