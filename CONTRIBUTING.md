# Contributing to Qwen Image Edit for macOS

Thank you for your interest in contributing! This project aims to make AI image generation accessible to everyone on Apple Silicon Macs.

## 🌟 How to Contribute

### Reporting Issues
- **Bug Reports**: Use the issue template and include system info from `qwen-image status`
- **Feature Requests**: Describe the use case and how it would help Mac users
- **Documentation**: Help us improve clarity for ML newcomers

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/qwen-image-edit-macos.git
   cd qwen-image-edit-macos
   ```

2. **Environment Setup**
   ```bash
   # Option 1: Conda (Recommended)
   conda env create -f environment.yml
   conda activate qwen-image-edit

   # Option 2: Virtual Environment
   python -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   ```

3. **Verify Setup**
   ```bash
   python -m pytest tests/
   qwen-image status
   ```

### Code Standards

- **Python Style**: We use `black` for formatting, `flake8` for linting
- **Type Hints**: Add type annotations for new functions
- **Documentation**: Include docstrings for public APIs
- **Tests**: Add tests for new features

```bash
# Format code
black qwen_image_edit/

# Run linting
flake8 qwen_image_edit/

# Run tests
pytest tests/ -v
```

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Keep commits focused and atomic
   - Write clear commit messages
   - Update tests and documentation

3. **Test Thoroughly**
   ```bash
   pytest tests/
   qwen-image status
   qwen-image generate -p "test" --lightning
   ```

4. **Submit PR**
   - Fill out the PR template
   - Link related issues
   - Request review

## 🎯 Areas We Need Help

### High Priority
- **Performance optimization** for Apple Silicon
- **Memory usage improvements** for lower-end Macs
- **Better error messages** and recovery suggestions
- **Example workflows** and tutorials

### Medium Priority
- **Additional image formats** support
- **Batch processing** capabilities
- **Integration tests** with actual models
- **Documentation improvements**

### Low Priority
- **GUI interface** (optional)
- **Plugin system** for custom workflows
- **Advanced configuration** options

## 🧠 Design Philosophy

### For ML Newcomers
- **Simple by default**: Work out of the box with good defaults
- **Clear feedback**: Progress bars, helpful error messages
- **Educational**: Help users understand what's happening

### For Experienced Users
- **Configurable**: Allow customization when needed
- **Performant**: Optimize for Apple Silicon
- **Extensible**: Clean APIs for advanced use cases

### Code Quality
- **Readable**: Code should be self-documenting
- **Robust**: Handle edge cases gracefully
- **Testable**: Design for easy testing

## 📝 Commit Message Format

```
type(scope): brief description

Longer description if needed

- Specific change 1
- Specific change 2

Fixes #issue_number
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

**Examples**:
```
feat(cli): add batch generation support

Add --batch flag to generate command for processing multiple prompts.

- Support file input with one prompt per line
- Add progress tracking for batch operations
- Include example batch files

Fixes #42
```

## 🐛 Issue Templates

### Bug Report
```markdown
**System Info** (from `qwen-image status`):
- Chip: 
- Memory: 
- Python: 
- PyTorch: 

**Expected Behavior**:
What should happen?

**Actual Behavior**: 
What actually happened?

**Steps to Reproduce**:
1. Run `qwen-image ...`
2. See error

**Error Output**:
```
Paste full error output here
```
```

### Feature Request
```markdown
**Use Case**:
Describe who would use this and why.

**Proposed Solution**:
How should this work?

**Alternatives**:
Other ways to solve this?

**Additional Context**:
Screenshots, examples, etc.
```

## 🚀 Release Process

1. **Version Bump**: Update `__version__` in `__init__.py`
2. **Changelog**: Update CHANGELOG.md with new features
3. **Testing**: Run full test suite on multiple Mac configurations
4. **Tag Release**: `git tag v1.x.x && git push origin v1.x.x`
5. **GitHub Release**: Auto-publishes to PyPI

## ❓ Questions?

- **General Questions**: GitHub Discussions
- **Bugs**: GitHub Issues  
- **Security Issues**: Email maintainers privately

## 🙏 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

Thank you for making AI more accessible on Mac! 🎨
