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

mkdir -p "$EXT_DIR" "$NODES_DIR" "$UNET_DIR" "$VAE_DIR" "$TEXT_DIR"

command -v git >/dev/null 2>&1 || { echo "git is required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "curl is required"; exit 1; }

# 1) Clone ComfyUI if missing
if [ ! -d "$COMFY_DIR" ]; then
  echo "Cloning ComfyUI..."
  git clone --depth=1 https://github.com/comfyanonymous/ComfyUI "$COMFY_DIR"
fi

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
# minimal deps; ComfyUI will install its own on first run if needed
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu >/dev/null 2>&1 || true

# 4) Download GGUF assets (use Q4_0 for balance). Adjust if you have more RAM.
GGUF_REPO="https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF/resolve/main"
CITY_REPO="https://huggingface.co/city96/Qwen-Image-gguf/resolve/main"

# Main UNet (choose Q4_0 ~11.9GB)
UNET_FILE="Qwen_Image_Edit-Q4_0.gguf"
if [ ! -f "$UNET_DIR/$UNET_FILE" ]; then
  echo "Downloading UNet GGUF ($UNET_FILE)..."
  curl -L "$GGUF_REPO/$UNET_FILE" -o "$UNET_DIR/$UNET_FILE"
fi

# VAE safetensors from QuantStack repo
VAE_FILE="Qwen_Image-VAE.safetensors"
if [ ! -f "$VAE_DIR/$VAE_FILE" ]; then
  echo "Downloading VAE ($VAE_FILE)..."
  curl -L "$GGUF_REPO/$VAE_FILE" -o "$VAE_DIR/$VAE_FILE"
fi

# Text encoder & mmproj (GGUF)
TE_FILE="Qwen2.5-VL-7B.gguf"
MMPROJ_FILE="Qwen2.5-VL-7B-Instruct-mmproj-BF16.gguf"
if [ ! -f "$TEXT_DIR/$TE_FILE" ]; then
  echo "Downloading text encoder ($TE_FILE)..."
  curl -L "$GGUF_REPO/$TE_FILE" -o "$TEXT_DIR/$TE_FILE"
fi
if [ ! -f "$TEXT_DIR/$MMPROJ_FILE" ]; then
  echo "Downloading mmproj ($MMPROJ_FILE)..."
  curl -L "$GGUF_REPO/$MMPROJ_FILE" -o "$TEXT_DIR/$MMPROJ_FILE"
fi

echo "\nAll models ready under $MODELS_DIR"
echo "Starting ComfyUI (Ctrl+C to stop)..."
cd "$COMFY_DIR"
python main.py --listen 127.0.0.1 --port 8188

