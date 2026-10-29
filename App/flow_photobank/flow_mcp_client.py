# -*- coding: utf-8 -*-
"""
Flow MCP HTTP & Stdio Client
Interfaces directly with GTAI-1/flow-mcp local server (http://127.0.0.1:8787).
"""

import os
import time
import json
import requests
from typing import Dict, Any, Optional, List

DEFAULT_PORT = int(os.environ.get("FLOW_MCP_PORT", 8787))
BASE_URL = f"http://127.0.0.1:{DEFAULT_PORT}"

def get_flow_token() -> Optional[str]:
    """Mengambil token autentikasi Flow MCP dari ~/.flow-mcp/token."""
    home = os.environ.get("FLOW_MCP_HOME") or os.path.expanduser("~")
    token_path = os.path.join(home, ".flow-mcp", "token")
    if os.path.exists(token_path):
        try:
            with open(token_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass
    return None

class FlowMcpClient:
    def __init__(self, base_url: str = BASE_URL, token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.token = token or get_flow_token()

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.token:
            headers["x-flow-token"] = self.token
        return headers

    def ping(self) -> bool:
        """Mengecek apakah server Flow MCP aktif di localhost."""
        try:
            r = requests.get(f"{self.base_url}/api/health", timeout=3)
            return r.status_code == 200 and r.json().get("name") == "flow-mcp"
        except Exception:
            return False

    def get_status(self) -> Dict[str, Any]:
        """
        Mengambil status sesi Google Flow (login, credits, active project).
        """
        if not self.ping():
            return {
                "online": False,
                "error": f"Flow MCP server tidak aktif di {self.base_url}. Jalankan 'npm run studio' di folder flow-mcp."
            }

        try:
            r = requests.post(
                f"{self.base_url}/api/flow_status",
                headers=self._headers(),
                json={},
                timeout=10
            )
            if r.status_code == 200:
                res = r.json()
                res["online"] = True
                return res
            return {"online": True, "error": f"HTTP {r.status_code}: {r.text}"}
        except Exception as e:
            return {"online": False, "error": str(e)}

    def upload_reference_image(self, file_path: str) -> Optional[str]:
        """Mengunggah gambar referensi lokal ke Flow MCP upload folder."""
        if not os.path.exists(file_path):
            return None
        try:
            filename = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                content = f.read()

            headers = self._headers()
            headers["Content-Type"] = "application/octet-stream"
            r = requests.post(
                f"{self.base_url}/api/upload?name={filename}",
                headers=headers,
                data=content,
                timeout=30
            )
            if r.status_code == 200:
                return r.json().get("path")
        except Exception as e:
            print(f"[!] Gagal upload reference image ke Flow MCP: {e}")
        return None

    def submit_generate(self, prompt: str, reference_images: Optional[List[str]] = None, 
                        aspect: str = "1:1", resolution: str = "1080p") -> Dict[str, Any]:
        """
        Mengirim perintah generate gambar ke Flow MCP.
        """
        payload = {
            "prompt": prompt,
            "type": "image",
            "aspect": aspect,
            "resolution": resolution,
            "reference_images": reference_images or [],
            "max_credits": 0  # 0 credits for image stills
        }

        try:
            r = requests.post(
                f"{self.base_url}/api/flow_generate",
                headers=self._headers(),
                json=payload,
                timeout=45
            )
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def submit_agent_images(self, scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Mengirim batch gambar ke Flow Agent mode (hingga 50 gambar sekaligus paralel, 0 credits!).
        """
        try:
            r = requests.post(
                f"{self.base_url}/api/flow_agent_images",
                headers=self._headers(),
                json={"scenes": scenes},
                timeout=60
            )
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def wait_completion(self, task_id: Optional[str] = None, timeout_seconds: int = 120) -> Dict[str, Any]:
        """Menunggu penyelesaian render gambar."""
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            try:
                r = requests.post(
                    f"{self.base_url}/api/flow_wait",
                    headers=self._headers(),
                    json={"task_id": task_id} if task_id else {},
                    timeout=45
                )
                if r.status_code == 200:
                    data = r.json()
                    if data.get("finished", False):
                        return data
                time.sleep(5)
            except Exception as e:
                time.sleep(5)
        return {"finished": False, "error": "Timeout menunggu hasil Flow MCP"}
