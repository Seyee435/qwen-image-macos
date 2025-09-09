# 🎨 Qwen Image Edit for macOS

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
[![Apple Silicon](https://img.shields.io/badge/Apple%20Silicon-optimized-green.svg)](https://support.apple.com/en-us/HT211814)
[![Drag & Drop](https://img.shields.io/badge/Drag%20%26%20Drop-supported-brightgreen.svg)]()

Professional AI image generation and editing optimized for macOS. **Simply drag & drop images directly into your terminal** for effortless editing with world-class results.

> ✨ **New in v1.1**: Enhanced drag-and-drop support, automatic Quick Look previews, and intelligent prompt suggestions make this the most Mac-friendly AI image editor available.

![Demo](assets/demo.gif)

## ✨ Why This Package?

The **most Mac-friendly AI image editor** with features designed specifically for macOS users:

- 🖼️ **Drag & Drop Magic** - Simply drag images from Finder into your terminal
- 🔍 **Quick Look Integration** - Automatic previews of edited images on macOS
- ⚡ **Lightning Fast** - Apple Silicon MPS optimization + Lightning LoRA acceleration
- 💡 **Smart Suggestions** - AI-powered prompt ideas and creative inspiration
- 🎮 **Zero Friction** - One-command setup, intelligent defaults, just works
- 🌍 **World-Class Results** - Professional-grade image editing with Qwen's state-of-the-art model

## 🎥 Quick Demo

```bash
# Generate an image with Lightning speed
qwen-image generate -p "A serene mountain lake at sunset" --lightning

# Edit with drag & drop (just drag your image into the terminal!)
qwen-image edit -i [DRAG IMAGE HERE] -p "Add snow to the mountains"

# Get creative prompt ideas
qwen-image suggestions

# Check your system optimization 
qwen-image status
```

> 🖼️ **Pro tip**: Drag any image file from Finder directly into the terminal instead of typing paths!

## 📋 Requirements

- **macOS** (any recent version)
- **Apple Silicon** Mac (M1, M2, M3, M4) *recommended*
- **Python 3.10+** (get it with `brew install python@3.11`)
- **16GB+ RAM** (32GB+ recommended for best performance)

*Works on Intel Macs too, but Apple Silicon is much faster.*

## 🚀 Installation

### Option 1: One-Command Setup (Recommended)

```bash
git clone https://github.com/zsxkib/qwen-image-edit-macos.git
cd qwen-image-edit-macos
python install.py
```

That's it! The setup script will:
- ✅ Check your system compatibility
- ✅ Install all dependencies
- ✅ Configure optimal settings for your Mac
- ✅ Test the installation
- ✅ Show you how to get started

### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/zsxkib/qwen-image-edit-macos.git
cd qwen-image-edit-macos

# Create conda environment (recommended)
conda env create -f environment.yml
conda activate qwen-image-edit

# Or install with pip
pip install -e .
```

## 🎯 Quick Start

### 1. Check Your System
```bash
qwen-image status
```
This shows your Mac's specs and recommended settings.

### 2. Generate Your First Image
```bash
qwen-image generate -p "A cozy coffee shop with warm lighting"
```

### 3. Try Image Editing
```bash
# First generate an image to edit
qwen-image generate -p "A landscape photo" -o landscape.png

# Then edit it
qwen-image edit -i landscape.png -p "Make it winter with snow"
```

### 4. Run Examples
```bash
qwen-image examples
```
Generates 3 example images to test everything works.

## 🖼️ Drag & Drop Magic

The most intuitive way to edit images on Mac - **no typing paths required!**

### How it works:
1. **Open your terminal** and start typing: `qwen-image edit -i `
2. **Drag any image from Finder** directly into the terminal window
3. **Add your editing prompt**: `-p "make it look like a painting"`
4. **Press Enter** - your edited image will automatically preview in Quick Look!

### Supported formats:
✅ **Common formats**: JPG, PNG, BMP, TIFF  
✅ **Mac-native formats**: HEIC (iPhone photos), WebP  
✅ **Special characters**: Handles spaces, quotes, and special characters automatically

### Example workflow:
```bash
# 1. Start typing the command
qwen-image edit -i 

# 2. Drag your "My Vacation Photo.HEIC" from Finder into terminal
# The terminal shows: qwen-image edit -i "/Users/you/Photos/My Vacation Photo.HEIC"

# 3. Complete the command
qwen-image edit -i "/Users/you/Photos/My Vacation Photo.HEIC" -p "add sunset lighting" --lightning

# 4. Press Enter and watch the magic happen! ✨
# Your edited image automatically opens in Quick Look
```

> 📝 **Interactive demo**: Run `python examples/drag_drop_demo.py` for a guided tour of all features!

## 🚀 Features

- **Image Generation**: Create high-quality images from text prompts
- **Image Editing**: Modify existing images with text instructions
- **Two Implementation Options**:
  - **MPS Native**: Optimized for Apple Silicon using PyTorch MPS
  - **GGUF Quantized**: Smaller memory footprint and potentially faster inference using GGUF models in ComfyUI
- **Lightning LoRA Support**: Ultra-fast generation with 4-step and 8-step modes
- **Easy Scripts**: Convenient bash scripts for common operations

## 📋 System Requirements

- **Hardware**: Apple Silicon Mac (M1/M2/M3/M4)
- **Memory**: 
  - 16GB+ recommended for GGUF quantized models
  - 32GB+ recommended for MPS native approach
  - 128GB (like your system) is excellent for any approach
- **Storage**: 
  - ~60GB for full models (MPS native)
  - ~20GB for GGUF quantized models
- **OS**: macOS with conda/miniconda installed

## 🔍 Implementation Options

| Feature | MPS Native | GGUF Quantized |
|---------|------------|-----------------|
| **Setup Complexity** | Simple CLI tool | Requires ComfyUI setup |
| **Memory Usage** | Higher (~32GB+) | Lower (~16GB+) |
| **Disk Space** | ~60GB | ~20GB |
| **Performance** | Good (51s gen / 3min edit) | Potentially faster |
| **Quality** | Full precision | Slight quality tradeoff |
| **UI** | Command line | ComfyUI visual interface |
| **Best For** | Maximum quality | Lower memory systems |

## ✅ Current Setup Status (MPS Native)

- ✅ **Environment**: `qwen-image` conda environment created
- ✅ **Dependencies**: `qwen-image-mps` tool installed with all dependencies
- ✅ **PyTorch**: Version 2.8.0 with MPS support
- ✅ **Models**: Qwen-Image (~57GB) and Lightning LoRA models downloaded
- ✅ **MPS Acceleration**: Confirmed working

## 📁 Project Structure

```
qwen-image-edit/
├── README.md              # This file
├── models/                 # Local model storage (if needed)
├── outputs/               
│   └── output/            # Generated and edited images
├── scripts/               # Utility scripts
│   ├── generate.sh        # Image generation script
│   └── edit.sh           # Image editing script
└── test_images/          # Sample images for testing
```

## 🎯 Quick Start

### Activate Environment
```bash
conda activate qwen-image
```

### Generate an Image
```bash
# Using the CLI directly
qwen-image-mps generate -p "A serene mountain lake at sunset, ultra detailed" --ultra-fast

# Using the convenience script
cd qwen-image-edit/scripts
./generate.sh "A magical forest with glowing mushrooms" 20 ultra-fast
```

### Edit an Image
```bash
# Using the CLI directly
qwen-image-mps edit -i "path/to/image.png" -p "Add snow to the mountains" --ultra-fast

# Using the convenience script  
cd qwen-image-edit/scripts
./edit.sh "../outputs/output/image-20250908-120613.png" "Add winter elements"
```

## 🎯 GGUF Setup Option (Alternative)

Alternatively, you can use the GGUF quantized models with ComfyUI for potentially better performance with lower memory usage:

### 1. Install ComfyUI
```bash
# Clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI

# Create a conda environment
conda create -n comfyui python=3.10 -y
conda activate comfyui

# Install requirements
pip install -r requirements.txt
```

### 2. Install ComfyUI-GGUF Extension
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
cd ComfyUI-GGUF
pip install -r requirements.txt
```

### 3. Download GGUF Models

Download these files to the following locations:

| Component | File Source | Destination Path |
|-----------|-------------|-----------------|
| Main Model | [QuantStack/Qwen-Image-Edit-GGUF](https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF) | `ComfyUI/models/unet/` |
| Text Encoder | [unsloth/Qwen2.5-VL-7B-Instruct-GGUF](https://huggingface.co/unsloth/Qwen2.5-VL-7B-Instruct-GGUF) | `ComfyUI/models/text_encoders/` |
| Text Encoder (mmproj) | [QuantStack/Qwen-Image-Edit-GGUF](https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF) | `ComfyUI/models/text_encoders/` |
| VAE | [QuantStack/Qwen-Image-Edit-GGUF](https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF) | `ComfyUI/models/vae/` |

You can choose the appropriate quantization level based on your system's memory:
- For M3 Max with 128GB: `Q8_0` for maximum quality (21.8GB)
- For 32GB systems: `Q4_K_M` or `Q5_K_S` (12-14GB)
- For 16GB systems: `Q2_K` or `Q3_K_S` (7-9GB)

### 4. Launch ComfyUI
```bash
cd ComfyUI
python main.py
```

Open your browser at http://127.0.0.1:8188 and import a workflow for Qwen Image Edit.

## ⚡ Performance Modes

1. **Ultra-Fast Mode** (`--ultra-fast`): 4 steps, ~50 seconds
   - Best for quick iterations and testing
   - Uses Lightning LoRA v1.0

2. **Fast Mode** (`--fast`): 8 steps, ~100 seconds
   - Good balance of speed and quality
   - Uses Lightning LoRA v1.1

3. **Normal Mode** (default): 50 steps, ~400+ seconds
   - Highest quality output
   - No LoRA acceleration

## 🔄 Which Approach Should I Use?

| Choose MPS Native If You: | Choose GGUF Quantized If You: |
|---------------------------|---------------------------------|
| Want a simple CLI tool | Prefer a visual workflow UI |
| Have 32GB+ memory | Have limited memory (16GB) |
| Prioritize maximum quality | Can accept slight quality reduction |
| Need a quick setup | Want faster inference times |
| Don't want to learn ComfyUI | Already use ComfyUI for other models |

Both approaches work well on Apple Silicon, but the GGUF approach may offer better memory efficiency, while the MPS approach offers a simpler setup.

## 🧪 Test Results

### Image Generation Test ✅
- **Prompt**: "A serene mountain lake at sunset with pine trees reflected in the water, ultra detailed, cinematic lighting"
- **Mode**: Ultra-fast (4 steps)
- **Time**: ~51 seconds
- **Device**: MPS (Apple Silicon)
- **Output**: `image-20250908-120613.png` (1664x928)

### Image Editing Test ✅
- **Input**: Generated lake image
- **Edit**: "Add snow-capped mountains in the background and change the sky to winter sunset colors"
- **Mode**: Ultra-fast (4 steps) 
- **Time**: ~3 minutes
- **Device**: MPS (Apple Silicon)
- **Output**: `edited-20250908-125053.png`

## 🛠️ CLI Commands

### Image Generation
```bash
# Basic generation
qwen-image-mps generate -p "Your prompt here"

# With specific parameters
qwen-image-mps generate -p "Cyberpunk cityscape" -s 30 --fast --seed 42

# Multiple images
qwen-image-mps generate -p "Forest scene" --num-images 3 --ultra-fast

# Custom aspect ratio
qwen-image-mps generate -p "Portrait" --aspect 1:1 --fast
```

### Image Editing
```bash
# Basic editing
qwen-image-mps edit -i input.jpg -p "Make it winter scene"

# With output filename
qwen-image-mps edit -i photo.jpg -p "Add sunset colors" -o sunset_version.png

# Fast editing
qwen-image-mps edit -i landscape.jpg -p "Add dramatic clouds" --ultra-fast
```

## 🎛️ Parameters

### Common Parameters
- `-p, --prompt`: Text prompt (required)
- `-s, --steps`: Number of inference steps (default: 50)
- `--seed`: Random seed for reproducibility (default: 42)
- `--fast`: 8-step mode with Lightning LoRA v1.1
- `--ultra-fast`: 4-step mode with Lightning LoRA v1.0
- `--outdir`: Output directory (default: ./output)

### Generation Only
- `--num-images`: Number of images to generate (default: 1)
- `--aspect`: Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3)

### Editing Only
- `-i, --input`: Input image path (required)
- `-o, --output`: Output filename (optional)

## 📈 Performance Notes

**M3 Max Performance** (your system):
- **Memory**: 128GB (excellent for large models)
- **MPS Native**:
  - Ultra-fast mode: ~51 seconds for generation, ~3 minutes for editing
  - MPS utilization: Confirmed working
  - Model loading: One-time download (~57GB), cached locally
- **GGUF Option**:
  - Performance will vary based on quantization level
  - Can use the highest quality Q8_0 quantization (21.8GB)
  - May offer even faster inference times

## 🔧 Implementation Details

### MPS Native Approach
The `qwen-image-mps` tool uses PyTorch with MPS backend to run the full-precision model directly on the Apple GPU. It includes optimizations specifically for Apple Silicon and handles all the complexities of model loading and pipeline setup.

### GGUF Quantized Approach
The GGUF models are quantized versions that reduce memory usage and potentially improve inference speed. These models work with the ComfyUI-GGUF extension within ComfyUI. You'll need several components:

1. **Main Model** (unet): The core diffusion model (multiple quantization options)
2. **Text Encoder**: The Qwen2.5-VL-7B model for processing text
3. **MMPROJ Adapter**: For visual-language understanding
4. **VAE**: For encoding/decoding images

Both approaches are valid, with MPS being simpler but potentially heavier on memory, while GGUF requires more setup but may offer better performance with lower memory usage.

## 🔧 Troubleshooting

### Common Issues

1. **"Using CPU" instead of MPS**
   - Ensure you're using the `qwen-image` environment
   - Check PyTorch MPS availability: `python -c "import torch; print(torch.backends.mps.is_available())"`

2. **Model download slow/fails**
   - Check internet connection
   - Models are cached in `~/.cache/huggingface/hub/`

3. **Out of memory errors**
   - Try reducing steps: `-s 20` instead of `-s 50`
   - Use ultra-fast mode: `--ultra-fast`
   - Consider switching to GGUF with lower quantization (Q4_K_M or Q2_K)

4. **ComfyUI node not found**
   - Ensure ComfyUI-GGUF extension is properly installed
   - Restart ComfyUI

## 📸 Sample Outputs

Both image generation and editing are working successfully with MPS acceleration on your M3 Max system. The generated images show:

- High quality output even in ultra-fast mode
- Proper MPS hardware acceleration utilization  
- Fast inference times suitable for interactive use
- Successful semantic and appearance editing capabilities

## 🔗 Useful Links

### MPS Native Approach
- [Qwen Image Model](https://huggingface.co/Qwen/Qwen-Image-Edit)
- [qwen-image-mps Tool](https://github.com/ivanfioravanti/qwen-image-mps)
- [Lightning LoRA](https://huggingface.co/lightx2v/Qwen-Image-Lightning)

### GGUF Quantized Approach
- [GGUF Quantized Version](https://huggingface.co/QuantStack/Qwen-Image-Edit-GGUF)
- [Qwen2.5-VL-7B GGUF](https://huggingface.co/unsloth/Qwen2.5-VL-7B-Instruct-GGUF)
- [ComfyUI-GGUF Extension](https://github.com/city96/ComfyUI-GGUF)
- [Qwen Text Encoders](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/tree/main/split_files/text_encoders)

---

## 🏆 Recommendation for M3 Max (128GB)

With your powerful M3 Max with 128GB RAM, you have the luxury of using either approach:

**Currently Implemented**: The MPS native approach is already set up and working perfectly. It offers a simple CLI interface and high-quality results, with generation times of ~51 seconds in ultra-fast mode.

**Potential Optimization**: If you want even faster performance, you could explore the GGUF quantized approach with ComfyUI. With 128GB RAM, you could use the highest quality Q8_0 quantization while still having plenty of memory to spare.

Given that the MPS native approach is already working well and delivering good performance, I recommend sticking with it for now. If you later want to experiment with potentially faster inference via GGUF, the setup instructions are included in this README.

**🎉 Setup Complete!** Your Qwen Image Edit installation is ready to use with full Apple Silicon acceleration.
