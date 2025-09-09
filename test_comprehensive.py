#!/usr/bin/env python3
"""
Comprehensive test suite for Qwen Image macOS

Tests all functionality including edge cases, performance,
and Apple Silicon integration.
"""

import time
import torch
import subprocess
import sys
from pathlib import Path
from PIL import Image
import tempfile
import platform


def test_device_setup():
    """Test that MPS/Apple Silicon is properly detected."""
    print("🧪 Testing device setup...")
    
    print(f"Platform: {platform.platform()}")
    print(f"Machine: {platform.machine()}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"MPS available: {torch.backends.mps.is_available()}")
    print(f"MPS built: {torch.backends.mps.is_built()}")
    
    if torch.backends.mps.is_available():
        print("✅ Apple Silicon GPU ready")
        # Test actual MPS operations
        try:
            device = torch.device("mps")
            x = torch.randn(1000, 1000, device=device, dtype=torch.bfloat16)
            y = torch.mm(x, x)
            print("✅ MPS tensor operations working")
        except Exception as e:
            print(f"❌ MPS operations failed: {e}")
            return False
    else:
        print("⚠️ MPS not available - will use CPU")
    
    return True


def test_qwen_cli_basic():
    """Test basic CLI functionality."""
    print("\n🧪 Testing Qwen CLI basic functionality...")
    
    # Test help
    try:
        result = subprocess.run([sys.executable, "qwen.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "Qwen Image" in result.stdout:
            print("✅ CLI help working")
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False
    
    # Test status command
    try:
        result = subprocess.run([sys.executable, "qwen.py", "status"],
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Status command working")
            print(f"   Output preview: {result.stdout[:100]}...")
        else:
            print(f"❌ Status command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Status test failed: {e}")
        return False
    
    return True


def test_image_generation():
    """Test text-to-image generation."""
    print("\n🧪 Testing image generation...")
    
    test_prompts = [
        "a simple red circle on white background",
        "a cute cat sitting on a windowsill",  
        "abstract geometric shapes in blue and yellow"
    ]
    
    output_dir = Path.home() / "qwen-images" / "tests"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, prompt in enumerate(test_prompts):
        print(f"   Testing prompt {i+1}/{len(test_prompts)}: {prompt[:40]}...")
        
        try:
            start_time = time.time()
            
            # Test with lightning mode for speed
            result = subprocess.run([
                sys.executable, "qwen.py", "generate", prompt,
                "--steps", "4",
                "--size", "512x512",
                "-o", f"test_gen_{i+1}.png"
            ], capture_output=True, text=True, timeout=300)
            
            generation_time = time.time() - start_time
            
            if result.returncode == 0:
                # Check if image was created
                expected_path = Path.home() / "qwen-images" / f"test_gen_{i+1}.png"
                if expected_path.exists():
                    # Verify it's a valid image
                    try:
                        img = Image.open(expected_path)
                        width, height = img.size
                        print(f"   ✅ Generated {width}x{height} image in {generation_time:.1f}s")
                    except Exception as e:
                        print(f"   ❌ Invalid image file: {e}")
                        return False
                else:
                    print(f"   ❌ Expected image file not found: {expected_path}")
                    return False
            else:
                print(f"   ❌ Generation failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ Generation timed out after 300s")
            return False
        except Exception as e:
            print(f"   ❌ Generation test failed: {e}")
            return False
    
    print("✅ All generation tests passed")
    return True


def test_image_editing():
    """Test image editing functionality."""
    print("\n🧪 Testing image editing...")
    
    # First create a test image to edit
    test_image_path = Path.home() / "qwen-images" / "test_base.png"
    
    # Create a simple test image if it doesn't exist
    if not test_image_path.exists():
        print("   Creating test image for editing...")
        try:
            result = subprocess.run([
                sys.executable, "qwen.py", "generate", 
                "a simple landscape with trees and sky",
                "--steps", "4",
                "--size", "512x512", 
                "-o", "test_base.png"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"   ❌ Failed to create test image: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ Test image creation failed: {e}")
            return False
    
    # Test editing prompts
    edit_prompts = [
        "make it winter with snow",
        "change to sunset lighting",
        "add birds flying in the sky"
    ]
    
    for i, edit_prompt in enumerate(edit_prompts):
        print(f"   Testing edit {i+1}/{len(edit_prompts)}: {edit_prompt}")
        
        try:
            start_time = time.time()
            
            result = subprocess.run([
                sys.executable, "qwen.py", "edit",
                str(test_image_path),
                edit_prompt,
                "--steps", "4",
                "-o", f"test_edit_{i+1}.png"
            ], capture_output=True, text=True, timeout=600)
            
            edit_time = time.time() - start_time
            
            if result.returncode == 0:
                expected_path = Path.home() / "qwen-images" / f"test_edit_{i+1}.png"
                if expected_path.exists():
                    try:
                        img = Image.open(expected_path)
                        width, height = img.size
                        print(f"   ✅ Edited to {width}x{height} in {edit_time:.1f}s")
                    except Exception as e:
                        print(f"   ❌ Invalid edited image: {e}")
                        return False
                else:
                    print(f"   ❌ Expected edited image not found")
                    return False
            else:
                print(f"   ❌ Editing failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ❌ Editing timed out after 600s")
            return False
        except Exception as e:
            print(f"   ❌ Editing test failed: {e}")
            return False
    
    print("✅ All editing tests passed")
    return True


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n🧪 Testing edge cases...")
    
    # Test with non-existent image file
    print("   Testing non-existent image file...")
    result = subprocess.run([
        sys.executable, "qwen.py", "edit",
        "/nonexistent/file.jpg", 
        "test prompt"
    ], capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0 and "not found" in result.stdout.lower():
        print("   ✅ Correctly handles non-existent files")
    else:
        print("   ❌ Should fail gracefully with non-existent files")
        return False
    
    # Test with very short prompts
    print("   Testing minimal prompts...")
    try:
        result = subprocess.run([
            sys.executable, "qwen.py", "generate", "cat",
            "--steps", "4", "--size", "256x256"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("   ✅ Handles minimal prompts")
        else:
            print(f"   ❌ Failed with minimal prompt: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Minimal prompt test failed: {e}")
        return False
    
    # Test drag-and-drop path handling
    print("   Testing drag-and-drop path handling...")
    
    # Create a test image with spaces in the name
    test_image_with_spaces = Path.home() / "qwen-images" / "test with spaces.png"
    if not test_image_with_spaces.exists():
        # Create it
        try:
            Image.new('RGB', (100, 100), color='red').save(test_image_with_spaces)
        except Exception as e:
            print(f"   ❌ Could not create test image: {e}")
            return False
    
    # Test with quoted path (simulating drag-and-drop)
    quoted_path = f'"{test_image_with_spaces}"'
    result = subprocess.run([
        sys.executable, "qwen.py", "edit",
        quoted_path,
        "make it blue", 
        "--steps", "4"
    ], capture_output=True, text=True, timeout=300)
    
    if result.returncode == 0:
        print("   ✅ Handles quoted paths with spaces")
    else:
        print(f"   ❌ Failed with quoted paths: {result.stderr}")
        return False
    
    print("✅ All edge case tests passed")
    return True


def test_performance_benchmarks():
    """Test performance benchmarks."""
    print("\n🧪 Running performance benchmarks...")
    
    # Benchmark generation speed
    print("   Benchmarking generation (Lightning mode)...")
    start_time = time.time()
    
    result = subprocess.run([
        sys.executable, "qwen.py", "generate",
        "performance test image",
        "--steps", "4",
        "--size", "512x512"
    ], capture_output=True, text=True, timeout=300)
    
    gen_time = time.time() - start_time
    
    if result.returncode == 0:
        print(f"   ✅ Generation benchmark: {gen_time:.1f}s (512x512, 4 steps)")
        
        # Analyze if performance is reasonable
        if gen_time < 120:  # Should be under 2 minutes for 512x512 
            print("   ✅ Performance is good")
        else:
            print("   ⚠️ Performance slower than expected")
    else:
        print(f"   ❌ Benchmark failed: {result.stderr}")
        return False
    
    return True


def cleanup_test_files():
    """Clean up test files."""
    print("\n🧹 Cleaning up test files...")
    
    test_dir = Path.home() / "qwen-images"
    if test_dir.exists():
        test_files = [
            "test_gen_1.png", "test_gen_2.png", "test_gen_3.png",
            "test_edit_1.png", "test_edit_2.png", "test_edit_3.png", 
            "test_base.png", "test with spaces.png",
            "qwen_*.png"  # Any generated files
        ]
        
        cleaned = 0
        for pattern in test_files:
            if "*" in pattern:
                # Handle glob patterns
                for file in test_dir.glob(pattern):
                    if "test" in file.name.lower():  # Only clean test files
                        file.unlink(missing_ok=True)
                        cleaned += 1
            else:
                file_path = test_dir / pattern
                if file_path.exists():
                    file_path.unlink()
                    cleaned += 1
        
        print(f"   Cleaned up {cleaned} test files")


def main():
    """Run comprehensive test suite."""
    print("🎯 Qwen Image macOS - Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        ("Device Setup", test_device_setup),
        ("CLI Basic", test_qwen_cli_basic), 
        ("Image Generation", test_image_generation),
        ("Image Editing", test_image_editing),
        ("Edge Cases", test_edge_cases),
        ("Performance", test_performance_benchmarks),
    ]
    
    passed = 0
    failed = 0
    
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} CRASHED: {e}")
    
    total_time = time.time() - start_time
    
    # Cleanup
    cleanup_test_files()
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed} passed, {failed} failed")
    print(f"⏱️  Total time: {total_time:.1f} seconds")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Qwen Image is ready for production use.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
