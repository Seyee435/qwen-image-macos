**Native Apple Silicon text-to-image with Lightning LoRA (generation only)**

Fast, local, and simple. Generate high‑quality images on your Mac using Qwen‑Image with MPS acceleration. Lightning LoRA enables very quick 4–8 step generations.

## 🚀 Highlights
- Lightning LoRA acceleration (4–8 steps fast path)
- Native Apple Silicon (M1/M2/M3/M4) via MPS
- Single file CLI: qwen.py
- Auto‑preview on macOS
- Zero Docker, zero cloud (Docker + Cog optional)

## 💾 Install (2 minutes)
```bash
git clone https://github.com/zsxkib/qwen-image-macos.git
cd qwen-image-macos
pip install -r requirements.txt
python qwen.py test
```

## 🎯 Usage
```bash
python qwen.py generate "cyberpunk cityscape at night" --steps 8
python qwen.py generate "oil painting of a cat" --steps 20 --seed 42
```

## 🧠 Requirements
- Apple Silicon Mac (32GB+ RAM recommended)
- Python 3.8+

---
This release focuses on generation only. All editing paths have been removed.