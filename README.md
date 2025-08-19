# Mobile Webcam - Phone to OBS Virtual Camera Bridge

Transform your phone into a wireless webcam for OBS and other applications. Stream your phone's camera over WiFi to OBS Virtual Camera with rotation support, horizontal flip, and low latency.

## Features

- 📱 Use phone as wireless webcam over WiFi
- 🔄 Automatic rotation handling (portrait/landscape)
- 🪞 Horizontal flip option for readable text
- 🔒 HTTPS support for camera permissions
- 📹 Direct integration with OBS Virtual Camera
- 🖼️ Maintains aspect ratio (no squishing)
- ⚡ Low latency streaming (~25-30 FPS)
- 🎯 No app installation required on phone

## Requirements

- Python 3.x
- Node.js
- OBS Virtual Camera installed
- Phone and PC on same network

## Quick Installation

### Windows
```batch
git clone https://github.com/yourusername/mobile-webcam.git
cd mobile-webcam
install_windows.bat
```

### macOS
```bash
git clone https://github.com/yourusername/mobile-webcam.git
cd mobile-webcam
chmod +x install_mac.sh
./install_mac.sh
```

The installer will:
- Check for required software (Python, Node.js, OpenSSL)
- Install all dependencies automatically
- Generate SSL certificates
- Verify OBS Virtual Camera availability
- Display your PC's IP address

### Manual Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Generate SSL certificates (for HTTPS):
```bash
openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.cert -days 365 -nodes
```

## Usage

### Quick Start

#### Windows
```batch
start_mobile_webcam.bat
```

#### macOS/Linux
```bash
./start_mobile_webcam.sh
```

This will automatically:
1. Start the HTTPS server
2. Start the phone-to-OBS bridge
3. Display your PC's IP address
4. Open both services in separate terminals

### Manual Start

1. Start the HTTPS server:
```bash
node webcam_server_https.js
```

2. Start the phone-to-OBS bridge:
```bash
python phone_obs_rotation.py
```

3. On your phone, open browser and go to:
```
https://YOUR_PC_IP:8443/
```
(Replace YOUR_PC_IP with your PC's IP address, e.g., 192.168.0.225)

4. Accept the security warning (self-signed certificate)

5. Tap "Start Camera" on your phone

6. In OBS or any app, select "OBS Virtual Camera" as video source

### Components

#### 1. HTTPS Server (`webcam_server_https.js`)
- Serves the web interface
- Handles WebSocket connections
- Enables HTTPS for camera permissions

#### 2. Phone Interface (`webcam_with_flip_control.html`)
- Camera selection (front/back)
- Horizontal flip toggle
- Real-time streaming via WebSocket

#### 3. Phone-to-OBS Bridge (`phone_obs_rotation.py`)
- Receives phone camera stream
- Handles rotation (portrait/landscape)
- Applies horizontal flip
- Sends to OBS Virtual Camera

#### 4. PC Receiver (`webcam_receiver.html`)
- Optional viewer for debugging
- Shows phone stream in browser

#### 5. Keep-Alive Mode (`webcam_keep_alive.html`)
- Prevents phone screen from locking
- Wake Lock API support
- Screen dimming with tap-to-restore
- Silent audio loop for background activity
- Maintains streaming even with dimmed screen

## File Structure

```
mobile-webcam/
├── webcam_server_https.js       # HTTPS/WebSocket server
├── phone_obs_rotation.py        # Main bridge script
├── webcam_with_flip_control.html # Phone interface (standard)
├── webcam_keep_alive.html       # Phone interface (keep-alive mode)
├── webcam_receiver.html         # PC viewer (optional)
├── server.key                   # SSL private key
├── server.cert                  # SSL certificate
├── package.json                 # Node.js dependencies
├── requirements.txt             # Python dependencies
├── install_windows.bat          # Windows installer
├── install_mac.sh               # macOS installer
├── start_mobile_webcam.bat      # Windows launcher
├── start_mobile_webcam.sh       # macOS launcher
└── README.md                    # This file
```

## Features in Detail

### Rotation Support
- **Landscape**: Full 1280x720 display
- **Portrait**: Maintains aspect ratio with black bars (pillarboxing)
- Automatic detection and switching

### Horizontal Flip
- Mirror mode for readable text
- Toggle available in phone interface
- Applied at bridge level

### Low Latency
- Direct WebSocket streaming
- ~25-30 FPS performance
- Optimized frame processing

### Keep-Alive Mode (Prevent Screen Lock)
Access the keep-alive interface at:
```
https://YOUR_PC_IP:8443/keep-alive
```

Features:
- **Wake Lock API**: Prevents screen timeout
- **Screen Dimming**: Dims after 10s, tap to restore
- **Audio Keep-Alive**: Silent audio loop keeps browser active
- **Background Streaming**: Continues even when dimmed
- **FPS Counter**: Monitor performance in real-time

Note: Complete screen lock prevention has limitations:
- Works best with screen always on + dimming
- Some phones may still lock after extended periods
- Consider using "Developer options" > "Stay awake" for extended use

## Troubleshooting

### Phone camera not starting
- Ensure HTTPS is used (not HTTP)
- Accept security certificate warning
- Check camera permissions in browser

### OBS Virtual Camera not available
- Install OBS Virtual Camera plugin
- Restart OBS after installation
- Check Windows privacy settings

### Connection refused
- Check firewall settings
- Ensure PC and phone on same network
- Verify IP address is correct

### Poor performance
- Reduce camera resolution on phone
- Check WiFi signal strength
- Close other bandwidth-heavy applications

## Advanced Configuration

### Change resolution
Edit `phone_obs_rotation.py`:
```python
WIDTH = 1920  # Change from 1280
HEIGHT = 1080  # Change from 720
```

### Change port
Edit `webcam_server_https.js`:
```javascript
const PORT = 8443;  // Change to desired port
```

### Custom SSL certificate
Replace `server.key` and `server.cert` with your own certificates.

## Security Notes

- Uses self-signed SSL certificate by default
- Secure WebSocket (WSS) for encrypted transmission
- No data stored or transmitted outside local network
- Camera access only when explicitly granted

## License

MIT License

## Contributing

Pull requests welcome! For major changes, please open an issue first.

## Credits

Created with Claude Code Assistant