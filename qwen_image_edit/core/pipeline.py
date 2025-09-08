"""
Main pipeline for Qwen Image generation and editing on macOS.
"""

import torch
from pathlib import Path
from typing import Optional, Union, Tuple, Dict, Any
from PIL import Image
import time
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text

from .config import Config


class QwenImagePipeline:
    """Professional pipeline for image generation and editing with Apple Silicon optimization."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.console = Console()
        self.pipeline = None  # Single pipeline for both generation and editing
        self._device = None
        self._dtype = None
        
        # Initialize device and data type
        self._setup_device()
        
    def _setup_device(self) -> None:
        """Setup optimal device and data type for Apple Silicon."""
        if self.config.system_info.has_mps and torch.backends.mps.is_available():
            self._device = torch.device("mps")
            self._dtype = torch.bfloat16
            device_info = f"🚀 Using Apple Silicon GPU (MPS) with {self._dtype}"
        else:
            self._device = torch.device("cpu")
            self._dtype = torch.float32
            device_info = "💻 Using CPU (MPS not available)"
            
        self.console.print(Panel(device_info, title="Device Configuration", style="green"))
    
    def _load_pipeline(self) -> None:
        """Load the Qwen Image Edit pipeline for both generation and editing."""
        if self.pipeline is not None:
            return
            
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Loading Qwen Image Edit model...", total=None)
            
            try:
                from diffusers import QwenImageEditPipeline
                
                # Load the pipeline - Qwen-Image-Edit can do both generation and editing
                self.pipeline = QwenImageEditPipeline.from_pretrained(
                    "Qwen/Qwen-Image-Edit",
                    torch_dtype=self._dtype,
                    trust_remote_code=True,
                    cache_dir=str(self.config.model_config.cache_dir),
                )
                
                progress.update(task, description="Moving model to device...")
                self.pipeline = self.pipeline.to(self._device)
                
                # Load Lightning LoRA if configured
                if self.config.model_config.use_lightning:
                    progress.update(task, description="Loading Lightning LoRA for acceleration...")
                    self._load_lightning_lora(self.pipeline, steps=self.config.model_config.lightning_steps)
                
                progress.update(task, description="✅ Qwen Image Edit pipeline ready!", completed=100)
                
            except Exception as e:
                progress.stop()
                self._handle_pipeline_error(e, "model loading")
                raise
    
    def _load_lightning_lora(self, pipeline, steps: int = 4) -> None:
        """Load Lightning LoRA for acceleration."""
        try:
            # Determine which Lightning LoRA to use
            if steps == 4:
                lora_id = "lightx2v/Qwen-Image-Lightning"
                lora_filename = "Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors"
                version = "v1.0 (4-steps)"
            else:
                lora_id = "lightx2v/Qwen-Image-Lightning"  
                lora_filename = "Qwen-Image-Lightning-8steps-V1.1-bf16.safetensors"
                version = "v1.1 (8-steps)"
            
            # Load and merge LoRA
            pipeline.load_lora_weights(lora_id, weight_name=lora_filename)
            pipeline.fuse_lora()
            
            self.console.print(f"⚡ Lightning LoRA {version} loaded and merged")
            
        except Exception as e:
            self.console.print(f"⚠️  Could not load Lightning LoRA: {e}")
            self.console.print("Continuing with standard model...")
    
    def _handle_pipeline_error(self, error: Exception, pipeline_type: str) -> None:
        """Handle pipeline loading errors with helpful guidance."""
        error_msg = str(error)
        
        suggestions = []
        if "out of memory" in error_msg.lower() or "memory" in error_msg.lower():
            suggestions.extend([
                "Your system may be running low on memory",
                f"Try freeing up memory by closing other applications",
                "Consider using a smaller model size or reducing batch size"
            ])
        elif "connection" in error_msg.lower() or "download" in error_msg.lower():
            suggestions.extend([
                "Check your internet connection",
                "The model download may have been interrupted",
                f"Try clearing the cache: rm -rf {self.config.model_config.cache_dir}/*"
            ])
        elif "mps" in error_msg.lower():
            suggestions.extend([
                "There may be an issue with Metal Performance Shaders",
                "Try updating to the latest macOS version",
                "Consider falling back to CPU: export PYTORCH_ENABLE_MPS_FALLBACK=1"
            ])
        else:
            suggestions.extend([
                "Check that all dependencies are properly installed",
                "Try reinstalling the package: pip install --upgrade --force-reinstall qwen-image-edit-macos"
            ])
        
        panel_content = f"❌ Failed to load {pipeline_type} pipeline:\n{error}\n\n💡 Suggestions:\n" + \
                       "\n".join(f"  • {s}" for s in suggestions)
        
        self.console.print(Panel(panel_content, title="Pipeline Error", style="red"))
    
    def generate(
        self,
        prompt: str,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        size: Optional[Tuple[int, int]] = None,
        seed: Optional[int] = None,
        use_lightning: Optional[bool] = None,
    ) -> Image.Image:
        """Generate an image from a text prompt using Qwen Image Edit."""
        
        # Load pipeline if needed
        self._load_pipeline()
        
        # Use intelligent defaults
        use_lightning = use_lightning if use_lightning is not None else self.config.model_config.use_lightning
        steps = steps or (self.config.model_config.lightning_steps if use_lightning else self.config.model_config.default_steps)
        cfg_scale = cfg_scale or (self.config.model_config.lightning_cfg_scale if use_lightning else self.config.model_config.default_cfg_scale)
        size = size or self.config.output_config.default_size
        
        # Setup generation parameters
        generator = torch.Generator(device="cpu" if self._device.type == "mps" else self._device)
        if seed is not None:
            generator.manual_seed(seed)
        
        # Display generation info
        mode_info = "⚡ Lightning" if use_lightning else "🎨 Standard"
        generation_info = f"{mode_info} | {steps} steps | {size[0]}x{size[1]} | CFG {cfg_scale}"
        
        self.console.print(Panel(
            f"Prompt: [bold]{prompt}[/bold]\n" +
            f"Settings: {generation_info}",
            title="🎨 Generating Image",
            style="blue"
        ))
        
        # Generate with progress
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Generating...", total=steps)
            
            # Callback to update progress
            def callback(step, timestep, latents):
                progress.update(task, advance=1)
            
            # Generate image using Qwen Image Edit pipeline
            # Note: For generation-only, pass image=None or use text-to-image mode
            result = self.pipeline(
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                true_cfg_scale=cfg_scale,
                width=size[0],
                height=size[1],
                generator=generator,
                # Note: QwenImageEditPipeline may not support callback
            )
        
        generation_time = time.time() - start_time
        self.console.print(f"✅ Generated in {generation_time:.1f} seconds")
        
        return result.images[0]
    
    def edit(
        self,
        image: Union[Image.Image, str, Path],
        prompt: str,
        negative_prompt: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[float] = None,
        seed: Optional[int] = None,
        use_lightning: Optional[bool] = None,
    ) -> Image.Image:
        """Edit an existing image based on a text prompt."""
        
        # Load pipeline if needed
        self._load_pipeline()
        
        # Load and validate input image
        if isinstance(image, (str, Path)):
            image_path = Path(image)
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            image = Image.open(image_path).convert("RGB")
        elif not isinstance(image, Image.Image):
            raise ValueError("Image must be PIL Image, string path, or Path object")
        
        # Use intelligent defaults
        use_lightning = use_lightning if use_lightning is not None else self.config.model_config.use_lightning
        steps = steps or (self.config.model_config.lightning_steps if use_lightning else self.config.model_config.default_steps)
        cfg_scale = cfg_scale or (self.config.model_config.lightning_cfg_scale if use_lightning else self.config.model_config.default_cfg_scale)
        
        # Setup generation parameters
        generator = torch.Generator(device="cpu" if self._device.type == "mps" else self._device)
        if seed is not None:
            generator.manual_seed(seed)
        
        # Display editing info
        mode_info = "⚡ Lightning" if use_lightning else "🎨 Standard"
        editing_info = f"{mode_info} | {steps} steps | {image.size[0]}x{image.size[1]} | CFG {cfg_scale}"
        
        self.console.print(Panel(
            f"Edit: [bold]{prompt}[/bold]\n" +
            f"Input: {image.size[0]}x{image.size[1]} image\n" +
            f"Settings: {editing_info}",
            title="✏️ Editing Image",
            style="blue"
        ))
        
        # Edit with progress
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Editing...", total=steps)
            
            # Callback to update progress
            def callback(step, timestep, latents):
                progress.update(task, advance=1)
            
            # Edit image
            result = self.pipeline(
                image=image,
                prompt=prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                true_cfg_scale=cfg_scale,
                generator=generator,
                # Note: callback not supported by QwenImageEditPipeline
            )
        
        editing_time = time.time() - start_time
        self.console.print(f"✅ Edited in {editing_time:.1f} seconds")
        
        return result.images[0]
    
    def save_image(
        self,
        image: Image.Image,
        filename: Optional[str] = None,
        output_dir: Optional[Path] = None,
    ) -> Path:
        """Save image with intelligent naming and organization."""
        
        output_dir = output_dir or self.config.output_config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qwen_image_{timestamp}.png"
        
        # Ensure proper extension
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filename += '.png'
        
        output_path = output_dir / filename
        
        # Save with optimal settings
        if output_path.suffix.lower() == '.png':
            image.save(output_path, "PNG", optimize=True)
        else:
            image.save(output_path, "JPEG", quality=self.config.output_config.quality, optimize=True)
        
        return output_path
    
    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status and system information."""
        return {
            "system": {
                "chip": self.config.system_info.chip,
                "memory_gb": self.config.system_info.memory_gb,
                "has_mps": self.config.system_info.has_mps,
                "torch_version": self.config.system_info.torch_version,
            },
            "device": {
                "device": str(self._device),
                "dtype": str(self._dtype),
            },
            "pipelines": {
                "pipeline_loaded": self.pipeline is not None,
                "model": "Qwen/Qwen-Image-Edit",
            },
            "config": {
                "use_lightning": self.config.model_config.use_lightning,
                "lightning_steps": self.config.model_config.lightning_steps,
                "output_dir": str(self.config.output_config.output_dir),
            }
        }
