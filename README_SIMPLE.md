# 🎨 Qwen Image for macOS

**AI image generation and editing on Apple Silicon - Just Works™**

Generate stunning images from text or edit existing photos with AI. Optimized for Mac with Apple Silicon GPU acceleration.

```bash
# Generate an image
python qwen.py generate "a cyberpunk cityscape at night"

# Edit an image (drag & drop supported!)
python qwen.py edit photo.jpg "make it look like an oil painting"
```

## Quick Start

```bash
# Clone and test
git clone https://github.com/zsxkib/qwen-image-edit-macos.git
cd qwen-image-edit-macos
pip install torch torchvision diffusers transformers pillow click
python qwen.py test

# Generate your first image
python qwen.py generate "a beautiful mountain landscape" --steps 4
```

**That's it.** No conda, no complex setup, no configuration files.

## Performance on Apple Silicon

- **Lightning mode** (`--steps 4`): ~30 seconds for 1024x1024 images
- **Quality mode** (`--steps 50`): ~4 minutes for best results  
- **Apple Silicon GPU**: Automatically detected and used
- **Memory efficient**: Works on 16GB+ Macs

## Examples

```bash
# Fast generation
python qwen.py generate "sunset over ocean" --steps 4

# High quality 
python qwen.py generate "detailed portrait" --steps 50

# Custom size
python qwen.py generate "wide landscape" --size 1664x928

# Edit images (drag files right into the terminal!)
python qwen.py edit vacation_photo.jpg "add dramatic clouds"
python qwen.py edit portrait.png "oil painting style" --steps 4
```

## Requirements

- **macOS** with Apple Silicon (M1/M2/M3/M4)
- **Python 3.8+** 
- **16GB+ RAM** recommended

Works on Intel Macs too, just slower.

## What You Get

- ✅ Text-to-image generation with Qwen-Image
- ✅ Image editing with Qwen-Image-Edit  
- ✅ Lightning LoRA for 4x speed boost
- ✅ Drag-and-drop image support
- ✅ Auto-preview on macOS
- ✅ Apple Silicon MPS acceleration
- ✅ Simple single-file CLI
- ✅ No complex configuration

## Behind the Scenes

Uses the state-of-the-art [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) and [Qwen-Image-Edit](https://huggingface.co/Qwen/Qwen-Image-Edit) models from Alibaba with [Lightning LoRA](https://huggingface.co/lightx2v/Qwen-Image-Lightning) acceleration.

Models automatically download on first use (~20GB total) and cache locally.

## Troubleshooting

**Not using Apple Silicon GPU?**
```bash
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```

**Out of memory?** Use `--steps 4` for lighter usage or close other apps.

**Slow generation?** First run downloads models (~20GB). Subsequent runs are much faster.

---

**Just want to generate images with AI on your Mac? This is it.**
