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
    """Load the Qwen Image pipeline for text-to-image generation."""
    print("Loading Qwen Image generation model...")
    start = time.time()
    
    from diffusers import QwenImagePipeline
    device, dtype = setup_device()
    
    pipeline = QwenImagePipeline.from_pretrained(
        "Qwen/Qwen-Image",
        torch_dtype=dtype,
    ).to(device)
    
    # Try to load Lightning LoRA for speed
    try:
        pipeline.load_lora_weights(
            "lightx2v/Qwen-Image-Lightning", 
            weight_name="Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors"
        )
        pipeline.fuse_lora()
        print("⚡ Lightning LoRA loaded - 4x faster!")
    except Exception as e:
        print(f"⚠️ Lightning LoRA failed: {str(e)[:100]}...")
        print("Continuing with standard model...")
    
    load_time = time.time() - start
    print(f"✅ Generation model ready in {load_time:.1f}s")
    return pipeline, device


def load_editing_pipeline():
    """Load the Qwen Image Edit pipeline for image editing."""
    print("Loading Qwen Image Edit model...")
    start = time.time()
    
    from diffusers import QwenImageEditPipeline
    device, dtype = setup_device()
    
    pipeline = QwenImageEditPipeline.from_pretrained(
        "Qwen/Qwen-Image-Edit",
        torch_dtype=dtype,
    ).to(device)
    
    # Try to load Lightning LoRA for speed
    try:
        pipeline.load_lora_weights(
            "lightx2v/Qwen-Image-Lightning", 
            weight_name="Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors"
        )
        pipeline.fuse_lora()
        print("⚡ Lightning LoRA loaded - 4x faster!")
    except Exception as e:
        print(f"⚠️ Lightning LoRA failed: {str(e)[:100]}...")
        print("Continuing with standard model...")
    
    load_time = time.time() - start
    print(f"✅ Edit model ready in {load_time:.1f}s")
    return pipeline, device


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
        except:
            pass
    
    return output_path


@click.group()
def cli():
    """🎨 Qwen Image - AI image generation and editing for macOS
    
    Fast AI image tools optimized for Apple Silicon.
    
    Examples:
      qwen generate "a beautiful mountain landscape"
      qwen edit photo.jpg "make it look like a painting"
      qwen test
    """
    pass


@cli.command()
@click.argument('prompt')
@click.option('-o', '--output', help='Output filename')  
@click.option('--steps', default=50, help='Inference steps (50=quality, 4=fast)')
@click.option('--seed', type=int, help='Random seed')
@click.option('--size', default='1024x1024', help='Image size (e.g. 1024x1024)')
def generate(prompt, output, steps, seed, size):
    """Generate a new image from text.
    
    Examples:
      qwen generate "a cyberpunk cityscape at night"
      qwen generate "cute corgi puppy" --steps 4 --seed 42
    """
    print(f"🎨 Generating: {prompt}")
    
    # Parse size
    try:
        width, height = map(int, size.split('x'))
    except:
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
    if steps <= 4:
        print("⚡ Lightning mode (4 steps)")
    else:
        print(f"🎨 Quality mode ({steps} steps)")
    
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
@click.option('--steps', default=50, help='Inference steps (50=quality, 4=fast)')
@click.option('--seed', type=int, help='Random seed')
def edit(image_path, prompt, output, steps, seed):
    """Edit an existing image with AI.
    
    Drag your image file into the terminal after 'qwen edit'!
    
    Examples:
      qwen edit photo.jpg "add snow to the mountains"
      qwen edit portrait.png "oil painting style" --steps 4
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
    except Exception as e:
        print(f"❌ Could not load image: {e}")
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
    if steps <= 4:
        print("⚡ Lightning mode (4 steps)")
        cfg_scale = 1.0
    else:
        print(f"🎨 Quality mode ({steps} steps)")
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
    """Quick test to verify everything works."""
    print("🧪 Testing Qwen Image...")
    
    # Test device
    device, dtype = setup_device()
    print(f"✅ Device: {device} ({dtype})")
    
    # Test MPS operations
    if device.type == "mps":
        try:
            x = torch.randn(100, 100, device=device, dtype=dtype)
            y = torch.mm(x, x)
            print("✅ MPS operations working")
        except Exception as e:
            print(f"❌ MPS failed: {e}")
            return
    
    # Quick generation test
    try:
        print("🎨 Testing text-to-image generation...")
        pipeline, _ = load_generation_pipeline()
        
        result = pipeline(
            prompt="a simple red circle",
            num_inference_steps=4,
            width=512,
            height=512,
        )
        
        # Save test result
        test_image = result.images[0]
        test_path = Path.home() / "qwen-images" / "test_generation.png"
        test_path.parent.mkdir(exist_ok=True)
        test_image.save(test_path)
        
        print(f"✅ Generation test passed: {test_path}")
        
        # Quick editing test using the generated image
        print("✏️ Testing image editing...")
        edit_pipeline, _ = load_editing_pipeline()
        
        edit_result = edit_pipeline(
            image=test_image,
            prompt="make it blue",
            num_inference_steps=4,
            true_cfg_scale=1.0,
        )
        
        edit_test_path = Path.home() / "qwen-images" / "test_edit.png"
        edit_result.images[0].save(edit_test_path)
        
        print(f"✅ Editing test passed: {edit_test_path}")
        print("🎉 All tests passed! Ready to create amazing images!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


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
    print("  • Use --steps 4 for fast results")
    print("  • Use --steps 50 for best quality")
    print("  • Drag images into terminal for editing")
    print("  • Run 'qwen test' to verify everything works")


if __name__ == '__main__':
    cli()
