"""
Configuration management for Qwen Image Edit macOS.
"""

import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dataclasses import dataclass, asdict


@dataclass
class SystemInfo:
    """System information for optimal configuration."""
    
    platform: str
    chip: str
    memory_gb: int
    python_version: str
    has_mps: bool
    torch_version: Optional[str] = None


@dataclass 
class ModelConfig:
    """Model configuration settings."""
    
    cache_dir: Path
    use_lightning: bool = True
    lightning_steps: int = 4
    default_steps: int = 50
    default_cfg_scale: float = 4.0
    lightning_cfg_scale: float = 1.0
    
    
@dataclass
class OutputConfig:
    """Output configuration settings."""
    
    output_dir: Path
    default_size: tuple = (1664, 928)  # 16:9 aspect ratio
    save_format: str = "PNG"
    quality: int = 95


class Config:
    """Intelligent configuration management for macOS users."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".qwen-image-edit" / "config.yaml"
        self.config_dir = self.config_path.parent
        self.system_info = self._detect_system()
        
        # Initialize with intelligent defaults
        self._setup_directories()
        self.model_config = self._get_model_config()
        self.output_config = self._get_output_config()
        
        # Load or create user config
        self._load_or_create_config()
    
    def _detect_system(self) -> SystemInfo:
        """Detect system capabilities for optimal defaults."""
        # Get chip information
        chip = "Unknown"
        memory_gb = 8  # Conservative default
        
        if platform.system() == "Darwin":  # macOS
            try:
                # Get chip info
                chip_info = subprocess.run(
                    ["system_profiler", "SPHardwareDataType"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                for line in chip_info.stdout.split('\n'):
                    if "Chip:" in line:
                        chip = line.split(":")[-1].strip()
                    elif "Memory:" in line:
                        memory_str = line.split(":")[-1].strip()
                        # Extract GB amount (e.g., "128 GB" -> 128)
                        memory_gb = int(memory_str.split()[0])
                        break
            except (subprocess.TimeoutExpired, subprocess.SubprocessError, ValueError):
                pass
        
        # Check PyTorch MPS availability
        has_mps = False
        torch_version = None
        try:
            import torch
            has_mps = torch.backends.mps.is_available()
            torch_version = torch.__version__
        except ImportError:
            pass
        
        return SystemInfo(
            platform=platform.system(),
            chip=chip,
            memory_gb=memory_gb,
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}",
            has_mps=has_mps,
            torch_version=torch_version
        )
    
    def _setup_directories(self) -> None:
        """Create necessary directories."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Create standard directories
        for dir_name in ["outputs", "models", "cache"]:
            (self.config_dir / dir_name).mkdir(exist_ok=True)
    
    def _get_model_config(self) -> ModelConfig:
        """Get model configuration based on system capabilities."""
        cache_dir = self.config_dir / "cache"
        
        # Adjust defaults based on system memory
        if self.system_info.memory_gb >= 64:
            # High-memory system: can use higher quality defaults
            return ModelConfig(
                cache_dir=cache_dir,
                use_lightning=True,
                lightning_steps=4,
                default_steps=50,
            )
        elif self.system_info.memory_gb >= 32:
            # Medium-memory system: balanced defaults
            return ModelConfig(
                cache_dir=cache_dir,
                use_lightning=True,
                lightning_steps=4,
                default_steps=30,
            )
        else:
            # Lower-memory system: prioritize speed
            return ModelConfig(
                cache_dir=cache_dir,
                use_lightning=True,
                lightning_steps=4,
                default_steps=20,
            )
    
    def _get_output_config(self) -> OutputConfig:
        """Get output configuration."""
        return OutputConfig(
            output_dir=self.config_dir / "outputs",
        )
    
    def _load_or_create_config(self) -> None:
        """Load existing config or create new one with intelligent defaults."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                self._merge_user_config(user_config)
            except Exception:
                # If config is corrupted, recreate it
                self._create_default_config()
        else:
            self._create_default_config()
    
    def _merge_user_config(self, user_config: Dict[str, Any]) -> None:
        """Merge user configuration with defaults."""
        # Update model config
        if "model" in user_config:
            for key, value in user_config["model"].items():
                if hasattr(self.model_config, key):
                    setattr(self.model_config, key, value)
        
        # Update output config  
        if "output" in user_config:
            for key, value in user_config["output"].items():
                if hasattr(self.output_config, key):
                    if key == "output_dir":
                        setattr(self.output_config, key, Path(value))
                    else:
                        setattr(self.output_config, key, value)
    
    def _create_default_config(self) -> None:
        """Create default configuration file."""
        config_data = {
            "system_info": asdict(self.system_info),
            "model": asdict(self.model_config),
            "output": asdict(self.output_config),
            "version": "1.0.0"
        }
        
        # Convert Path objects to strings for YAML serialization
        config_data["model"]["cache_dir"] = str(config_data["model"]["cache_dir"])
        config_data["output"]["output_dir"] = str(config_data["output"]["output_dir"])
        
        # Ensure all values are YAML serializable
        if "torch_version" in config_data["system_info"]:
            config_data["system_info"]["torch_version"] = str(config_data["system_info"]["torch_version"]) if config_data["system_info"]["torch_version"] else None
        
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(config_data, f, default_flow_style=False, sort_keys=False)
    
    def save(self) -> None:
        """Save current configuration."""
        self._create_default_config()
    
    def get_recommended_settings(self) -> Dict[str, Any]:
        """Get recommended settings based on system capabilities."""
        recommendations = {
            "use_lightning": True,
            "steps": self.model_config.lightning_steps if self.model_config.use_lightning else self.model_config.default_steps,
        }
        
        # Add memory-based recommendations
        if self.system_info.memory_gb >= 64:
            recommendations["quality_preset"] = "maximum"
            recommendations["batch_size"] = 1
        elif self.system_info.memory_gb >= 32:
            recommendations["quality_preset"] = "high" 
            recommendations["batch_size"] = 1
        else:
            recommendations["quality_preset"] = "balanced"
            recommendations["batch_size"] = 1
        
        return recommendations
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"""Qwen Image Edit Configuration
System: {self.system_info.chip} with {self.system_info.memory_gb}GB RAM
PyTorch MPS: {'Available' if self.system_info.has_mps else 'Not Available'}
Output Directory: {self.output_config.output_dir}
Cache Directory: {self.model_config.cache_dir}"""
