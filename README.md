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

- Python 3.8+ with pip
- Node.js 18+ with npm
- OBS Virtual Camera installed
- Phone and PC on same network
- OpenSSL (for SSL certificate generation)

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

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Server Configuration
PORT=8443
HOST=0.0.0.0
SERVER_IP=192.168.0.225

# SSL Configuration
SSL_KEY_PATH=server.key
SSL_CERT_PATH=server.cert

# CORS Configuration (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,https://localhost:3000

# Camera Configuration
CAMERA_WIDTH=1280
CAMERA_HEIGHT=720
CAMERA_FPS=30

# Development
NODE_ENV=development
```

### Advanced Configuration

#### Development Tools

```bash
# Install development dependencies
npm install

# Run with auto-reload
npm run dev

# Run tests
npm test
npm run test:python

# Code formatting
npm run format
black *.py

# Linting
npm run lint
flake8 *.py
```

#### Custom SSL Certificates

For production use, replace self-signed certificates:

```bash
# Generate production certificates (replace with real domain)
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.cert -days 365 -nodes -subj "/CN=yourdomain.com"
```

#### Performance Tuning

- **Higher resolution**: Set `CAMERA_WIDTH=1920` and `CAMERA_HEIGHT=1080`
- **Lower latency**: Reduce `CAMERA_FPS=15` for slower networks
- **Connection limits**: Modify WebSocket connection limits in code

## Security Notes

### Built-in Security Features

- ✅ **HTTPS/WSS encryption** for all communications
- ✅ **Configurable CORS policies** to restrict access origins
- ✅ **SSL certificate validation** (configurable)
- ✅ **Connection limits** and message size limits
- ✅ **Input validation** for all data processing
- ✅ **Security headers** (X-Frame-Options, Content-Type-Options)
- ✅ **Environment-based configuration** (no hardcoded secrets)

### Production Security Checklist

- [ ] Use valid SSL certificates (not self-signed)
- [ ] Configure specific CORS origins (avoid wildcards)
- [ ] Enable SSL certificate validation
- [ ] Run on trusted networks with firewall protection
- [ ] Regularly update dependencies (`npm audit`, `pip-audit`)
- [ ] Monitor access logs for suspicious activity

### Development vs Production

**Development (Default)**:
- Self-signed SSL certificates
- Wildcard CORS (`*`) allowed
- SSL verification can be disabled
- Detailed error messages

**Production Recommendations**:
- Valid SSL certificates from trusted CA
- Specific CORS origins only
- SSL verification always enabled
- Error message sanitization
- Network-level access controls

See [SECURITY.md](SECURITY.md) for detailed security information.

## License

MIT License

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch
3. Install dependencies: `npm install && pip install -r requirements.txt`
4. Make your changes
5. Run tests: `npm test && pytest`
6. Submit a pull request

## Credits

Created with Claude Code Assistant