#!/bin/bash

echo "============================================"
echo "      Starting Mobile Webcam System"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get IP address
IP_ADDRESS=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $SERVER_PID 2>/dev/null
    kill $BRIDGE_PID 2>/dev/null
    echo "Services stopped."
    exit 0
}

# Set up trap for cleanup
trap cleanup INT TERM

echo "Starting HTTPS server..."
node webcam_server_https.js &
SERVER_PID=$!
sleep 2

echo "Starting Phone-to-OBS bridge..."
python3 phone_obs_rotation.py &
BRIDGE_PID=$!
sleep 1

echo ""
echo "============================================"
echo "      Mobile Webcam is Running!"
echo "============================================"
echo ""
echo -e "${GREEN}On your phone, open browser and go to:${NC}"
echo ""
echo -e "${YELLOW}  https://$IP_ADDRESS:8443/${NC}"
echo ""
echo "Accept the security warning (self-signed certificate)"
echo "Then tap 'Start Camera' on your phone"
echo ""
echo "In OBS or any app, select 'OBS Virtual Camera'"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for interrupt
wait