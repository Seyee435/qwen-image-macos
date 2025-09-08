#!/bin/bash

# Qwen Image Editing Script
# Usage: ./edit.sh "path/to/image.png" "editing prompt" [mode]
# Mode: normal, fast, ultra-fast

set -e

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Error: conda is not available"
    exit 1
fi

# Source conda and activate environment
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
conda activate qwen-image

# Check arguments
if [ $# -lt 2 ]; then
    echo "❌ Usage: $0 \"path/to/image.png\" \"editing prompt\" [mode]"
    echo "   Mode options: normal, fast, ultra-fast (default: ultra-fast)"
    exit 1
fi

IMAGE_PATH="$1"
PROMPT="$2"
MODE="${3:-ultra-fast}"

# Check if image exists
if [ ! -f "$IMAGE_PATH" ]; then
    echo "❌ Error: Image file '$IMAGE_PATH' not found"
    exit 1
fi

echo "✏️ Editing image with Qwen..."
echo "🖼️ Input: $IMAGE_PATH"
echo "📝 Edit prompt: $PROMPT"
echo "⚡ Mode: $MODE"

cd /Users/zsakib/Documents/qwen-image-edit/outputs

case $MODE in
    "ultra-fast"|"uf")
        qwen-image-mps edit -i "$IMAGE_PATH" -p "$PROMPT" --ultra-fast
        ;;
    "fast"|"f")
        qwen-image-mps edit -i "$IMAGE_PATH" -p "$PROMPT" --fast
        ;;
    "normal"|"n")
        qwen-image-mps edit -i "$IMAGE_PATH" -p "$PROMPT"
        ;;
    *)
        echo "❌ Invalid mode. Use: normal, fast, or ultra-fast"
        exit 1
        ;;
esac

echo "✅ Image editing complete!"
echo "📁 Check: $(pwd)/output/"
