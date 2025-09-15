# 🎨 Qwen Image for macOS

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Optimized-green.svg)](https://support.apple.com/en-us/HT211814)

**Fast AI image generation for Apple Silicon.** Native CLI with MPS acceleration **or** containerized with Cog. Lightning LoRA for 4–8 step generation.

## 🚀 Quick Start

**Choose your approach:**

### Option A: Native CLI (⚡ **2 minutes** - Recommended for Apple Silicon)

```bash
git clone https://github.com/zsxkib/qwen-image-macos.git
cd qwen-image-macos
pip install -r requirements.txt
python qwen.py generate "cyberpunk cityscape" --ultra-fast
```

### Option B: Containerized with Cog (🐳 **Reproducible** - Works everywhere)

```bash
git clone https://github.com/zsxkib/qwen-image-macos.git
cd qwen-image-macos
python3 precache.py  # downloads model once (~10 min)
cog predict -i prompt="cyberpunk cityscape" --output city.png
```

> **Note**: Cog runs ~30x slower on Apple Silicon (60+ min) due to x86_64 emulation. Use native CLI for speed, cog for reproducibility/deployment.

## ⚡ Performance Comparison

| Method | Time | Platform | GPU | Best For |
|--------|------|----------|-----|----------|
| **Native CLI** | **2 min** | Apple Silicon | ✅ MPS | Speed, development |
| **Cog (macOS)** | 60+ min | x86_64 emulation | ❌ CPU only | Reproducibility |
| **Cog (Linux)** | ~2-5 min | Native x86_64 | ✅ CUDA | Deployment, cloud |

## 🎯 Native CLI Usage

```bash
# Ultra-fast (4 steps with Lightning LoRA)
python qwen.py generate "cyberpunk cityscape" --ultra-fast

# Fast mode (8 steps)
python qwen.py generate "mountain landscape" --fast

# Custom settings
python qwen.py generate "robot on mars" --steps 20 --seed 42

# Test your setup
python qwen.py test
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

## 🐳 Cog Usage (Containerized)

**Prerequisites:**
- Docker Desktop (macOS: increase memory to 64GB+ in Settings → Resources)
- Cog CLI: `brew install replicate/cog/cog`

**Quick workflow:**

```bash
# 1. Pre-download model (recommended, ~10 min)
python3 precache.py

# 2. Generate images
cog predict -i prompt="robot on mars" --output robot.png
cog predict -i prompt="cyberpunk city" -i steps=10 --output city.png
```

**When to use cog:**
- ✅ **Linux/NVIDIA**: Fast with CUDA acceleration
- ✅ **Reproducible deployments**: Exact same environment everywhere
- ✅ **Replicate cloud**: Deploy to replicate.com
- ❌ **Apple Silicon**: Use native CLI instead (30x faster)

## 🔧 Technical Details

- **Model**: [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) (57GB)
- **Acceleration**: Lightning LoRA for 4-8 step generation
- **Memory**: Attention slicing + VAE tiling for efficiency
- **Cache**: Models stored in `model_cache/` (~63GB)

## 🛠️ Troubleshooting

**Check Apple Silicon GPU:**
```bash
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```

**Common fixes:**
- MPS not available → Update macOS/PyTorch
- Images look unfinished → Increase `--steps` to 20-30
- Cog OOM errors → Increase Docker memory to 64GB+

## 🎆 Example Output

Native CLI generates high-quality images in ~2 minutes:

![Example](example.webp)

---

**Built for Apple Silicon. Optimized for speed. Ready for deployment.**
