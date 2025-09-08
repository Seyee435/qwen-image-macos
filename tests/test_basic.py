"""
Basic tests for Qwen Image Edit macOS package.
"""

import pytest
from pathlib import Path
import tempfile
import platform

from qwen_image_edit.core.config import Config, SystemInfo
from qwen_image_edit.core.pipeline import QwenImagePipeline


class TestConfig:
    """Test configuration management."""
    
    def test_system_detection(self):
        """Test that system detection works."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config = Config(config_path)
            
            # Basic system info should be detected
            assert config.system_info.platform == platform.system()
            assert config.system_info.memory_gb > 0
            assert config.system_info.python_version is not None
            
            # On macOS, should detect chip information
            if platform.system() == "Darwin":
                assert "Apple" in config.system_info.chip or config.system_info.chip == "Unknown"
    
    def test_config_creation(self):
        """Test that configuration files are created properly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config = Config(config_path)
            
            # Config file should be created
            assert config.config_path.exists()
            
            # Directories should be created
            assert config.config_dir.exists()
            assert (config.config_dir / "outputs").exists()
            assert (config.config_dir / "cache").exists()
    
    def test_memory_based_defaults(self):
        """Test that defaults are adjusted based on memory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config = Config(config_path)
            
            # Should have reasonable defaults
            assert config.model_config.lightning_steps in [4, 8]
            assert config.model_config.default_steps > 0
            assert config.output_config.default_size == (1664, 928)


class TestPipeline:
    """Test pipeline functionality (without actual model loading)."""
    
    def test_pipeline_creation(self):
        """Test that pipeline can be created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"
            config = Config(config_path)
            
            # Should be able to create pipeline without errors
            pipeline = QwenImagePipeline(config)
            
            # Device should be set
            assert pipeline._device is not None
            assert pipeline._dtype is not None
    
    def test_status_info(self):
        """Test that status information is available."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.yaml"  
            config = Config(config_path)
            pipeline = QwenImagePipeline(config)
            
            status = pipeline.get_status()
            
            # Should contain expected keys
            assert "system" in status
            assert "device" in status
            assert "pipelines" in status
            assert "config" in status
            
            # System info should be populated
            assert "chip" in status["system"]
            assert "memory_gb" in status["system"]


class TestCLI:
    """Test CLI functionality."""
    
    def test_cli_imports(self):
        """Test that CLI can be imported."""
        from qwen_image_edit.cli.main import cli
        assert cli is not None
