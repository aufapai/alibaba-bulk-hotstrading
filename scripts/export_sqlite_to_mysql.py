# -*- coding: utf-8 -*-
"""
Export Database/alibaba_master.db to MySQL / MariaDB SQL Dump for cPanel phpMyAdmin.
"""
import os
import sqlite3

def export_to_mysql():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, "Database", "alibaba_master.db")
    out_sql = os.path.join(project_root, "HotsAdmin_Module", "sql", "full_alibaba_master_dump.sql")

    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    def sanitize_val(val):
        if val is None:
            return "NULL"
        if isinstance(val, (int, float)):
            return str(val)
        s = str(val).replace("\\", "\\\\").replace("'", "\\'").replace("\r", "\\r").replace("\n", "\\n")
        return f"'{s}'"

    tables = ["products", "alibaba_matrix_800", "alibaba_keywords", "marketplace_raw"]

    with open(out_sql, "w", encoding="utf-8") as f:
        f.write("-- ==========================================================\n")
        f.write("-- HOTS TRADING - COMPLETE MASTER DATABASE DUMP FOR CPANEL\n")
        f.write("-- Source: Database/alibaba_master.db (Extracted from Input/)\n")
        f.write("-- Generated for: cPanel MariaDB / MySQL Import (phpMyAdmin)\n")
        f.write("-- ==========================================================\n\n")
        f.write("SET FOREIGN_KEY_CHECKS=0;\n")
        f.write("SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\n")
        f.write("SET NAMES utf8mb4;\n\n")

        for table in tables:
            cur.execute(f"PRAGMA table_info({table})")
            cols = cur.fetchall()
            if not cols:
                continue

            f.write(f"-- --------------------------------------------------------\n")
            f.write(f"-- Table structure for `{table}`\n")
            f.write(f"-- --------------------------------------------------------\n")
            f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
            f.write(f"CREATE TABLE `{table}` (\n")

            col_defs = []
            primary_key = None
            for col in cols:
                cname = col[1]
                ctype = col[2].upper()
                is_pk = col[5]

                mysql_type = "VARCHAR(255)"
                if "INT" in ctype:
                    mysql_type = "INT(11)"
                elif "REAL" in ctype or "FLOAT" in ctype or "DOUBLE" in ctype:
                    mysql_type = "DECIMAL(12,2)"
                elif "TEXT" in ctype:
                    if any(k in cname.lower() for k in ["description", "raw", "html", "specs", "keywords", "images"]):
                        mysql_type = "LONGTEXT"
                    elif "url" in cname.lower() or "title" in cname.lower():
                        mysql_type = "VARCHAR(500)"
                    else:
                        mysql_type = "TEXT"
                elif "TIME" in ctype:
                    mysql_type = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"

                auto_inc = ""
                if is_pk and "INT" in ctype:
                    auto_inc = " AUTO_INCREMENT"
                    primary_key = cname
                elif is_pk:
                    primary_key = cname

                null_def = "DEFAULT NULL" if not is_pk else "NOT NULL"
                col_defs.append(f"  `{cname}` {mysql_type} {null_def}{auto_inc}")

            if primary_key:
                col_defs.append(f"  PRIMARY KEY (`{primary_key}`)")

            f.write(",\n".join(col_defs))
            f.write("\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n\n")

            # Dump rows
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()
            if rows:
                col_names = [f"`{c[1]}`" for c in cols]
                f.write(f"-- Dumping data for table `{table}` ({len(rows)} records)\n")

                chunk_size = 50
                for i in range(0, len(rows), chunk_size):
                    chunk = rows[i:i + chunk_size]
                    f.write(f"INSERT INTO `{table}` ({', '.join(col_names)}) VALUES\n")
                    val_lines = []
                    for row in chunk:
                        vals = [sanitize_val(row[idx]) for idx in range(len(cols))]
                        val_lines.append(f"({', '.join(vals)})")
                    f.write(",\n".join(val_lines) + ";\n\n")

        f.write("SET FOREIGN_KEY_CHECKS=1;\n")

    size_mb = os.path.getsize(out_sql) / (1024 * 1024)
    print(f"Dump successfully created at {out_sql} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    export_to_mysql()
