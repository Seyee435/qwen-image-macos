"""
Qwen Image Edit for macOS - Professional image generation and editing with Apple Silicon optimization.
"""

__version__ = "1.0.0"
__author__ = "Qwen Image Edit macOS Team"
__description__ = "Professional image generation and editing with Qwen Image Edit, optimized for Apple Silicon"

from .core.pipeline import QwenImagePipeline
from .core.config import Config

__all__ = ["QwenImagePipeline", "Config", "__version__"]
