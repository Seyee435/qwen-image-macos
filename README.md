# 🎨 Qwen Image for macOS

**Run Qwen Image Edit natively on Apple Silicon. No bullshit.**

I got tired of waiting for good AI image tools on Mac, so I built this. It's Qwen Image Edit running locally on your MacBook with full GPU acceleration. Simple CLI, stupid fast, just works.

```bash
python qwen.py generate "cyberpunk cityscape at night" --steps 4
# 30 seconds later: mind-blown
```

## Installation

Literally just this:

```bash
git clone https://github.com/zsxkib/qwen-image-edit-macos.git
cd qwen-image-edit-macos
pip install -r requirements.txt
python qwen.py test
```

That's it. No conda environments, no Docker, no 50-step setup guides. If you have a Mac with Apple Silicon, this will work.

## How Fast?

I'm running this on an M3 Pro and it's genuinely stupid fast:

- **Lightning mode**: ~30 seconds for 1024x1024 images
- **Quality mode**: ~4 minutes when you want it perfect
- **Your GPU**: Automatically uses Apple Silicon MPS
- **Memory**: Works fine on 16GB, better on 32GB+

## Examples

```bash
# Generate something cool
python qwen.py generate "a neon-lit street in Tokyo at night" --steps 4

# Edit photos (literally drag the file into terminal)
python qwen.py edit IMG_4829.HEIC "make it look like a movie poster"

# Want higher quality? More steps
python qwen.py generate "detailed oil painting of a cat" --steps 50

# Custom sizes
python qwen.py generate "ultrawide landscape" --size 1664x928
```

## What You Need

- MacBook with Apple Silicon (M1/M2/M3/M4)
- Python 3.8+ (you probably have this)
- 16GB+ RAM (32GB+ is better but not required)

*Technically works on Intel Macs but why would you do that to yourself?*

## What You Get

✅ **Text-to-image generation** - Think it, generate it  
✅ **Image editing** - Upload photo, describe changes, done  
✅ **Lightning LoRA** - 4x faster than normal (this is the magic)  
✅ **Drag & drop** - Just drag files into terminal like a normal person  
✅ **Auto preview** - Images pop open automatically on Mac  
✅ **GPU acceleration** - Uses your expensive Apple Silicon  
✅ **Single file** - It's literally just `qwen.py`  

## The Technical Stuff

This uses Alibaba's latest [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) models which are genuinely incredible. I'm using the Lightning LoRA to make it fast as hell.

First run downloads ~20GB of models (they cache locally). After that, it's instant startup.

## If Something Breaks

**GPU not working?**
```bash
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```
Should say `True`. If not, your Mac is too old or something.

**Out of memory?** Close Chrome (you have 47 tabs open). Or use `--steps 4`.

**First run slow?** It's downloading 20GB of models. Go make coffee. After that it's fast.

**Images look bad?** Try `--steps 50` instead of `--steps 4`. Quality vs speed tradeoff.

## Commands

```bash
python qwen.py generate "<prompt>" [--steps 4] [--size 1024x1024] [--seed 42]
python qwen.py edit <image> "<changes>" [--steps 4] 
python qwen.py status  # Check if everything's working
python qwen.py test    # Quick test
```

---

*I built this because I wanted to generate images on my Mac without dealing with cloud APIs, slow web interfaces, or running random Docker containers. It just works.*

**Star this if it saved you time** ❤️
