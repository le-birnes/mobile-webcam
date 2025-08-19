"""Configuration management for the mobile webcam bridge."""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for the mobile webcam bridge."""
    
    # WebSocket Configuration
    ws_url: str
    
    # Camera Configuration  
    width: int
    height: int
    fps: int
    virtual_camera_device: str
    
    # SSL Configuration
    ssl_verify: bool
    ssl_cert_path: Optional[str]
    ssl_key_path: Optional[str]
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables."""
        server_ip = os.getenv('SERVER_IP', 'localhost')
        port = os.getenv('PORT', '8443')
        
        return cls(
            ws_url=f"wss://{server_ip}:{port}",
            width=int(os.getenv('CAMERA_WIDTH', '1280')),
            height=int(os.getenv('CAMERA_HEIGHT', '720')),
            fps=int(os.getenv('CAMERA_FPS', '30')),
            virtual_camera_device=os.getenv('VIRTUAL_CAMERA_DEVICE', 'OBS Virtual Camera'),
            ssl_verify=os.getenv('SSL_VERIFY', 'true').lower() == 'true',
            ssl_cert_path=os.getenv('SSL_CERT_PATH'),
            ssl_key_path=os.getenv('SSL_KEY_PATH')
        )