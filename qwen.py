#!/usr/bin/env python3
"""
🎨 Qwen Image for macOS - AI image generation and editing

Simple, fast AI image tools optimized for Apple Silicon.
Just works. No complexity.
"""

import torch
import click
import time
import sys
from pathlib import Path
from PIL import Image
import platform


def setup_device():
    """Get the best available device."""
    if torch.backends.mps.is_available():
        print("🚀 Using Apple Silicon GPU (MPS)")
        return torch.device("mps"), torch.bfloat16
    else:
        print("💻 Using CPU")
        return torch.device("cpu"), torch.float32


def load_generation_pipeline():
    """Load generation pipeline with Lightning LoRA."""
    print("📥 Loading Qwen Image model (first run downloads ~20GB)...")
    start = time.time()
    
    try:
        from diffusers import QwenImagePipeline
        device, dtype = setup_device()
        
        pipeline = QwenImagePipeline.from_pretrained(
            "Qwen/Qwen-Image",
            torch_dtype=dtype,
        ).to(device)
        
        # Load Lightning LoRA for speed optimization
        try:
            pipeline.load_lora_weights(
                "lightx2v/Qwen-Image-Lightning", 
                weight_name="Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors"
            )
            pipeline.fuse_lora()
            print("⚡ Lightning LoRA loaded - optimized for speed!")
        except (OSError, ValueError, RuntimeError):
            print("⚠️ Lightning LoRA not available, using standard model")
        
        load_time = time.time() - start
        print(f"✅ Ready in {load_time:.1f}s")
        return pipeline, device
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        print("💡 Try: pip install --upgrade diffusers transformers")
        sys.exit(1)


def load_editing_pipeline():
    """Load editing pipeline with Lightning LoRA."""
    print("📥 Loading Qwen Image Edit model...")
    start = time.time()
    
    try:
        from diffusers import QwenImageEditPipeline
        device, dtype = setup_device()
        
        pipeline = QwenImageEditPipeline.from_pretrained(
            "Qwen/Qwen-Image-Edit",
            torch_dtype=dtype,
        ).to(device)
        
        # Load Lightning LoRA for speed optimization  
        try:
            pipeline.load_lora_weights(
                "lightx2v/Qwen-Image-Lightning", 
                weight_name="Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors"
            )
            pipeline.fuse_lora()
            print("⚡ Lightning LoRA loaded - optimized for speed!")
        except (OSError, ValueError, RuntimeError):
            print("⚠️ Lightning LoRA not available, using standard model")
        
        load_time = time.time() - start
        print(f"✅ Ready in {load_time:.1f}s")
        return pipeline, device
        
    except Exception as e:
        print(f"❌ Failed to load editing model: {e}")
        print("💡 Try: pip install --upgrade diffusers transformers")
        sys.exit(1)


def save_and_preview(image, filename=None):
    """Save image and auto-preview on Mac."""
    output_dir = Path.home() / "qwen-images"
    output_dir.mkdir(exist_ok=True)
    
    if not filename:
        timestamp = int(time.time())
        filename = f"qwen_{timestamp}.png"
    
    if not filename.endswith(('.png', '.jpg', '.jpeg')):
        filename += '.png'
    
    output_path = output_dir / filename
    image.save(output_path, optimize=True)
    print(f"💾 Saved: {output_path}")
    
    # Auto-preview on Mac
    if platform.system() == "Darwin":
        import subprocess
        try:
            subprocess.run(["open", str(output_path)], check=True)
            print("👀 Opening preview...")
        except subprocess.SubprocessError:
            # Preview failed, but image was still saved successfully
            pass
    
    return output_path


@click.group()
def cli():
    """🎨 Qwen Image - AI image generation and editing for macOS
    
    Fast AI image tools optimized for Apple Silicon.
    
    Examples:
      python qwen.py generate "a beautiful mountain landscape"
      python qwen.py edit photo.jpg "make it look like a painting"
      python qwen.py test
    """
    pass


@cli.command()
@click.argument('prompt')
@click.option('-o', '--output', help='Output filename')  
@click.option('--steps', default=20, help='Inference steps (10=stylistic, 20=quality, 30=max)')
@click.option('--seed', type=int, help='Random seed')
@click.option('--size', default='1024x1024', help='Image size (e.g. 1024x1024)')
def generate(prompt, output, steps, seed, size):
    """Generate a new image from text.
    
    Examples:
      python qwen.py generate "a cyberpunk cityscape at night"
      python qwen.py generate "cute corgi puppy" --steps 20 --seed 42
    """
    print(f"🎨 Generating: {prompt}")
    
    # Parse size
    try:
        width, height = map(int, size.split('x'))
    except (ValueError, AttributeError):
        print(f"❌ Invalid size format: {size} (use WxH like 1024x1024)")
        sys.exit(1)
    
    # Load pipeline
    pipeline, device = load_generation_pipeline()
    
    # Setup generator
    generator = None
    if seed is not None:
        generator = torch.Generator(device="cpu" if device.type == "mps" else device)  
        generator.manual_seed(seed)
        print(f"🎲 Seed: {seed}")
    
    # Show settings
    if steps <= 10:
        print(f"🎨 Quick mode ({steps} steps) - stylistic results")
    elif steps <= 25:
        print(f"🎨 Quality mode ({steps} steps) - fully formed")
    else:
        print(f"🎆 Maximum quality mode ({steps} steps)")
    
    print(f"📐 Size: {width}x{height}")
    
    # Generate
    print("Generating...")
    start = time.time()
    
    result = pipeline(
        prompt=prompt,
        num_inference_steps=steps,
        width=width,
        height=height,
        generator=generator,
    )
    
    gen_time = time.time() - start
    
    # Save and preview
    image = result.images[0]
    output_path = save_and_preview(image, output)
    
    print(f"✅ Generated in {gen_time:.1f}s")
    print(f"📁 Location: {output_path.parent}")


@cli.command()
@click.argument('image_path')
@click.argument('prompt')
@click.option('-o', '--output', help='Output filename')
@click.option('--steps', default=20, help='Inference steps (10=stylistic, 20=quality, 30=max)')
@click.option('--seed', type=int, help='Random seed')
def edit(image_path, prompt, output, steps, seed):
    """Edit an existing image with AI.
    
    Drag your image file into the terminal after 'qwen edit'!
    
    Examples:
      python qwen.py edit photo.jpg "add snow to the mountains"
      python qwen.py edit portrait.png "oil painting style" --steps 20
    """
    # Handle drag-and-drop paths
    image_path = image_path.strip('"\'')
    img_path = Path(image_path)
    
    if not img_path.exists():
        print(f"❌ Image not found: {img_path}")
        print("💡 Tip: Drag your image into the terminal!")
        sys.exit(1)
    
    print(f"✏️ Editing: {img_path.name}")
    print(f"📝 Edit: {prompt}")
    
    # Load and validate image
    try:
        image = Image.open(img_path).convert("RGB")
        print(f"📏 Input: {image.size[0]}x{image.size[1]} pixels")
    except (OSError, ValueError) as e:
        print(f"❌ Could not load image: {e}")
        print("💡 Make sure the file is a valid image format")
        sys.exit(1)
    
    # Load pipeline
    pipeline, device = load_editing_pipeline()
    
    # Setup generator
    generator = None
    if seed is not None:
        generator = torch.Generator(device="cpu" if device.type == "mps" else device)
        generator.manual_seed(seed)
        print(f"🎲 Seed: {seed}")
    
    # Show settings  
    if steps <= 10:
        print(f"🎨 Quick mode ({steps} steps) - stylistic results")
        cfg_scale = 2.0
    elif steps <= 25:
        print(f"🎨 Quality mode ({steps} steps) - fully formed")
        cfg_scale = 4.0
    else:
        print(f"🎆 Maximum quality mode ({steps} steps)")
        cfg_scale = 4.0
    
    # Edit
    print("Editing...")
    start = time.time()
    
    result = pipeline(
        image=image,
        prompt=prompt,
        num_inference_steps=steps,
        true_cfg_scale=cfg_scale,
        generator=generator,
    )
    
    edit_time = time.time() - start
    
    # Save and preview
    edited_image = result.images[0]
    output_path = save_and_preview(edited_image, output)
    
    print(f"✅ Edited in {edit_time:.1f}s")
    print(f"📁 Location: {output_path.parent}")


@cli.command()
def test():
    """Quick test - generates a demo image."""
    print("🧪 Testing Qwen Image on your Mac...")
    
    # Check device
    device, dtype = setup_device()
    if device.type == "mps":
        print("✅ Apple Silicon GPU ready")
    else:
        print("⚠️ Using CPU (will be slower)")
    
    # Quick demo generation
    try:
        print("🎨 Generating demo image...")
        pipeline, _ = load_generation_pipeline()
        
        start_time = time.time()
        result = pipeline(
            prompt="a cute robot waving hello",
            num_inference_steps=10,
            width=512,
            height=512,
        )
        gen_time = time.time() - start_time
        
        # Save and show
        test_image = result.images[0]
        output_dir = Path.home() / "qwen-images"
        output_dir.mkdir(exist_ok=True)
        test_path = output_dir / "demo.png"
        test_image.save(test_path)
        
        print(f"🎉 Demo image generated in {gen_time:.1f}s!")
        print(f"📁 Saved: {test_path}")
        print("📝 Note: This is a quick demo (10 steps). Use --steps 20 for higher quality!")
        
        # Auto-open on Mac
        if platform.system() == "Darwin":
            import subprocess
            subprocess.run(["open", str(test_path)], check=True)
            print("👀 Opening demo image...")
            
        print("\n🚀 Ready! Try: python qwen.py generate 'your prompt here' --steps 20")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Try: pip install --upgrade torch diffusers transformers")
        sys.exit(1)


@cli.command()
def status():
    """Show system status and tips."""
    device, dtype = setup_device()
    
    print(f"🖥️  System: {platform.platform()}")
    print(f"🔥 Device: {device} ({dtype})")
    print(f"🧠 PyTorch: {torch.__version__}")
    
    if device.type == "mps":
        print("✅ Apple Silicon GPU acceleration active")
    else:
        print("⚠️  Using CPU (slower)")
    
    # Check output directory
    output_dir = Path.home() / "qwen-images" 
    print(f"📁 Output: {output_dir}")
    if output_dir.exists():
        images = list(output_dir.glob("*.png")) + list(output_dir.glob("*.jpg"))
        print(f"🖼️  Images: {len(images)} created")
    
    print("\n💡 Tips:")
    print("  • Use --steps 10 for quick stylistic results")
    print("  • Use --steps 20 for fully formed, quality images")
    print("  • Use --steps 30 for maximum quality")
    print("  • Drag images into terminal for editing")
    print("  • Run 'python qwen.py test' to verify everything works")


if __name__ == '__main__':
    cli()
