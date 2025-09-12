from typing import List, Optional, Tuple
from pathlib import Path as SysPath
import secrets

from cog import BasePredictor, Input, Path
import torch


ASPECTS = {
    "1:1": (1328, 1328),
    "16:9": (1664, 928),
    "9:16": (928, 1664),
    "4:3": (1472, 1104),
    "3:4": (1104, 1472),
    "3:2": (1584, 1056),
    "2:3": (1056, 1584),
}


def pick_device_and_dtype() -> Tuple[str, torch.dtype]:
    if torch.cuda.is_available():
        return "cuda", torch.bfloat16
    # Docker on macOS won’t have MPS; CPU fallback
    return "cpu", torch.float32


def maybe_load_lightning_lora(pipe, mode: Optional[str]) -> Optional[str]:
    """
    mode: None | "fast" (8 steps) | "ultra" (4 steps)
    Returns a short description if loaded, else None.
    """
    if mode is None:
        return None
    repo_id = "lightx2v/Qwen-Image-Lightning"
    files = {
        "fast": "Qwen-Image-Lightning-8steps-V1.1-bf16.safetensors",
        "ultra": "Qwen-Image-Lightning-4steps-V1.0-bf16.safetensors",
    }
    fname = files.get(mode)
    if not fname:
        return None
    try:
        pipe.load_lora_weights(repo_id, weight_name=fname)
        try:
            pipe.fuse_lora()
        except Exception:
            pass
        return f"Lightning LoRA loaded ({mode})"
    except Exception:
        return None


class Predictor(BasePredictor):
    def setup(self) -> None:
        from diffusers import QwenImagePipeline

        device, dtype = pick_device_and_dtype()
        self.device = device
        self.dtype = dtype

        # Large download on first run (57+ GB)
        self.pipe = QwenImagePipeline.from_pretrained(
            "Qwen/Qwen-Image",
            dtype=dtype,
        ).to(device)

        try:
            self.pipe.enable_attention_slicing()
        except Exception:
            pass
        try:
            self.pipe.enable_vae_tiling()
        except Exception:
            pass

    def predict(
        self,
        prompt: str = Input(
            description="Text prompt for generation",
            default="A cinematic photo of a corgi in sunglasses",
        ),
        steps: int = Input(
            description="Number of inference steps (ignored if fast/ultra-fast)",
            ge=1,
            le=100,
            default=20,
        ),
        fast: bool = Input(
            description="Use Lightning LoRA 8-step mode",
            default=False,
        ),
        ultra_fast: bool = Input(
            description="Use Lightning LoRA 4-step mode",
            default=False,
        ),
        negative_prompt: str = Input(
            description="Negative prompt to discourage artifacts",
            default="",
        ),
        aspect: str = Input(
            description="Aspect ratio",
            choices=list(ASPECTS.keys()),
            default="16:9",
        ),
        num_images: int = Input(
            description="Number of images to generate",
            ge=1,
            le=8,
            default=1,
        ),
        seed: Optional[int] = Input(
            description="Random seed (fixed). If not set, a new random seed per image.",
            default=None,
        ),
        cfg_scale: Optional[float] = Input(
            description="CFG scale. Defaults: 4.0 normal; 1.0 fast/ultra-fast",
            default=None,
        ),
        width: Optional[int] = Input(
            description="Override width (pixels). If set with height, ignores aspect.",
            default=None,
        ),
        height: Optional[int] = Input(
            description="Override height (pixels). If set with width, ignores aspect.",
            default=None,
        ),
    ) -> List[Path]:
        # LoRA mode
        lora_mode = "ultra" if ultra_fast else ("fast" if fast else None)

        msg = maybe_load_lightning_lora(self.pipe, lora_mode)
        if msg:
            print(msg)

        if lora_mode == "ultra":
            num_steps = 4
            cfg = 1.0
        elif lora_mode == "fast":
            num_steps = 8
            cfg = 1.0
        else:
            num_steps = steps
            cfg = 4.0

        if cfg_scale is not None:
            try:
                cfg = float(cfg_scale)
            except Exception:
                pass

        if width is not None and height is not None and width > 0 and height > 0:
            w, h = int(width), int(height)
        else:
            w, h = ASPECTS[aspect]
        out_dir = SysPath("/tmp/outputs")
        out_dir.mkdir(parents=True, exist_ok=True)

        paths: List[Path] = []
        for i in range(max(1, int(num_images))):
            per_seed = seed if seed is not None else secrets.randbits(63)
            gen_device = "cpu" if self.device == "mps" else self.device
            g = torch.Generator(device=gen_device).manual_seed(int(per_seed))

            print(f"[{i+1}/{num_images}] steps={num_steps} cfg={cfg} seed={per_seed} {w}x{h}")
            result = self.pipe(
                prompt=prompt,
                negative_prompt=(negative_prompt or " "),
                num_inference_steps=num_steps,
                true_cfg_scale=cfg,
                width=w,
                height=h,
                generator=g,
            )
            image = result.images[0]

            outfile = out_dir / f"image_{per_seed}_{i+1}.png"
            image.save(outfile)
            paths.append(Path(str(outfile)))

        return paths
