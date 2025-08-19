import websocket
import cv2
import numpy as np
import pyvirtualcam
from PIL import Image
import io
import sys
import time
import ssl

# Unbuffered output
sys.stdout.reconfigure(line_buffering=True)

WS_URL = "wss://192.168.0.225:8443"
WIDTH = 1280
HEIGHT = 720
FPS = 30

print("Phone to OBS Virtual Camera Bridge (with rotation support)", flush=True)
print("===========================================================", flush=True)
print(f"Connecting to {WS_URL}...", flush=True)

# Create virtual camera
cam = pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=FPS, device='OBS Virtual Camera')
print(f"Virtual camera created: {cam.device}", flush=True)
print(f"Output resolution: {WIDTH}x{HEIGHT} @ {FPS}fps", flush=True)

frame_count = 0
last_stats_time = time.time()
last_orientation = "landscape"

def resize_with_padding(image, target_width, target_height):
    """Resize image to fit target dimensions while maintaining aspect ratio with padding"""
    
    # Get original dimensions
    orig_width, orig_height = image.size
    
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

def on_message(ws, message):
    global frame_count, last_stats_time, last_orientation
    
    if isinstance(message, bytes):
        try:
            # Convert bytes to image
            image = Image.open(io.BytesIO(message))
            
            # Convert to RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get original dimensions
            orig_width, orig_height = image.size
            
            # Resize with padding to maintain aspect ratio
            image_padded, is_portrait = resize_with_padding(image, WIDTH, HEIGHT)
            
            # Convert to numpy array
            frame = np.array(image_padded)
            
            # Apply horizontal flip for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Send to virtual camera
            cam.send(frame)
            
            frame_count += 1
            
            # Detect orientation change
            current_orientation = "portrait" if is_portrait else "landscape"
            if current_orientation != last_orientation:
                print(f"Orientation changed to: {current_orientation.upper()} ({orig_width}x{orig_height})", flush=True)
                last_orientation = current_orientation
            
            # Print stats every 3 seconds
            current_time = time.time()
            if current_time - last_stats_time >= 3.0:
                elapsed = current_time - last_stats_time
                fps = frame_count / elapsed
                print(f"FPS: {fps:.1f}, Mode: {current_orientation}, Input: {orig_width}x{orig_height}", flush=True)
                frame_count = 0
                last_stats_time = current_time
                
        except Exception as e:
            print(f"Frame error: {e}", flush=True)

def on_error(ws, error):
    print(f"WebSocket error: {error}", flush=True)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed", flush=True)

def on_open(ws):
    print("Connected! Receiving phone camera...", flush=True)
    print("Rotation is handled: portrait videos will have black bars on sides", flush=True)

print("Creating WebSocket connection...", flush=True)

# Create WebSocket with SSL disabled
ws = websocket.WebSocketApp(WS_URL,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

print("Starting bridge...", flush=True)
print("Press Ctrl+C to stop", flush=True)

try:
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
except KeyboardInterrupt:
    print("Stopping...", flush=True)
finally:
    cam.close()
    print("Bridge stopped", flush=True)