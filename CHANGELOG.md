# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-08

### Added
- 🎉 **Initial release** of Qwen Image Edit for macOS
- 🎨 **Professional CLI interface** with `qwen-image` command
- 🧠 **Intelligent system detection** for Apple Silicon Macs
- ⚡ **Lightning LoRA support** for 4-step ultra-fast generation
- 🔧 **Smart configuration system** with automatic optimization
- 📊 **System status** command with hardware information
- 🖼️ **Image generation** from text prompts
- ✏️ **Image editing** with text instructions
- 📝 **Example generation** for testing installation
- 🔍 **Progress indicators** with Rich-based UI
- 🏗️ **Modern Python package** structure with pyproject.toml
- 🧪 **Test suite** for code quality assurance

### Features
- **Apple Silicon Optimization**: Automatically detects M-series chips and uses MPS acceleration
- **Memory-Based Defaults**: Adjusts settings based on your Mac's memory (8GB/16GB/32GB/64GB+)
- **One-Command Setup**: Simple `python install.py` gets everything working
- **Beautiful CLI**: Rich formatting, progress bars, and helpful error messages
- **Intelligent Configuration**: Saves preferences and remembers optimal settings
- **World-Class Documentation**: Comprehensive README, contributing guide, and examples

### Performance
- **Generation Speed**: ~45-60 seconds for ultra-fast mode (4 steps) on Apple Silicon
- **Model Support**: Full Qwen Image Edit model with Lightning LoRA acceleration
- **Memory Efficient**: Optimized for various Mac configurations
- **MPS Acceleration**: Takes full advantage of Apple's Metal Performance Shaders

### Developer Experience
- **Modern Tooling**: Click CLI, Rich UI, proper Python packaging
- **Type Hints**: Full type annotation throughout codebase
- **Testing**: Basic test suite with pytest
- **Code Quality**: Black formatting, clean architecture
- **Documentation**: Docstrings, README, contributing guidelines

### Commands
- `qwen-image status` - Show system information and recommendations
- `qwen-image generate` - Generate images from text prompts
- `qwen-image edit` - Edit existing images with text instructions
- `qwen-image examples` - Generate example images for testing
- `qwen-image config` - Manage configuration settings

### Supported Systems
- **macOS**: Primary target (all versions)
- **Apple Silicon**: M1, M2, M3, M4 chips (recommended)
- **Intel Macs**: Supported but slower
- **Python**: 3.10+ required
- **Memory**: 16GB+ recommended

### Dependencies
- PyTorch 2.0+ with MPS support
- Diffusers 0.35.0+ for pipeline management
- Transformers 4.35.0+ for model loading
- Rich 13.0+ for beautiful CLI interface
- Click 8.0+ for command-line interface
- And other carefully selected dependencies

---

## Future Releases

### Planned for 1.1.0
- [ ] **Batch processing** support
- [ ] **Additional image formats** (WEBP, TIFF)
- [ ] **Memory usage optimizations** for lower-end Macs
- [ ] **Integration tests** with actual model loading

### Planned for 1.2.0
- [ ] **GUI interface** (optional)
- [ ] **Plugin system** for custom workflows
- [ ] **Advanced configuration** options
- [ ] **Performance benchmarking** tools

### Long-term Goals
- [ ] **GGUF model support** integration
- [ ] **ComfyUI integration** option
- [ ] **Cloud integration** for heavier models
- [ ] **Mobile app** for remote generation

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE) for details.
