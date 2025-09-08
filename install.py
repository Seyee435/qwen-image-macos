#!/usr/bin/env python3
"""
Simple installation script for Qwen Image Edit macOS.
This script helps users install the package with proper dependency management.
"""

import sys
import subprocess
import platform
from pathlib import Path


def print_status(message: str, status: str = "info"):
    """Print status message with appropriate formatting."""
    symbols = {
        "info": "🔍",
        "success": "✅", 
        "error": "❌",
        "warning": "⚠️"
    }
    symbol = symbols.get(status, "ℹ️")
    print(f"{symbol} {message}")


def check_system():
    """Check basic system requirements."""
    print_status("Checking system requirements...")
    
    # Check macOS
    if platform.system() != "Darwin":
        print_status("This package is designed for macOS", "warning")
        print("  It may work on other systems but performance will be limited")
        
    # Check Python version
    if sys.version_info < (3, 10):
        print_status(f"Python 3.10+ required, found {sys.version_info.major}.{sys.version_info.minor}", "error")
        print("  Please upgrade Python: brew install python@3.11")
        return False
        
    print_status(f"Python {sys.version.split()[0]} detected", "success")
    return True


def install_package():
    """Install the package using pip."""
    print_status("Installing Qwen Image Edit macOS package...")
    
    try:
        # Install with pip
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], check=True, capture_output=True, text=True)
        
        print_status("Package installed successfully!", "success")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status("Installation failed", "error")
        print(f"Error: {e.stderr}")
        print("\nTroubleshooting:")
        print("  1. Make sure you're in a virtual environment")
        print("  2. Try: pip install --upgrade pip")
        print("  3. Try: conda create -n qwen-image python=3.11 && conda activate qwen-image")
        return False


def test_installation():
    """Test that the package was installed correctly."""
    print_status("Testing installation...")
    
    try:
        # Test basic import
        import qwen_image_edit
        print_status(f"Package version {qwen_image_edit.__version__} imported successfully", "success")
        
        # Test CLI
        result = subprocess.run([
            sys.executable, "-c", "from qwen_image_edit.cli.main import main; print('CLI works')"
        ], check=True, capture_output=True, text=True)
        
        print_status("CLI interface is working", "success")
        return True
        
    except Exception as e:
        print_status(f"Test failed: {e}", "error")
        return False


def show_next_steps():
    """Show what to do next."""
    print("\n🎉 Installation Complete!")
    print("\nNext steps:")
    print("  1. Check your system: qwen-image status")  
    print("  2. Generate an image: qwen-image generate -p 'A beautiful landscape'")
    print("  3. Get help: qwen-image --help")
    print("\n📚 Documentation: README.md")
    print("🐛 Issues: https://github.com/yourusername/qwen-image-edit-macos/issues")


def main():
    """Main installation function."""
    print("🎨 Qwen Image Edit for macOS - Installation")
    print("==========================================\n")
    
    if not check_system():
        sys.exit(1)
    
    if not install_package():
        sys.exit(1)
        
    if not test_installation():
        print_status("Package installed but tests failed", "warning")
        print("You may still be able to use the package")
    
    show_next_steps()


if __name__ == "__main__":
    main()
