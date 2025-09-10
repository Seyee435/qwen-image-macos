# Fast Qwen Image Edit on macOS using GGUF (ComfyUI)

This project ships a tiny, optional integration path to run Qwen-Image-Edit in minutes on Apple Silicon using GGUF quantized weights via ComfyUI.

Why
- Diffusers + MPS is compute-bound for Qwen-Image-Edit (20B) and can be very slow for edits.
- The community GGUF route (ComfyUI-GGUF) trades a little quality for big speed/VRAM wins, and supports Lightning 4/8-step workflows.

What this adds
- scripts/setup_gguf.sh sets up ComfyUI + ComfyUI-GGUF and downloads Q4_0 (~12GB) UNet + VAE + text-encoder/mmproj into ComfyUI/models/.
- You run ComfyUI locally, then either:
  - Use ComfyUI’s web UI to load a prepared workflow (recommended first run), or
  - Use the API to submit a JSON workflow (advanced).

Quick start (10–15 min)
1) Run the setup (downloads models and starts ComfyUI):

```bash
bash scripts/setup_gguf.sh
```

This will:
- Clone ComfyUI into external/ComfyUI
- Install ComfyUI-GGUF custom node
- Download models under external/ComfyUI/models/
- Start ComfyUI at http://127.0.0.1:8188

2) Open ComfyUI in your browser and import a Qwen-Image-Edit GGUF workflow.
- Use a workflow from the community (e.g. ComfyUI-GGUF README or Qwen-Image-Edit-Fast space)
- Make sure loaders are set to:
  - UNet: Qwen_Image_Edit-Q4_0.gguf (or your selected quant)
  - VAE: Qwen_Image-VAE.safetensors
  - Text encoder: Qwen2.5-VL-7B.gguf
  - mmproj: Qwen2.5-VL-7B-Instruct-mmproj-BF16.gguf
- For speed, start with 4 or 8 steps and CFG ~1.0–2.0.

3) Try the included example:
- Drop example.webp into the workflow’s image input
- Prompt: "make the dog look like a superhero, cape, cinematic lighting"
- Run. You should see output within a couple minutes on M3 Max for 4–8 steps.

Notes
- You can switch to Q3/Q2 quant if your Mac has 16GB RAM and you need smaller weights. Higher-bit (Q5/Q6/Q8) may improve quality but will be slower/heavier.
- Lightning LoRA 4/8 step setups exist in ComfyUI workflows; ensure you’re using the normal CLIP loader (not GGUF CLIP) when required by the workflow.
- This path keeps the main CLI lean: diffusers-based generate/edit remain available. GGUF is optional and isolated.

Troubleshooting
- ComfyUI doesn’t start or UI errors:
  - Activate the venv: `source external/.venv/bin/activate` and run `pip install -r requirements.txt` inside ComfyUI if prompted.
- Model not found inside nodes:
  - Verify files exist under external/ComfyUI/models/{unet,vae,text_encoders}.
- Too slow or OOM:
  - Try Q3_K_M or Q2_K, reduce steps to 4–8, set CFG ≈ 1.0–2.0, keep input at 512×512.

Next
- If there’s strong interest, we can add a tiny script to POST a prepared workflow to ComfyUI’s /prompt API for fully headless runs. For now, the web UI is the fastest path to reliable edits.

