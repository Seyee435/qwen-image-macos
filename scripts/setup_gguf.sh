#!/usr/bin/env bash
set -euo pipefail

FETCH_ONLY=0
if [[ "${1:-}" == "--fetch-only" ]]; then
  FETCH_ONLY=1
fi

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

# 3) Python deps (in a dedicated venv under external/.venv)
if [ ! -d "$EXT_DIR/.venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$EXT_DIR/.venv"
fi
source "$EXT_DIR/.venv/bin/activate"
python -m pip install --upgrade pip setuptools wheel

# Install PyTorch (known-good for macOS Sequoia with ComfyUI-GGUF)
# NOTE: If you already have a working torch in this venv, this will be a no-op
python -m pip install "torch==2.4.1" "torchvision==0.19.1" "torchaudio==2.4.1" --upgrade --quiet || true

# Install ComfyUI requirements (includes psutil and friends)
if [ -f "$COMFY_DIR/requirements.txt" ]; then
  python -m pip install -r "$COMFY_DIR/requirements.txt" --upgrade --quiet || true
fi

# Install ComfyUI-GGUF requirements (gguf>=0.13.0, sentencepiece, protobuf)
if [ -f "$NODES_DIR/ComfyUI-GGUF/requirements.txt" ]; then
  python -m pip install -r "$NODES_DIR/ComfyUI-GGUF/requirements.txt" --upgrade --quiet || true
fi

# Extra safety: ensure these are present
python -m pip install requests huggingface_hub einops pillow tqdm pyyaml psutil --upgrade --quiet || true

# 4) Download GGUF assets using huggingface_hub (reliable paths)
python scripts/fetch_gguf.py --unet-dir "$UNET_DIR" --vae-dir "$VAE_DIR" --text-dir "$TEXT_DIR"

echo "\nAll models ready under $MODELS_DIR"
if [[ "$FETCH_ONLY" == "1" ]]; then
  echo "Fetch-only mode. Not starting ComfyUI."
  exit 0
fi

echo "Starting ComfyUI (Ctrl+C to stop)..."
cd "$COMFY_DIR"
python main.py --listen 127.0.0.1 --port 8188
