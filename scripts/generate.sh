#!/bin/bash

# Qwen Image Generation Script
# Usage: ./generate.sh "your prompt here" [steps] [mode]
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

# Default values
PROMPT="${1:-A beautiful sunset over mountains with reflections in water, ultra detailed, cinematic}"
STEPS="${2:-20}"
MODE="${3:-ultra-fast}"

echo "🎨 Generating image with Qwen..."
echo "📝 Prompt: $PROMPT"
echo "⚡ Mode: $MODE"
echo "🔢 Steps: $STEPS"

cd /Users/zsakib/Documents/qwen-image-edit/outputs

case $MODE in
    "ultra-fast"|"uf")
        qwen-image-mps generate -p "$PROMPT" -s "$STEPS" --ultra-fast
        ;;
    "fast"|"f")
        qwen-image-mps generate -p "$PROMPT" -s "$STEPS" --fast
        ;;
    "normal"|"n")
        qwen-image-mps generate -p "$PROMPT" -s "$STEPS"
        ;;
    *)
        echo "❌ Invalid mode. Use: normal, fast, or ultra-fast"
        exit 1
        ;;
esac

echo "✅ Image generation complete!"
echo "📁 Check: $(pwd)/output/"
