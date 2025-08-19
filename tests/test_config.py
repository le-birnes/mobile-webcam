"""Tests for the configuration module."""
import os
import pytest
from config import Config


class TestConfig:
    """Test cases for the Config class."""

    def test_config_from_env_defaults(self, monkeypatch):
        """Test configuration with default values."""
        # Clear relevant environment variables
        monkeypatch.delenv('SERVER_IP', raising=False)
        monkeypatch.delenv('PORT', raising=False)
        monkeypatch.delenv('CAMERA_WIDTH', raising=False)
        
        config = Config.from_env()
        
        assert config.ws_url == 'wss://localhost:8443'
        assert config.width == 1280
        assert config.height == 720
        assert config.fps == 30
        assert config.virtual_camera_device == 'OBS Virtual Camera'
        assert config.ssl_verify is True

    def test_config_from_env_custom(self, monkeypatch):
        """Test configuration with custom environment variables."""
        monkeypatch.setenv('SERVER_IP', '192.168.1.100')
        monkeypatch.setenv('PORT', '9000')
        monkeypatch.setenv('CAMERA_WIDTH', '1920')
        monkeypatch.setenv('CAMERA_HEIGHT', '1080')
        monkeypatch.setenv('CAMERA_FPS', '60')
        monkeypatch.setenv('SSL_VERIFY', 'false')
        
        config = Config.from_env()
        
        assert config.ws_url == 'wss://192.168.1.100:9000'
        assert config.width == 1920
        assert config.height == 1080
        assert config.fps == 60
        assert config.ssl_verify is False

    def test_ssl_verify_parsing(self, monkeypatch):
        """Test SSL verification flag parsing."""
        # Test true values
        for true_value in ['true', 'True', 'TRUE', 'yes', '1']:
            monkeypatch.setenv('SSL_VERIFY', true_value)
            config = Config.from_env()
            assert config.ssl_verify is True

        # Test false values  
        for false_value in ['false', 'False', 'FALSE', 'no', '0', '']:
            monkeypatch.setenv('SSL_VERIFY', false_value)
            config = Config.from_env()
            assert config.ssl_verify is False