#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from huggingface_hub import hf_hub_download

REPO_EDIT = "QuantStack/Qwen-Image-Edit-GGUF"
REPO_TE   = "unsloth/Qwen2.5-VL-7B-Instruct-GGUF"

TE_CANDIDATES = [
    "Qwen2.5-VL-7B-Instruct-Q4_0.gguf",
    "Qwen2.5-VL-7B-Instruct-Q3_K_M.gguf",
    "Qwen2.5-VL-7B-Instruct-Q2_K.gguf",
]


def ensure(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unet-dir", required=True)
    ap.add_argument("--vae-dir", required=True)
    ap.add_argument("--text-dir", required=True)
    args = ap.parse_args()

    unet_dir = Path(args.unet_dir)
    vae_dir = Path(args.vae_dir)
    text_dir = Path(args.text_dir)

    # 1) UNET (Q4_0)
    unet_name = "Qwen_Image_Edit-Q4_0.gguf"
    unet_out = unet_dir / unet_name
    if not unet_out.exists():
        ensure(unet_out)
        p = hf_hub_download(REPO_EDIT, filename=unet_name, local_dir=unet_dir)
        print(f"UNET -> {p}")

    # 2) VAE
    vae_name = "VAE/Qwen_Image-VAE.safetensors"
    vae_out = vae_dir / "Qwen_Image-VAE.safetensors"
    if not vae_out.exists():
        ensure(vae_out)
        p = hf_hub_download(REPO_EDIT, filename=vae_name, local_dir=vae_dir)
        print(f"VAE  -> {p}")

    # 3) mmproj
    mmproj_name = "mmproj/Qwen2.5-VL-7B-Instruct-mmproj-BF16.gguf"
    mmproj_out = text_dir / "Qwen2.5-VL-7B-Instruct-mmproj-BF16.gguf"
    if not mmproj_out.exists():
        ensure(mmproj_out)
        p = hf_hub_download(REPO_EDIT, filename=mmproj_name, local_dir=text_dir)
        print(f"MMPROJ -> {p}")

    # 4) text encoder (pick first available candidate)
    found = None
    for cand in TE_CANDIDATES:
        out = text_dir / cand
        if out.exists():
            found = out
            break
        try:
            ensure(out)
            p = hf_hub_download(REPO_TE, filename=cand, local_dir=text_dir)
            print(f"TE -> {p}")
            found = out
            break
        except Exception as e:
            continue
    if not found:
        raise SystemExit("Could not download any Qwen2.5-VL-7B GGUF text encoder (tried: " + ", ".join(TE_CANDIDATES) + ")")

if __name__ == "__main__":
    main()

