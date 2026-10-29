# -*- coding: utf-8 -*-
"""
Master Flow MCP to Photobank Pipeline Orchestrator
Coordinates: Product Input -> JSON Schema -> Flow MCP Generation -> Photobank Folder Push
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from .category_mapper import resolve_photobank_category
from .product_json_exporter import load_products_data, build_product_jobs, export_jobs_to_json
from .flow_mcp_client import FlowMcpClient
from .photobank_pusher import PhotobankPusher

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DEFAULT_JSON_OUT = os.path.join(PROJECT_ROOT, "Output", "flow_product_input_jobs.json")

class FlowPhotobankPipeline:
    def __init__(self, flow_url: Optional[str] = None):
        self.client = FlowMcpClient(base_url=flow_url) if flow_url else FlowMcpClient()
        self.pusher = PhotobankPusher()

    def get_system_status(self) -> Dict[str, Any]:
        """Memeriksa status modul, file katalog, dan koneksi Flow MCP."""
        flow_status = self.client.get_status()
        manifest_path = os.path.join(PROJECT_ROOT, "Output", "Photobank_Siap_Upload", "DAFTAR_FOTO_DAN_KATEGORI_PHOTOBANK.csv")
        
        return {
            "pipeline_ready": True,
            "flow_mcp": flow_status,
            "photobank": {
                "folder_exists": os.path.exists(os.path.join(PROJECT_ROOT, "Output", "Photobank_Siap_Upload")),
                "manifest_exists": os.path.exists(manifest_path)
            }
        }

    def generate_jobs_json(self, sku_filter: Optional[str] = None, limit: Optional[int] = None, 
                           output_file: str = DEFAULT_JSON_OUT) -> Dict[str, Any]:
        """
        Membaca catalog input dan mengekspor seluruh prompt/slot ke file JSON.
        """
        df = load_products_data()
        jobs = build_product_jobs(df, sku_filter=sku_filter, limit=limit)
        saved_file = export_jobs_to_json(jobs, output_file)

        return {
            "status": "success",
            "total_jobs": len(jobs),
            "output_file": saved_file,
            "sample_job": jobs[0] if jobs else None
        }

    def execute_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Menjalankan 1 job spesifik: Flow MCP Generation -> Push Photobank.
        """
        prompt = job["prompt"]
        ref_images = job["flow_payload"].get("reference_images", [])

        # Kirim ke Flow MCP
        res = self.client.submit_generate(
            prompt=prompt,
            reference_images=ref_images,
            aspect=job["flow_payload"].get("aspect", "1:1"),
            resolution=job["flow_payload"].get("resolution", "1080p")
        )

        if "error" in res:
            return {"job_id": job["job_id"], "status": "failed", "error": res["error"]}

        # Tunggu hasil render
        task_id = res.get("task_id")
        finish_res = self.client.wait_completion(task_id=task_id, timeout_seconds=90)
        
        output_files = finish_res.get("files", [])
        if not output_files:
            return {"job_id": job["job_id"], "status": "failed", "error": "Tidak ada file output dari Flow MCP"}

        # Push ke folder Photobank
        push_res = self.pusher.push_job_result(job, output_files[0])
        return {
            "job_id": job["job_id"],
            "status": "completed",
            "photobank_result": push_res
        }
