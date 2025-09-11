# 🎨 Qwen Image for macOS (Generation Only)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Optimized-green.svg)](https://support.apple.com/en-us/HT211814)

Native, fast, Apple Silicon–accelerated text-to-image generation with Qwen Image. No Docker, no cloud, no complexity.

## 🚀 Installation

Clone, install, and run:

```bash
# use your repo URL (rename coming soon)
# git clone https://github.com/<you>/<repo>.git
cd qwen-image-edit
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

## 🔧 Technical Notes

- Uses Alibaba's [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) via Diffusers
- Scheduler defaults to DPM-Solver++ Multistep when available
- Attention slicing and VAE tiling enabled to reduce memory spikes on MPS

## 🛠️ Troubleshooting

```bash
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```
Should print `True`. If not, update macOS / Xcode Command Line Tools and PyTorch.

If images look unfinished, increase `--steps` to 20 or 30.

---

Built for a clean, native Mac experience. Pure Apple Silicon power.
