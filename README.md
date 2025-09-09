# 🎨 Qwen Image for macOS

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-Optimized-green.svg)](https://support.apple.com/en-us/HT211814)
[![Native Apple Silicon](https://img.shields.io/badge/Native-Apple%20Silicon-brightgreen.svg)](#performance)

**Finally, a native AI image tool that actually uses your Apple Silicon properly.**

I got tired of slow cloud APIs and Docker containers that waste your expensive Apple Silicon. This is different - it runs Qwen Image Edit natively on your Mac with full MPS acceleration. No subscriptions, no Docker, no bullshit.

*This is what Mac AI should have been from day one.*

```bash
python qwen.py generate "cyberpunk cityscape at night" --steps 20
# 🤯
```

## 🚀 Installation

Clone, install, and run:

```bash
git clone https://github.com/zsxkib/qwen-image-edit-macos.git
cd qwen-image-edit-macos
pip install -r requirements.txt
python qwen.py test
```

That's it. No Docker, no containers, no virtualization overhead. Pure native Apple Silicon performance. If you have an M1/M2/M3/M4 Mac, this will absolutely fly.

## ⚡ Performance

Running this on M3 Max with 128GB unified memory:

- **Quick mode (10 steps)**: Stylistic results, good for sketches
- **Quality mode (20+ steps)**: Fully formed, professional images  
- **Your GPU**: Automatically uses Apple Silicon MPS
- **Memory**: Works fine on 32GB+, excellent on 64GB+

## 🎯 Examples

```bash
# Quick stylistic results
python qwen.py generate "a neon-lit street in Tokyo at night" --steps 10

# High quality, fully formed images
python qwen.py generate "detailed oil painting of a cat" --steps 20

# Edit photos (drag & drop supported!)
python qwen.py edit IMG_4829.HEIC "make it look like a movie poster" --steps 20

# Custom sizes
python qwen.py generate "ultrawide landscape" --size 1664x928 --steps 20

# Reproducible results
python qwen.py generate "pixel art robot" --seed 42 --steps 20
```

## 🧰 What You Need

- MacBook with Apple Silicon (M1/M2/M3/M4)
- Python 3.8+ (you probably have this)
- 32GB+ RAM (64GB+ recommended for best performance)

*Technically works on Intel Macs but why would you do that to yourself?*

## ✅ What You Get

✅ **Text-to-image generation** - Think it, generate it  
✅ **Image editing** - Upload photo, describe changes, done  
✅ **Native MPS acceleration** - Uses Apple Silicon GPU properly
✅ **Drag & drop** - Just drag files into terminal like a normal person  
✅ **Auto preview** - Images pop open automatically on Mac  
✅ **GPU acceleration** - Uses your expensive Apple Silicon  
✅ **Single file** - It's literally just `qwen.py`  

## 🔧 The Technical Stuff

This uses Alibaba's latest [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) models which are genuinely incredible. Runs natively on Apple Silicon with MPS acceleration for maximum performance.

First run downloads ~20GB of models (they cache locally). After that, it's instant startup.

## 🛠️ If Something Breaks

**GPU not working?**
```bash
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```
Should say `True`. If not, your Mac is too old or something.

**Out of memory?** Close Chrome (you have 47 tabs open). Works best with 32GB+ RAM.

**First run slow?** It's downloading ~20GB of models. Go make coffee. After that it's fast.

**Images look unfinished?** Try `--steps 20` for fully formed results. 10 steps = stylistic, 20+ = professional.

## 🖥️ Commands

Simple CLI interface:

```bash
# Generate images
python qwen.py generate "your idea" [options]

# Edit existing images
python qwen.py edit image.jpg "your edit description"

# Key options:
--steps 10    # Quick stylistic results  
--steps 20    # High quality, fully formed
--steps 30    # Maximum quality
--size 1024x1024  # Custom size
--seed 42     # Reproducible
--output filename.png  # Custom output name

# Quick commands
python qwen.py test    # Test installation
python qwen.py status  # Check system info
```

---

*I built this because I wanted native speed on my Mac without Docker, cloud APIs, or weird configs. Pure Apple Silicon power.*

**Star this if it saved you time** ❤️
