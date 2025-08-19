"""
Mobile Webcam Bridge - Connects phone camera to OBS Virtual Camera
Refactored for better error handling, security, and maintainability.
"""
import websocket
import sys
import time
import ssl
import os
from typing import Optional
from config import Config
from camera_bridge import CameraBridge

# Load environment variables if .env file exists
if os.path.exists('.env'):
    from dotenv import load_dotenv
    load_dotenv()

# Unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Initialize configuration
config = Config.from_env()

print("Phone to OBS Virtual Camera Bridge (with rotation support)", flush=True)
print("===========================================================", flush=True)
print(f"Connecting to {config.ws_url}...", flush=True)
print(f"SSL verification: {'enabled' if config.ssl_verify else 'disabled'}", flush=True)

# Initialize camera bridge
camera_bridge = CameraBridge(config)

def on_message(ws: websocket.WebSocketApp, message) -> None:
    """Handle incoming WebSocket messages."""
    if isinstance(message, bytes):
        success = camera_bridge.process_frame(message)
        if not success:
            print("Failed to process frame", flush=True)

def on_error(ws: websocket.WebSocketApp, error) -> None:
    """Handle WebSocket errors."""
    print(f"WebSocket error: {error}", flush=True)

def on_close(ws: websocket.WebSocketApp, close_status_code: int, close_msg: str) -> None:
    """Handle WebSocket closure."""
    print(f"WebSocket closed: {close_status_code} - {close_msg}", flush=True)
    camera_bridge.close_camera()

def on_open(ws: websocket.WebSocketApp) -> None:
    """Handle WebSocket connection establishment."""
    print("Connected! Receiving phone camera...", flush=True)
    print("Rotation is handled: portrait videos will have black bars on sides", flush=True)

def main() -> None:
    """Main function to run the webcam bridge."""
    # Initialize camera
    if not camera_bridge.initialize_camera():
        print("Failed to initialize camera, exiting...", flush=True)
        return
    
    print("Creating WebSocket connection...", flush=True)
    
    # Configure SSL options
    ssl_options = {}
    if not config.ssl_verify:
        print("WARNING: SSL certificate verification is disabled", flush=True)
        ssl_options = {"cert_reqs": ssl.CERT_NONE}
    elif config.ssl_cert_path and config.ssl_key_path:
        ssl_options = {
            "cert_reqs": ssl.CERT_REQUIRED,
            "ca_certs": config.ssl_cert_path
        }
    
    # Create WebSocket connection
    ws = websocket.WebSocketApp(
        config.ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    print("Starting bridge...", flush=True)
    print("Press Ctrl+C to stop", flush=True)
    
    try:
        # Run with retry logic
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                ws.run_forever(sslopt=ssl_options)
                break
            except Exception as e:
                retry_count += 1
                print(f"Connection failed (attempt {retry_count}/{max_retries}): {e}", flush=True)
                if retry_count < max_retries:
                    print(f"Retrying in 5 seconds...", flush=True)
                    time.sleep(5)
                else:
                    print("Max retries reached, exiting...", flush=True)
                    
    except KeyboardInterrupt:
        print("Stopping...", flush=True)
    finally:
        camera_bridge.close_camera()
        print("Bridge stopped", flush=True)

if __name__ == "__main__":
    main()