"""
Professional CLI interface for Qwen Image Edit macOS.
"""

import click
from pathlib import Path
from typing import Optional, Tuple
import sys
import os

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from ..core.pipeline import QwenImagePipeline
from ..core.config import Config
from .. import __version__


console = Console()


def validate_image_path(ctx, param, value):
    """Validate that image path exists."""
    if value is None:
        return None
    path = Path(value)
    if not path.exists():
        raise click.BadParameter(f"Image file not found: {path}")
    if not path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        raise click.BadParameter(f"Unsupported image format: {path.suffix}")
    return path


def validate_size(ctx, param, value):
    """Validate image size parameter."""
    if value is None:
        return None
    try:
        if 'x' in value:
            width, height = map(int, value.split('x'))
        else:
            # Handle aspect ratios like "16:9"
            if ':' in value:
                w_ratio, h_ratio = map(int, value.split(':'))
                # Convert to standard size maintaining aspect ratio
                if w_ratio == 16 and h_ratio == 9:
                    width, height = 1664, 928
                elif w_ratio == 1 and h_ratio == 1:
                    width, height = 1024, 1024
                elif w_ratio == 4 and h_ratio == 3:
                    width, height = 1536, 1152
                else:
                    # Default calculation for other ratios
                    base_size = 1024
                    if w_ratio >= h_ratio:
                        width = base_size * w_ratio // min(w_ratio, h_ratio)
                        height = base_size * h_ratio // min(w_ratio, h_ratio)
                    else:
                        width = base_size * w_ratio // min(w_ratio, h_ratio)
                        height = base_size * h_ratio // min(w_ratio, h_ratio)
            else:
                raise ValueError("Invalid format")
        
        if width < 256 or height < 256:
            raise click.BadParameter("Image dimensions must be at least 256x256")
        if width > 2048 or height > 2048:
            raise click.BadParameter("Image dimensions must not exceed 2048x2048")
        
        return (width, height)
    except ValueError:
        raise click.BadParameter(
            "Size must be in format 'WxH' (e.g., '1024x1024') or aspect ratio (e.g., '16:9')"
        )


@click.group()
@click.version_option(version=__version__, prog_name="qwen-image")
@click.option('--config-dir', type=click.Path(), help='Configuration directory path')
@click.pass_context
def cli(ctx, config_dir):
    """
    🎨 Qwen Image Edit for macOS
    
    Professional image generation and editing optimized for Apple Silicon.
    """
    ctx.ensure_object(dict)
    
    # Initialize configuration
    config_path = Path(config_dir) / "config.yaml" if config_dir else None
    try:
        ctx.obj['config'] = Config(config_path)
    except Exception as e:
        console.print(Panel(
            f"❌ Configuration Error: {e}\n\n"
            "Try running with --help for usage information.",
            title="Error",
            style="red"
        ))
        sys.exit(1)
    
    # Initialize pipeline (lazy loading)
    ctx.obj['pipeline'] = None


def get_pipeline(ctx) -> QwenImagePipeline:
    """Get or create pipeline instance."""
    if ctx.obj['pipeline'] is None:
        ctx.obj['pipeline'] = QwenImagePipeline(ctx.obj['config'])
    return ctx.obj['pipeline']


@cli.command()
@click.option('-p', '--prompt', required=True, help='Text description of the image to generate')
@click.option('-n', '--negative-prompt', help='What to avoid in the generated image')
@click.option('-s', '--steps', type=int, help='Number of inference steps (default: auto)')
@click.option('-c', '--cfg-scale', type=float, help='Guidance scale (default: auto)')
@click.option('--size', callback=validate_size, help='Image size as WxH or aspect ratio (e.g., 1024x1024, 16:9)')
@click.option('--seed', type=int, help='Random seed for reproducible results')
@click.option('--lightning/--no-lightning', default=None, help='Use Lightning LoRA for faster generation')
@click.option('-o', '--output', help='Output filename (auto-generated if not provided)')
@click.option('--output-dir', type=click.Path(), help='Output directory (default: ~/.qwen-image-edit/outputs)')
@click.pass_context
def generate(ctx, prompt, negative_prompt, steps, cfg_scale, size, seed, lightning, output, output_dir):
    """Generate a new image from text description."""
    
    pipeline = get_pipeline(ctx)
    
    try:
        # Generate image
        image = pipeline.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            steps=steps,
            cfg_scale=cfg_scale,
            size=size,
            seed=seed,
            use_lightning=lightning,
        )
        
        # Save image
        output_dir_path = Path(output_dir) if output_dir else None
        saved_path = pipeline.save_image(image, filename=output, output_dir=output_dir_path)
        
        console.print(Panel(
            f"🎉 Image saved to: [bold green]{saved_path}[/bold green]\n"
            f"💾 Size: {image.size[0]}x{image.size[1]} pixels",
            title="Success",
            style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n⚠️ Generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        console.print(Panel(
            f"❌ Generation failed: {e}",
            title="Error",
            style="red"
        ))
        sys.exit(1)


@cli.command()
@click.option('-i', '--input', 'input_image', required=True, callback=validate_image_path,
              help='Path to the input image to edit')
@click.option('-p', '--prompt', required=True, help='Description of the desired changes')
@click.option('-n', '--negative-prompt', help='What to avoid in the edited image')
@click.option('-s', '--steps', type=int, help='Number of inference steps (default: auto)')
@click.option('-c', '--cfg-scale', type=float, help='Guidance scale (default: auto)')
@click.option('--seed', type=int, help='Random seed for reproducible results')
@click.option('--lightning/--no-lightning', default=None, help='Use Lightning LoRA for faster editing')
@click.option('-o', '--output', help='Output filename (auto-generated if not provided)')
@click.option('--output-dir', type=click.Path(), help='Output directory (default: ~/.qwen-image-edit/outputs)')
@click.pass_context
def edit(ctx, input_image, prompt, negative_prompt, steps, cfg_scale, seed, lightning, output, output_dir):
    """Edit an existing image with text instructions."""
    
    pipeline = get_pipeline(ctx)
    
    try:
        # Edit image
        edited_image = pipeline.edit(
            image=input_image,
            prompt=prompt,
            negative_prompt=negative_prompt,
            steps=steps,
            cfg_scale=cfg_scale,
            seed=seed,
            use_lightning=lightning,
        )
        
        # Save edited image
        output_dir_path = Path(output_dir) if output_dir else None
        saved_path = pipeline.save_image(edited_image, filename=output, output_dir=output_dir_path)
        
        console.print(Panel(
            f"🎉 Edited image saved to: [bold green]{saved_path}[/bold green]\n"
            f"📷 Input: {input_image.name} ({input_image.stat().st_size // 1024}KB)\n"
            f"💾 Output: {edited_image.size[0]}x{edited_image.size[1]} pixels",
            title="Success",
            style="green"
        ))
        
    except KeyboardInterrupt:
        console.print("\n⚠️ Editing cancelled by user")
        sys.exit(1)
    except Exception as e:
        console.print(Panel(
            f"❌ Editing failed: {e}",
            title="Error",
            style="red"
        ))
        sys.exit(1)


@cli.command()
@click.pass_context
def status(ctx):
    """Show system status and configuration."""
    
    config = ctx.obj['config']
    
    # System Information Table
    system_table = Table(title="🖥️ System Information")
    system_table.add_column("Property", style="cyan")
    system_table.add_column("Value", style="white")
    
    system_table.add_row("Platform", config.system_info.platform)
    system_table.add_row("Chip", config.system_info.chip)
    system_table.add_row("Memory", f"{config.system_info.memory_gb} GB")
    system_table.add_row("Python", config.system_info.python_version)
    
    if config.system_info.torch_version:
        system_table.add_row("PyTorch", config.system_info.torch_version)
        mps_status = "✅ Available" if config.system_info.has_mps else "❌ Not Available"
        system_table.add_row("MPS Support", mps_status)
    else:
        system_table.add_row("PyTorch", "❌ Not Installed")
    
    console.print(system_table)
    console.print()
    
    # Configuration Table
    config_table = Table(title="⚙️ Configuration")
    config_table.add_column("Setting", style="cyan")
    config_table.add_column("Value", style="white")
    
    config_table.add_row("Output Directory", str(config.output_config.output_dir))
    config_table.add_row("Cache Directory", str(config.model_config.cache_dir))
    config_table.add_row("Lightning LoRA", "✅ Enabled" if config.model_config.use_lightning else "❌ Disabled")
    config_table.add_row("Lightning Steps", str(config.model_config.lightning_steps))
    config_table.add_row("Default Steps", str(config.model_config.default_steps))
    
    console.print(config_table)
    console.print()
    
    # Recommendations
    recommendations = config.get_recommended_settings()
    
    rec_table = Table(title="💡 Recommendations for Your System")
    rec_table.add_column("Setting", style="cyan")
    rec_table.add_column("Recommended Value", style="green")
    
    rec_table.add_row("Quality Preset", recommendations.get("quality_preset", "balanced"))
    rec_table.add_row("Use Lightning", "✅ Yes" if recommendations.get("use_lightning") else "❌ No")
    rec_table.add_row("Recommended Steps", str(recommendations.get("steps", "auto")))
    
    console.print(rec_table)


@cli.command()
@click.option('--output-dir', type=click.Path(), help='Directory to save examples')
@click.pass_context
def examples(ctx, output_dir):
    """Generate example images to test the installation."""
    
    pipeline = get_pipeline(ctx)
    output_dir_path = Path(output_dir) if output_dir else pipeline.config.output_config.output_dir / "examples"
    output_dir_path.mkdir(parents=True, exist_ok=True)
    
    example_prompts = [
        "A serene mountain lake at sunset with pine trees reflected in the water",
        "A cozy coffee shop interior with warm lighting and people working on laptops", 
        "A futuristic cityscape at night with neon lights and flying cars",
    ]
    
    console.print(Panel(
        f"🎨 Generating {len(example_prompts)} example images...\n"
        f"📁 Output directory: {output_dir_path}",
        title="Example Generation",
        style="blue"
    ))
    
    for i, prompt in enumerate(example_prompts, 1):
        try:
            console.print(f"\n📸 Example {i}/{len(example_prompts)}")
            
            # Generate with lightning for speed
            image = pipeline.generate(
                prompt=prompt,
                use_lightning=True,
            )
            
            # Save with descriptive name
            filename = f"example_{i:02d}_{prompt[:50].replace(' ', '_').replace(',', '')}.png"
            saved_path = pipeline.save_image(image, filename=filename, output_dir=output_dir_path)
            
            console.print(f"✅ Saved: {saved_path.name}")
            
        except KeyboardInterrupt:
            console.print(f"\n⚠️ Example generation cancelled at {i}/{len(example_prompts)}")
            break
        except Exception as e:
            console.print(f"❌ Failed to generate example {i}: {e}")
    
    console.print(Panel(
        f"🎉 Example generation complete!\n"
        f"📁 Check your images in: {output_dir_path}",
        title="Examples Ready",
        style="green"
    ))


@cli.command()
@click.option('--reset', is_flag=True, help='Reset configuration to defaults')
@click.pass_context
def config_cmd(ctx, reset):
    """Manage configuration settings."""
    
    config = ctx.obj['config']
    
    if reset:
        # Reset configuration
        if config.config_path.exists():
            config.config_path.unlink()
        
        # Recreate with defaults
        config._create_default_config()
        
        console.print(Panel(
            f"✅ Configuration reset to defaults\n"
            f"📄 Config file: {config.config_path}",
            title="Configuration Reset",
            style="green"
        ))
    else:
        # Show current configuration
        console.print(Panel(
            str(config),
            title="Current Configuration",
            style="blue"
        ))
        
        console.print(f"\n📄 Configuration file: {config.config_path}")
        console.print(f"💡 Edit the file directly or use --reset to restore defaults")


def main():
    """Main entry point for the CLI."""
    # Set up environment
    os.environ.setdefault('PYTORCH_ENABLE_MPS_FALLBACK', '1')
    
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        console.print(Panel(
            f"❌ Unexpected error: {e}\n\n"
            "Please report this issue at: https://github.com/yourusername/qwen-image-edit-macos/issues",
            title="Fatal Error",
            style="red"
        ))
        sys.exit(1)


if __name__ == '__main__':
    main()
