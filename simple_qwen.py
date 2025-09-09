#!/usr/bin/env python3
"""
Ultra-simple Qwen Image Edit for macOS - Just Works™

Generate and edit images with AI on Apple Silicon.
No complexity, no bloat, just fast results.
"""

import torch
import click
import time
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


def load_pipeline():
    """Load the Qwen Image Edit pipeline."""
    print("Loading Qwen Image Edit model...")
    start = time.time()
    
    from diffusers import QwenImageEditPipeline
    
    device, dtype = setup_device()
    
    # Load pipeline
    pipeline = QwenImageEditPipeline.from_pretrained(
        "Qwen/Qwen-Image-Edit",
        torch_dtype=dtype,
        trust_remote_code=True
    ).to(device)
    
    # Load Lightning LoRA for 4x speed boost
    try:
        pipeline.load_lora_weights(
            "lightx2v/Qwen-Image-Lightning", 
            weight_name="Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors"
        )
        pipeline.fuse_lora()
        print("⚡ Lightning LoRA loaded - 4x faster!")
    except Exception as e:
        print(f"⚠️ Lightning LoRA failed to load: {e}")
        print("Continuing with standard model...")
    
    load_time = time.time() - start
    print(f"✅ Model ready in {load_time:.1f}s")
    
    return pipeline, device


def save_and_preview(image, filename=None):
    """Save image and auto-preview on Mac."""
    # Create output directory
    output_dir = Path.home() / "qwen-images"
    output_dir.mkdir(exist_ok=True)
    
    # Generate filename if not provided
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
            print("👀 Opening in preview...")
        except:
            pass
    
    return output_path


@click.group()
def cli():
    """🎨 Qwen Image Edit - AI image generation and editing for macOS
    
    Generate stunning images or edit existing ones with AI.
    Optimized for Apple Silicon with Lightning-fast results.
    
    Examples:
      qwen generate "a red sports car"
      qwen edit photo.jpg "make it look like a painting"
    """
    pass


@cli.command()
@click.argument('prompt')
@click.option('-o', '--output', help='Output filename')
@click.option('--steps', default=4, help='Number of steps (4=lightning, 50=quality)')
@click.option('--seed', type=int, help='Random seed for reproducible results')
def generate(prompt, output, steps, seed):
    """Generate a new image from text.
    
    Examples:
      qwen generate "a beautiful sunset over mountains"
      qwen generate "cyberpunk city at night" --steps 50
      qwen generate "cute cat" --seed 42 -o my_cat.png
    """
    print(f"🎨 Generating: {prompt}")
    
    # Load pipeline
    pipeline, device = load_pipeline()
    
    # Setup generator with seed
    generator = None
    if seed is not None:
        generator = torch.Generator(device="cpu" if device.type == "mps" else device)
        generator.manual_seed(seed)
        print(f"🎲 Using seed: {seed}")
    
    # Lightning vs quality mode
    if steps == 4:
        print("⚡ Lightning mode (4 steps)")
        cfg_scale = 1.0
    else:
        print(f"🎨 Quality mode ({steps} steps)")
        cfg_scale = 7.5
    
    # Generate
    print("Generating...")
    start = time.time()
    
    result = pipeline(
        image=None,  # Text-to-image mode
        prompt=prompt,
        num_inference_steps=steps,
        true_cfg_scale=cfg_scale,
        width=1024,
        height=1024,
        generator=generator,
    )
    
    gen_time = time.time() - start
    
    # Save and show
    image = result.images[0]
    output_path = save_and_preview(image, output)
    
    print(f"✅ Done in {gen_time:.1f}s - {1024}x{1024} pixels")
    print(f"📁 Find it at: {output_path.parent}")


@cli.command()
@click.argument('image_path')
@click.argument('prompt') 
@click.option('-o', '--output', help='Output filename')
@click.option('--steps', default=4, help='Number of steps (4=lightning, 50=quality)')
@click.option('--seed', type=int, help='Random seed for reproducible results')
def edit(image_path, prompt, output, steps, seed):
    """Edit an existing image with AI.
    
    Just drag your image file into the terminal after 'qwen edit'!
    
    Examples:
      qwen edit photo.jpg "add snow to the mountains"
      qwen edit portrait.png "make it oil painting style" --steps 50
      qwen edit landscape.jpg "change to sunset lighting" --seed 42
    """
    # Clean up the path (handle drag-and-drop)
    image_path = image_path.strip('"\'')
    img_path = Path(image_path)
    
    if not img_path.exists():
        print(f"❌ Image not found: {img_path}")
        print("💡 Tip: Drag your image file directly into the terminal!")
        return
    
    print(f"✏️ Editing: {img_path.name}")
    print(f"📝 Edit: {prompt}")
    
    # Load image
    try:
        image = Image.open(img_path).convert("RGB")
        print(f"📏 Input: {image.size[0]}x{image.size[1]} pixels")
    except Exception as e:
        print(f"❌ Could not load image: {e}")
        return
    
    # Load pipeline
    pipeline, device = load_pipeline()
    
    # Setup generator
    generator = None
    if seed is not None:
        generator = torch.Generator(device="cpu" if device.type == "mps" else device)
        generator.manual_seed(seed)
        print(f"🎲 Using seed: {seed}")
    
    # Lightning vs quality mode  
    if steps == 4:
        print("⚡ Lightning mode (4 steps)")
        cfg_scale = 1.0
    else:
        print(f"🎨 Quality mode ({steps} steps)")
        cfg_scale = 7.5
    
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
    
    # Save and show
    edited_image = result.images[0]
    output_path = save_and_preview(edited_image, output)
    
    print(f"✅ Done in {edit_time:.1f}s - {edited_image.size[0]}x{edited_image.size[1]} pixels")
    print(f"📁 Find it at: {output_path.parent}")


@cli.command()
def test():
    """Quick test to verify everything works."""
    print("🧪 Running quick test...")
    
    # Test device
    device, dtype = setup_device()
    print(f"✅ Device: {device} ({dtype})")
    
    # Test tensor operations
    if device.type == "mps":
        try:
            x = torch.randn(100, 100, device=device, dtype=dtype)
            y = torch.mm(x, x)
            print("✅ MPS tensor operations working")
        except Exception as e:
            print(f"❌ MPS test failed: {e}")
            return
    
    # Test generation with simple prompt
    try:
        print("🎨 Testing generation with simple prompt...")
        pipeline, _ = load_pipeline()
        
        result = pipeline(
            image=None,
            prompt="a red circle",
            num_inference_steps=4,
            true_cfg_scale=1.0,
            width=512,
            height=512,
        )
        
        # Save test image
        test_image = result.images[0]
        test_path = Path.home() / "qwen-images" / "test.png"
        test_path.parent.mkdir(exist_ok=True)
        test_image.save(test_path)
        
        print(f"✅ Test image generated: {test_path}")
        print("🎉 Everything works!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Try: pip install diffusers transformers torch pillow")


if __name__ == '__main__':
    cli()
