#!/usr/bin/env python3
"""
Quick test to make sure everything works before going viral
"""

import subprocess
import sys
import time
from pathlib import Path

def run_cmd(cmd):
    """Run command and return success, time, output"""
    start = time.time()
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        elapsed = time.time() - start
        return result.returncode == 0, elapsed, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, 300, "", "Timeout"

def main():
    print("🧪 Final Test - Making sure everything works for Hacker News")
    print("=" * 60)
    
    # Test 1: Basic CLI
    print("1. Testing basic CLI...")
    success, _, output, _ = run_cmd("python qwen.py --help")
    if success and "Qwen Image" in output:
        print("   ✅ CLI works")
    else:
        print("   ❌ CLI broken")
        return False
    
    # Test 2: Status check
    print("2. Checking Apple Silicon...")
    success, _, output, _ = run_cmd("python qwen.py status")
    if success and ("mps" in output.lower() or "apple silicon" in output.lower()):
        print("   ✅ Apple Silicon GPU detected")
    else:
        print("   ⚠️ No Apple Silicon GPU (will use CPU)")
    
    # Test 3: Quick generation
    print("3. Testing image generation (30s timeout)...")
    success, elapsed, output, error = run_cmd("python qwen.py generate 'a red dot' --steps 4 --size 256x256")
    if success:
        print(f"   ✅ Generated image in {elapsed:.1f}s")
    else:
        print(f"   ❌ Generation failed: {error}")
        return False
    
    # Test 4: Error handling
    print("4. Testing error handling...")
    success, _, output, _ = run_cmd("python qwen.py edit '/fake/image.jpg' 'test'")
    if not success and "not found" in output.lower():
        print("   ✅ Proper error handling")
    else:
        print("   ❌ Error handling broken")
        return False
    
    # Test 5: Check output directory
    print("5. Checking output...")
    output_dir = Path.home() / "qwen-images"
    if output_dir.exists():
        images = list(output_dir.glob("*.png"))
        print(f"   ✅ Found {len(images)} generated images")
    else:
        print("   ❌ No output directory")
        return False
    
    print("=" * 60)
    print("🎉 ALL TESTS PASSED! Ready for Hacker News!")
    print(f"📁 Generated images: {output_dir}")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
