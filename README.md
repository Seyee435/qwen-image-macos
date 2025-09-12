# 🎨 Qwen Image for macOS (Generation Only)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Optimized-green.svg)](https://support.apple.com/en-us/HT211814)

Native, fast, Apple Silicon–accelerated text-to-image generation with Qwen Image. Lightning LoRA acceleration for quick 4–8 step generations. No Docker, no cloud, no complexity.

## 🚀 Installation

Clone, install, and run:

```bash
git clone https://github.com/zsxkib/qwen-image-macos.git
cd qwen-image-macos
pip install -r requirements.txt
python qwen.py test
```

First run downloads ~20GB of model weights (cached locally). After that, startup is quick.

## ⚡ Performance

Tested on an M3 Max (128GB):
- 10 steps: quick stylistic results
- 20+ steps: fully formed, high quality images
- Uses Apple Silicon MPS automatically

## 🎯 Usage

```bash
# Generate from a prompt
python qwen.py generate "cyberpunk cityscape at night" --steps 20

# Custom sizes and settings
python qwen.py generate "mountain landscape" --size 1024x768 --steps 20 --seed 42

# Quick commands
python qwen.py test    # Verify setup
python qwen.py status  # Show system info
```

## 🧰 Requirements

- Apple Silicon Mac (M1/M2/M3/M4)
- Python 3.8+
- 32GB+ RAM recommended (64GB+ ideal)

## ✅ Features

- Native MPS acceleration on macOS
- Simple, single-file CLI (`qwen.py`)
- Auto-opens generated image in Preview on macOS
- Reproducible seeds and custom sizes

## 🐳 Docker + Cog (optional)

On macOS, you can run this in a container with Replicate Cog. Note: Docker on macOS does not expose MPS, so it runs on CPU (slower). On Linux with NVIDIA, Cog will use CUDA automatically.

Prereqs:
- Docker Desktop (macOS users: increase memory to 64GB+ in Settings → Resources)
- Cog CLI: brew install replicate/cog/cog

Build the image (first time installs Python deps):

```bash
cog build
```

Quick generate (CPU on macOS):

```bash
# Enable faster HF downloads and increase setup timeout for first-run model pull
export HF_HUB_ENABLE_HF_TRANSFER=1
cog predict --setup-timeout 10800 \
  -i prompt="A cinematic photo of a corgi in sunglasses" \
  -i ultra_fast=true \
  -i width=512 -i height=512
```

Tips:
- First predict downloads the Qwen-Image model (~57GB) inside the container. This may take a while on first run.
- Speed up downloads by enabling HF transfer: `export HF_HUB_ENABLE_HF_TRANSFER=1` (already shown above).
- For local Apple Silicon speed, prefer the native CLI with MPS; Cog is best for reproducible containers and Linux/NVIDIA GPUs.
- If you need to pre-cache inside Docker, run the above once with a long timeout; subsequent runs will be faster.

## 🔧 Technical Notes

- Uses Alibaba's [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) via Diffusers
- Attention slicing and VAE tiling enabled to reduce memory spikes on MPS

## 🛠️ Troubleshooting

```bash
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```
Should print `True`. If not, update macOS / Xcode Command Line Tools and PyTorch.

If images look unfinished, increase `--steps` to 20 or 30.

---

Built for a clean, native Mac experience. Pure Apple Silicon power.
