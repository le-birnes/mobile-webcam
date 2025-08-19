#!/bin/bash

echo "============================================"
echo "    Mobile Webcam Installer for macOS"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check for Homebrew
echo "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}[WARNING] Homebrew not installed${NC}"
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi
echo -e "${GREEN}[OK] Homebrew found${NC}"

# Check for Python
echo "Checking for Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}[WARNING] Python not installed${NC}"
    echo "Installing Python..."
    brew install python3
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}[OK] Python found: $PYTHON_VERSION${NC}"

# Check for Node.js
echo "Checking for Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}[WARNING] Node.js not installed${NC}"
    echo "Installing Node.js..."
    brew install node
fi
NODE_VERSION=$(node --version 2>&1)
echo -e "${GREEN}[OK] Node.js found: $NODE_VERSION${NC}"

# Check for OpenSSL
echo "Checking for OpenSSL..."
if ! command -v openssl &> /dev/null; then
    echo -e "${YELLOW}[WARNING] OpenSSL not installed${NC}"
    echo "Installing OpenSSL..."
    brew install openssl
fi
echo -e "${GREEN}[OK] OpenSSL found${NC}"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install Python dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Python dependencies installed${NC}"

# Install Node.js dependencies
echo ""
echo "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install Node.js dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Node.js dependencies installed${NC}"

# Check for OBS Virtual Camera
echo ""
echo "Checking for OBS Virtual Camera..."
python3 -c "import pyvirtualcam; print('Testing virtual camera...')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Virtual camera support may not be available${NC}"
    echo "On macOS, OBS Virtual Camera requires:"
    echo "1. OBS Studio installed"
    echo "2. OBS Virtual Camera plugin enabled"
    echo "3. System permissions granted"
    echo ""
    echo "Download OBS from: https://obsproject.com/"
else
    echo -e "${GREEN}[OK] Virtual camera support available${NC}"
fi

# Generate SSL certificates
echo ""
echo "Generating SSL certificates..."
if [ -f "server.key" ]; then
    echo -e "${YELLOW}[INFO] SSL certificates already exist${NC}"
else
    echo "Creating self-signed certificate..."
    openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.cert -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=MobileWebcam/CN=localhost" 2>/dev/null
    
    if [ -f "server.key" ]; then
        echo -e "${GREEN}[OK] SSL certificates generated${NC}"
    else
        echo -e "${RED}[ERROR] Failed to generate certificates${NC}"
        exit 1
    fi
fi

# Get IP address
echo ""
echo "Getting network information..."
IP_ADDRESS=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')

echo ""
echo "============================================"
echo "    Installation Complete!"
echo "============================================"
echo ""
echo "To start Mobile Webcam:"
echo "1. Run: ./start_mobile_webcam.sh"
echo "   Or manually:"
echo "   - Terminal 1: node webcam_server_https.js"
echo "   - Terminal 2: python3 phone_obs_rotation.py"
echo ""
echo "2. On your phone, open browser and go to:"
echo "   https://$IP_ADDRESS:8443/"
echo ""
echo "Note: Accept the security warning for the self-signed certificate"
echo ""

# Make start script executable
chmod +x start_mobile_webcam.sh 2>/dev/null