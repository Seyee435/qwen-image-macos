#!/usr/bin/env bash
set -euo pipefail

# Simple setup script for fast Qwen Image Edit on macOS using ComfyUI + GGUF
# - Installs ComfyUI to ./external/ComfyUI
# - Installs ComfyUI-GGUF custom node
# - Downloads Qwen-Image-Edit GGUF + VAE + text encoder mmproj
# - Starts ComfyUI listening on 127.0.0.1:8188
#
# Requirements: git, python3, curl. Homebrew recommended for missing deps.

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
EXT_DIR="$ROOT_DIR/external"
COMFY_DIR="$EXT_DIR/ComfyUI"
NODES_DIR="$COMFY_DIR/custom_nodes"
MODELS_DIR="$COMFY_DIR/models"
UNET_DIR="$MODELS_DIR/unet"
VAE_DIR="$MODELS_DIR/vae"
TEXT_DIR="$MODELS_DIR/text_encoders"

mkdir -p "$EXT_DIR"

command -v git >/dev/null 2>&1 || { echo "git is required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 1; }

# 1) Clone ComfyUI if missing (ensure main.py exists)
if [ ! -f "$COMFY_DIR/main.py" ]; then
  echo "Cloning ComfyUI..."
  rm -rf "$COMFY_DIR"
  git clone --depth=1 https://github.com/comfyanonymous/ComfyUI "$COMFY_DIR"
fi

# Create subdirs now that ComfyUI exists
mkdir -p "$NODES_DIR" "$UNET_DIR" "$VAE_DIR" "$TEXT_DIR"

# 2) Install ComfyUI-GGUF custom node
if [ ! -d "$NODES_DIR/ComfyUI-GGUF" ]; then
  echo "Installing ComfyUI-GGUF custom node..."
  git clone --depth=1 https://github.com/city96/ComfyUI-GGUF "$NODES_DIR/ComfyUI-GGUF"
fi

# 3) Python deps (in a lightweight venv under external/.venv)
if [ ! -d "$EXT_DIR/.venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$EXT_DIR/.venv"
fi
source "$EXT_DIR/.venv/bin/activate"
pip install --upgrade pip
# minimal deps; ComfyUI will install more on first run if needed
pip install requests >/dev/null 2>&1 || true

# 4) Download GGUF assets (use Q4_0 for balance). Adjust if you have more RAM.
GGUF_REPO="https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF/resolve/main"

# Helper to download and sanity-check (>1KB)
download() {
  local url="$1" out="$2"
  curl -L "$url" -o "$out"
  if [ -f "$out" ]; then
    local size
    size=$(stat -f%z "$out" 2>/dev/null || stat -c%s "$out" 2>/dev/null || echo 0)
    if [ "$size" -lt 1024 ]; then
      echo "Download looked wrong (size $size). Removing $out"
      rm -f "$out"
      return 1
    fi
  fi
}

# Main UNet (choose Q4_0 ~11.9GB)
UNET_FILE="Qwen_Image_Edit-Q4_0.gguf"
if [ ! -f "$UNET_DIR/$UNET_FILE" ]; then
  echo "Downloading UNet GGUF ($UNET_FILE)..."
  download "$GGUF_REPO/$UNET_FILE" "$UNET_DIR/$UNET_FILE" || {
    echo "Failed to fetch $UNET_FILE"; exit 1; }
fi

# VAE safetensors
VAE_FILE="Qwen_Image-VAE.safetensors"
if [ ! -f "$VAE_DIR/$VAE_FILE" ]; then
  echo "Downloading VAE ($VAE_FILE)..."
  download "$GGUF_REPO/$VAE_FILE" "$VAE_DIR/$VAE_FILE" || {
    echo "Failed to fetch $VAE_FILE"; exit 1; }
fi

# Text encoder (try common filenames)
TE_CANDIDATES=(
  "Qwen2.5-VL-7B-Instruct-Q4_0.gguf"
  "Qwen2.5-VL-7B-Q4_0.gguf"
  "Qwen2.5-VL-7B-Instruct-Q3_K_M.gguf"
  "Qwen2.5-VL-7B-Instruct-Q5_K_M.gguf"
)
TE_FOUND=0
for f in "${TE_CANDIDATES[@]}"; do
  if [ -f "$TEXT_DIR/$f" ]; then TE_FOUND=1; TE_FILE="$f"; break; fi
  echo "Trying text encoder $f..."
  if download "$GGUF_REPO/$f" "$TEXT_DIR/$f"; then
    TE_FOUND=1; TE_FILE="$f"; break
  fi
done
if [ "$TE_FOUND" -ne 1 ]; then
  echo "Could not download a Qwen2.5-VL-7B text encoder GGUF. Check repo for available filenames."; exit 1
fi

# mmproj
MMPROJ_FILE="Qwen2.5-VL-7B-Instruct-mmproj-BF16.gguf"
if [ ! -f "$TEXT_DIR/$MMPROJ_FILE" ]; then
  echo "Downloading mmproj ($MMPROJ_FILE)..."
  download "$GGUF_REPO/$MMPROJ_FILE" "$TEXT_DIR/$MMPROJ_FILE" || {
    echo "Failed to fetch $MMPROJ_FILE"; exit 1; }
fi

echo "\nAll models ready under $MODELS_DIR"
echo "Starting ComfyUI (Ctrl+C to stop)..."
cd "$COMFY_DIR"
python main.py --listen 127.0.0.1 --port 8188

