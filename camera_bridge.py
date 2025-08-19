"""Camera processing functionality separated into a class."""
import cv2
import numpy as np
import pyvirtualcam
from PIL import Image
import io
import time
from typing import Tuple, Optional
from config import Config


class CameraBridge:
    """Handles camera operations and frame processing."""
    
    def __init__(self, config: Config):
        self.config = config
        self.cam: Optional[pyvirtualcam.Camera] = None
        self.frame_count = 0
        self.last_stats_time = time.time()
        self.last_orientation = "landscape"
        
    def initialize_camera(self) -> bool:
        """Initialize the virtual camera."""
        try:
            self.cam = pyvirtualcam.Camera(
                width=self.config.width, 
                height=self.config.height, 
                fps=self.config.fps, 
                device=self.config.virtual_camera_device
            )
            print(f"Virtual camera created: {self.cam.device}", flush=True)
            print(f"Output resolution: {self.config.width}x{self.config.height} @ {self.config.fps}fps", flush=True)
            return True
        except Exception as e:
            print(f"Failed to initialize virtual camera: {e}", flush=True)
            return False
    
    def close_camera(self):
        """Close the virtual camera."""
        if self.cam:
            self.cam.close()
            self.cam = None
    
    def resize_with_padding(self, image: Image.Image) -> Tuple[Image.Image, bool]:
        """Resize image to fit target dimensions while maintaining aspect ratio with padding."""
        
        # Get original dimensions
        orig_width, orig_height = image.size
        target_width, target_height = self.config.width, self.config.height
        
        # Calculate aspect ratios
        orig_aspect = orig_width / orig_height
        target_aspect = target_width / target_height
        
        # Determine if portrait or landscape
        is_portrait = orig_height > orig_width
        
        # Calculate scaling to fit within target while maintaining aspect ratio
        if orig_aspect > target_aspect:
            # Image is wider than target - fit by width
            new_width = target_width
            new_height = int(target_width / orig_aspect)
        else:
            # Image is taller than target - fit by height
            new_height = target_height
            new_width = int(target_height * orig_aspect)
        
        # Resize image maintaining aspect ratio
        image_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create black background
        result = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        
        # Calculate position to center the resized image
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        
        # Paste resized image onto black background
        result.paste(image_resized, (x_offset, y_offset))
        
        return result, is_portrait
    
    def process_frame(self, message: bytes) -> bool:
        """Process a frame from WebSocket message."""
        if not self.cam:
            print("Camera not initialized", flush=True)
            return False
            
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(message))
            
            # Convert to RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get original dimensions
            orig_width, orig_height = image.size
            
            # Validate image size (prevent excessive memory usage)
            if orig_width * orig_height > 50_000_000:  # 50MP limit
                print(f"Image too large: {orig_width}x{orig_height}", flush=True)
                return False
            
            # Resize with padding to maintain aspect ratio
            image_padded, is_portrait = self.resize_with_padding(image)
            
            # Convert to numpy array
            frame = np.array(image_padded)
            
            # Apply horizontal flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Send to virtual camera
            self.cam.send(frame)
            
            self.frame_count += 1
            
            # Detect orientation change
            current_orientation = "portrait" if is_portrait else "landscape"
            if current_orientation != self.last_orientation:
                print(f"Orientation changed to: {current_orientation.upper()} ({orig_width}x{orig_height})", flush=True)
                self.last_orientation = current_orientation
            
            # Print stats every 3 seconds
            current_time = time.time()
            if current_time - self.last_stats_time >= 3.0:
                elapsed = current_time - self.last_stats_time
                fps = self.frame_count / elapsed
                print(f"FPS: {fps:.1f}, Mode: {current_orientation}, Input: {orig_width}x{orig_height}", flush=True)
                self.frame_count = 0
                self.last_stats_time = current_time
            
            return True
            
        except Exception as e:
            print(f"Frame processing error: {e}", flush=True)
            return False