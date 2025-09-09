#!/usr/bin/env python3
"""
Test script for drag-and-drop path validation functionality.

Tests the enhanced path handling that supports dragged files from Finder.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock
import click

# Import the validation function we created
from qwen_image_edit.cli.main import validate_image_path


class TestDragDropValidation:
    """Test drag-and-drop path validation functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary image file for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image = self.temp_dir / "test_image.jpg"
        self.test_image.write_text("fake image content")  # Create a fake file
        
        # Mock click context and parameter
        self.mock_ctx = Mock()
        self.mock_param = Mock()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        # Remove temporary files
        if self.test_image.exists():
            self.test_image.unlink()
        self.temp_dir.rmdir()
    
    def test_basic_path_validation(self):
        """Test basic path validation works."""
        result = validate_image_path(
            self.mock_ctx, 
            self.mock_param, 
            str(self.test_image)
        )
        # Compare resolved paths since validate_image_path calls .resolve()
        assert result == self.test_image.resolve()
    
    def test_quoted_path_handling(self):
        """Test handling of quoted paths (common with drag-and-drop)."""
        quoted_path = f'"{self.test_image}"'
        result = validate_image_path(
            self.mock_ctx,
            self.mock_param,
            quoted_path
        )
        assert result == self.test_image.resolve()
    
    def test_single_quoted_path(self):
        """Test handling of single-quoted paths."""
        quoted_path = f"'{self.test_image}'"
        result = validate_image_path(
            self.mock_ctx,
            self.mock_param,
            quoted_path
        )
        assert result == self.test_image.resolve()
    
    def test_path_with_spaces(self):
        """Test handling of paths with spaces."""
        # Create a file with spaces in the name
        spaced_image = self.temp_dir / "my vacation photo.jpg"
        spaced_image.write_text("fake content")
        
        try:
            result = validate_image_path(
                self.mock_ctx,
                self.mock_param,
                str(spaced_image)
            )
            assert result == spaced_image.resolve()
        finally:
            spaced_image.unlink()
    
    def test_escaped_spaces(self):
        """Test handling of escaped spaces in paths."""
        # Create a file with spaces
        spaced_image = self.temp_dir / "my photo.jpg"
        spaced_image.write_text("fake content")
        
        try:
            # Test with escaped spaces (common when dragging from terminal)
            escaped_path = str(spaced_image).replace(' ', '\\ ')
            result = validate_image_path(
                self.mock_ctx,
                self.mock_param,
                escaped_path
            )
            assert result == spaced_image.resolve()
        finally:
            spaced_image.unlink()
    
    def test_home_directory_expansion(self):
        """Test that ~ is properly expanded to home directory."""
        # This test uses a fake path since we can't guarantee ~/test.jpg exists
        fake_home_path = "~/test.jpg"
        expected_path = Path.home() / "test.jpg"
        
        # This should fail since the file doesn't exist, but we can check the error
        with pytest.raises(click.BadParameter) as exc_info:
            validate_image_path(
                self.mock_ctx,
                self.mock_param,
                fake_home_path
            )
        
        # Verify that the expanded path is mentioned in the error
        assert str(expected_path) in str(exc_info.value)
    
    def test_supported_formats(self):
        """Test that all supported image formats are accepted."""
        supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.heic', '.webp']
        
        for fmt in supported_formats:
            test_file = self.temp_dir / f"test{fmt}"
            test_file.write_text("fake content")
            
            try:
                result = validate_image_path(
                    self.mock_ctx,
                    self.mock_param,
                    str(test_file)
                )
                assert result == test_file.resolve()
            finally:
                test_file.unlink()
    
    def test_unsupported_format_error(self):
        """Test that unsupported formats raise appropriate errors."""
        unsupported_file = self.temp_dir / "test.gif"
        unsupported_file.write_text("fake content")
        
        try:
            with pytest.raises(click.BadParameter) as exc_info:
                validate_image_path(
                    self.mock_ctx,
                    self.mock_param,
                    str(unsupported_file)
                )
            
            # Check that the error mentions supported formats
            error_msg = str(exc_info.value)
            assert "Unsupported image format" in error_msg
            assert ".jpg" in error_msg  # Should list supported formats
        finally:
            unsupported_file.unlink()
    
    def test_nonexistent_file_error(self):
        """Test appropriate error for non-existent files."""
        fake_path = self.temp_dir / "nonexistent.jpg"
        
        with pytest.raises(click.BadParameter) as exc_info:
            validate_image_path(
                self.mock_ctx,
                self.mock_param,
                str(fake_path)
            )
        
        error_msg = str(exc_info.value)
        assert "Image file not found" in error_msg
        assert "drag and drop" in error_msg.lower()  # Should mention drag-and-drop tip
    
    def test_none_value_passthrough(self):
        """Test that None values pass through unchanged."""
        result = validate_image_path(
            self.mock_ctx,
            self.mock_param,
            None
        )
        assert result is None


def test_integration_with_click():
    """Integration test to ensure the validator works with Click."""
    import tempfile
    from click.testing import CliRunner
    import click
    
    # Create a simple CLI command using our validator
    @click.command()
    @click.option('-i', '--input', callback=validate_image_path)
    def test_command(input):
        click.echo(f"Valid image: {input}")
    
    runner = CliRunner()
    
    # Test with a real temporary file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        temp_path = f.name
    
    try:
        # Test valid file
        result = runner.invoke(test_command, ['-i', temp_path])
        assert result.exit_code == 0
        assert "Valid image:" in result.output
        
        # Test invalid file
        result = runner.invoke(test_command, ['-i', '/nonexistent/file.jpg'])
        assert result.exit_code != 0
        assert "Image file not found" in result.output
        
    finally:
        Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    # Run a simple test when executed directly
    import sys
    
    print("Testing drag-and-drop path validation...")
    
    test_instance = TestDragDropValidation()
    test_instance.setup_method()
    
    try:
        # Test basic functionality
        test_instance.test_basic_path_validation()
        print("✅ Basic path validation works")
        
        test_instance.test_quoted_path_handling()
        print("✅ Quoted path handling works")
        
        test_instance.test_supported_formats()
        print("✅ All supported formats accepted")
        
        print("\n🎉 All drag-and-drop tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
        
    finally:
        test_instance.teardown_method()
