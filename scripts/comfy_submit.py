#!/usr/bin/env python3
"""
Submit a ComfyUI API-compatible workflow JSON and wait for results.

Usage:
  python scripts/comfy_submit.py \
    --workflow path/to/workflow_api.json \
    --server http://127.0.0.1:8188 \
    --timeout 600

Notes:
- The workflow JSON must already be API-compatible (ComfyUI > Queue Prompt > API Format).
- If you want to inject prompt/steps/cfg programmatically, export a workflow
  with the appropriate nodes and edit this script to set those inputs before submit.
- This script does not currently upload images; assume your workflow already
  references an image in ComfyUI's input folder, or set the image via the UI
  and re-export API format before calling this script.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict

import requests


def submit_prompt(server: str, prompt: Dict[str, Any]) -> str:
    resp = requests.post(f"{server}/prompt", json=prompt, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data.get("prompt_id") or data.get("promptid")


essential_view_keys = ("filename", "subfolder", "type")


def fetch_history(server: str, prompt_id: str) -> Dict[str, Any]:
    resp = requests.get(f"{server}/history/{prompt_id}", timeout=30)
    resp.raise_for_status()
    return resp.json()


def download_image(server: str, outdir: Path, info: Dict[str, Any]) -> Path:
    missing = [k for k in essential_view_keys if k not in info]
    if missing:
        raise RuntimeError(f"Image info missing keys: {missing}")
    params = {k: info[k] for k in essential_view_keys}
    r = requests.get(f"{server}/view", params=params, timeout=60)
    r.raise_for_status()
    outdir.mkdir(parents=True, exist_ok=True)
    fname = info["filename"]
    out_path = outdir / fname
    with open(out_path, "wb") as f:
        f.write(r.content)
    return out_path


def main() -> int:
    p = argparse.ArgumentParser(description="Submit ComfyUI workflow and download outputs")
    p.add_argument("--workflow", required=True, help="Path to API-compatible workflow JSON")
    p.add_argument("--server", default="http://127.0.0.1:8188", help="ComfyUI server base URL")
    p.add_argument("--timeout", type=int, default=600, help="Overall timeout in seconds")
    p.add_argument("--interval", type=float, default=2.0, help="Polling interval (seconds)")
    p.add_argument("--outdir", default="comfyui-outputs", help="Directory to save results")
    args = p.parse_args()

    wf_path = Path(args.workflow)
    if not wf_path.exists():
        print(f"Workflow not found: {wf_path}", file=sys.stderr)
        return 2

    with open(wf_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    # Normalize: ComfyUI expects a dict with a top-level 'prompt'
    if "prompt" not in payload:
        # If the file itself is the prompt, wrap it
        payload = {"prompt": payload}

    print("📤 Submitting workflow to ComfyUI...")
    prompt_id = submit_prompt(args.server, payload)
    if not prompt_id:
        print("Failed to obtain prompt id from server response", file=sys.stderr)
        return 3
    print(f"🆔 Prompt ID: {prompt_id}")

    deadline = time.time() + args.timeout
    seen_images: set[str] = set()
    outdir = Path(args.outdir)

    while time.time() < deadline:
        try:
            history = fetch_history(args.server, prompt_id)
        except requests.HTTPError as e:
            # History may not be ready yet
            time.sleep(args.interval)
            continue

        entry = history.get(prompt_id)
        if not entry:
            time.sleep(args.interval)
            continue

        outputs = entry.get("outputs", {})
        any_new = False
        for node_id, node_out in outputs.items():
            images = node_out.get("images") or []
            for img in images:
                key = f"{img.get('subfolder','')}/{img.get('filename','')}"
                if key in seen_images:
                    continue
                path = download_image(args.server, outdir, img)
                print(f"💾 Saved: {path}")
                seen_images.add(key)
                any_new = True

        if entry.get("status", {}).get("completed") is True:
            print("✅ Completed")
            return 0

        if any_new:
            # continue polling for additional outputs
            pass
        time.sleep(args.interval)

    print("⏱️ Timeout waiting for results", file=sys.stderr)
    return 4


if __name__ == "__main__":
    raise SystemExit(main())

