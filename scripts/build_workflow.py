#!/usr/bin/env python3
"""
Build a ComfyUI API workflow JSON for Qwen-Image-Edit (GGUF) and optionally
copy an input image into ComfyUI's input folder.

Usage:
  python scripts/build_workflow.py \
    --image example.webp \
    --prompt "make the dog look like a superhero, cape, cinematic lighting" \
    --steps 8 --cfg 1.5 \
    --out workflow_api.json

This script scans external/ComfyUI/models to pick the first matching files:
- models/unet/*.gguf          -> UNet
- models/vae/*.safetensors    -> VAE
- models/text_encoders/*.gguf -> CLIP text encoder (and mmproj if required by loader)

The generated JSON is API-compatible for /prompt.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMFY = ROOT / "external" / "ComfyUI"
MODELS = COMFY / "models"
UNET = MODELS / "unet"
VAE = MODELS / "vae"
TEXT = MODELS / "text_encoders"
INPUTS_DIR = COMFY / "input"


def pick_first(dirpath: Path, suffixes: tuple[str, ...]) -> str | None:
    if not dirpath.exists():
        return None
    files = sorted([p.name for p in dirpath.iterdir() if p.is_file() and p.suffix in suffixes])
    return files[0] if files else None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--image", required=True, help="Path to input image to edit")
    p.add_argument("--prompt", required=True, help="Edit prompt")
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--cfg", type=float, default=1.5)
    p.add_argument("--negative", default=" ")
    p.add_argument("--out", default="workflow_api.json")
    args = p.parse_args()

    # ensure ComfyUI structure exists
    for d in [UNET, VAE, TEXT, INPUTS_DIR]:
        if not d.exists():
            raise SystemExit(f"Expected directory missing: {d}. Run scripts/setup_gguf.sh first.")

    unet_name = pick_first(UNET, (".gguf",))
    vae_name = pick_first(VAE, (".safetensors", ".ckpt"))
    clip_name = pick_first(TEXT, (".gguf",))

    if not unet_name:
        raise SystemExit("No UNet GGUF found under models/unet. Did setup_gguf.sh finish?")
    if not vae_name:
        raise SystemExit("No VAE found under models/vae. Did setup_gguf.sh finish?")
    if not clip_name:
        raise SystemExit("No text-encoder GGUF found under models/text_encoders. Did setup_gguf.sh finish?")

    # Copy image to ComfyUI/input
    src = Path(args.image)
    if not src.exists():
        raise SystemExit(f"Input image not found: {src}")
    INPUTS_DIR.mkdir(parents=True, exist_ok=True)
    target = INPUTS_DIR / src.name
    if src.resolve() != target.resolve():
        target.write_bytes(src.read_bytes())

    # Build graph
    # Node ids as strings; ComfyUI expects a dict of nodes under 'prompt'
    nid = 1
    def n():
        nonlocal nid
        nid += 1
        return str(nid)

    # Nodes
    nodes = {}

    # 1) Load UNet (GGUF)
    unet_node = "1"
    nodes[unet_node] = {
        "class_type": "UnetLoaderGGUF",
        "inputs": {"unet_name": unet_name},
    }

    # 2) Load VAE
    vae_node = n()
    nodes[vae_node] = {"class_type": "VAELoader", "inputs": {"vae_name": vae_name}}

    # 3) CLIP loader (GGUF)
    clip_node = n()
    nodes[clip_node] = {
        "class_type": "CLIPLoaderGGUF",
        "inputs": {"clip_name": clip_name, "type": "stable_diffusion"},
    }

    # 4) Encode positive prompt
    pos_node = n()
    nodes[pos_node] = {
        "class_type": "CLIPTextEncode",
        "inputs": {"clip": [clip_node, 0], "text": args.prompt},
    }
    # 5) Encode negative prompt
    neg_node = n()
    nodes[neg_node] = {
        "class_type": "CLIPTextEncode",
        "inputs": {"clip": [clip_node, 0], "text": args.negative},
    }

    # 6) Load image and VAE Encode to latents
    load_img = n()
    nodes[load_img] = {"class_type": "LoadImage", "inputs": {"image": src.name}}

    vae_encode = n()
    nodes[vae_encode] = {
        "class_type": "VAEEncode",
        "inputs": {"vae": [vae_node, 0], "image": [load_img, 0]},
    }

    # 7) KSampler edit
    ksampler = n()
    nodes[ksampler] = {
        "class_type": "KSampler",
        "inputs": {
            "model": [unet_node, 0],
            "seed": 42,
            "steps": args.steps,
            "cfg": args.cfg,
            "sampler_name": "euler",
            "scheduler": "karras",
            "positive": [pos_node, 0],
            "negative": [neg_node, 0],
            "latent_image": [vae_encode, 0],
        },
    }

    # 8) Decode and Save
    vae_decode = n()
    nodes[vae_decode] = {
        "class_type": "VAEDecode",
        "inputs": {"vae": [vae_node, 0], "samples": [ksampler, 0]},
    }

    save = n()
    nodes[save] = {
        "class_type": "SaveImage",
        "inputs": {"images": [vae_decode, 0], "filename_prefix": "qwen_edit"},
    }

    payload = {"prompt": nodes}
    Path(args.out).write_text(json.dumps(payload), encoding="utf-8")
    print(f"✅ Wrote workflow: {args.out}")
    print(f"   UNet: {unet_name}\n   VAE: {vae_name}\n   CLIP: {clip_name}")
    print(f"   Image copied to: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

