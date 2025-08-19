require('dotenv').config();
const https = require('https');
const fs = require('fs');
const path = require('path');
const express = require('express');
const WebSocket = require('ws');

// Configuration
const PORT = process.env.PORT || 8443;
const HOST = process.env.HOST || '0.0.0.0';
const SERVER_IP = process.env.SERVER_IP || 'localhost';
const ALLOWED_ORIGINS = process.env.ALLOWED_ORIGINS ? 
    process.env.ALLOWED_ORIGINS.split(',').map(origin => origin.trim()) : 
    ['http://localhost:3000', 'https://localhost:3000'];
const SSL_KEY_PATH = process.env.SSL_KEY_PATH || 'server.key';
const SSL_CERT_PATH = process.env.SSL_CERT_PATH || 'server.cert';

const app = express();

// Serve static files
app.use(express.static(__dirname));

// Enhanced CORS middleware with origin validation
app.use((req, res, next) => {
    const origin = req.headers.origin;
    
    // Allow requests without origin (like Postman, curl) in development
    if (!origin && process.env.NODE_ENV === 'development') {
        res.header('Access-Control-Allow-Origin', '*');
    } else if (origin && (ALLOWED_ORIGINS.includes('*') || ALLOWED_ORIGINS.includes(origin))) {
        res.header('Access-Control-Allow-Origin', origin);
    } else if (origin) {
        return res.status(403).json({ error: 'CORS: Origin not allowed' });
    }
    
    res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    res.header('Access-Control-Allow-Credentials', 'true');
    
    // Security headers
    res.header('X-Content-Type-Options', 'nosniff');
    res.header('X-Frame-Options', 'DENY');
    res.header('X-XSS-Protection', '1; mode=block');
    
    if (req.method === 'OPTIONS') {
        res.sendStatus(200);
    } else {
        next();
    }
});

// Serve the HTML files
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'webcam_with_flip_control.html'));
});

app.get('/webcam_with_bridge.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'webcam_with_bridge.html'));
});

app.get('/webcam_with_flip_control.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'webcam_with_flip_control.html'));
});

app.get('/webcam_receiver.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'webcam_receiver.html'));
});

app.get('/webcam_keep_alive.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'webcam_keep_alive.html'));
});

app.get('/keep-alive', (req, res) => {
    res.redirect('/webcam_keep_alive.html');
});

// SSL options for HTTPS with error handling
let serverOptions;
try {
    serverOptions = {
        key: fs.readFileSync(SSL_KEY_PATH),
        cert: fs.readFileSync(SSL_CERT_PATH)
    };
} catch (error) {
    console.error('Error loading SSL certificates:', error.message);
    console.error('Please ensure SSL certificate files exist:');
    console.error(`- Key file: ${SSL_KEY_PATH}`);
    console.error(`- Cert file: ${SSL_CERT_PATH}`);
    console.error('You can generate self-signed certificates using:');
    console.error('openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.cert -days 365 -nodes');
    process.exit(1);
}

// Create HTTPS server
const server = https.createServer(serverOptions, app);

// Create WebSocket server for HTTPS
const wss = new WebSocket.Server({ 
    server,
    perMessageDeflate: false
});

let clients = new Set();

wss.on('connection', (ws, req) => {
    const clientIP = req.socket.remoteAddress;
    console.log(`New WebSocket client connected from ${clientIP}`);
    clients.add(ws);
    
    // Connection limit
    if (clients.size > 100) {
        console.warn('Connection limit reached, closing oldest connection');
        const oldestClient = clients.values().next().value;
        oldestClient.close(1008, 'Connection limit exceeded');
        clients.delete(oldestClient);
    }
    
    ws.on('message', (message) => {
        try {
            // Message size limit (10MB)
            if (message.length > 10 * 1024 * 1024) {
                console.warn(`Large message received: ${message.length} bytes from ${clientIP}`);
                return;
            }
            
            // Broadcast to all other clients
            clients.forEach(client => {
                if (client !== ws && client.readyState === WebSocket.OPEN) {
                    try {
                        client.send(message);
                    } catch (sendError) {
                        console.error('Error sending message to client:', sendError.message);
                        clients.delete(client);
                    }
                }
            });
        } catch (error) {
            console.error('Error processing message:', error.message);
        }
    });
    
    ws.on('close', (code, reason) => {
        console.log(`WebSocket client disconnected: ${code} ${reason}`);
        clients.delete(ws);
    });
    
    ws.on('error', (error) => {
        console.error(`WebSocket error from ${clientIP}:`, error.message);
        clients.delete(ws);
    });
});

// Graceful shutdown handling
const gracefulShutdown = () => {
    console.log('Received shutdown signal, closing server...');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
    
    // Force close after 10 seconds
    setTimeout(() => {
        console.log('Force closing server...');
        process.exit(1);
    }, 10000);
};

process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

server.listen(PORT, HOST, () => {
    console.log(`HTTPS Server running on https://${SERVER_IP}:${PORT}`);
    console.log(`WebSocket available on wss://${SERVER_IP}:${PORT}`);
    console.log(`Access the camera at https://${SERVER_IP}:${PORT}/webcam_with_flip_control.html`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`Allowed origins: ${ALLOWED_ORIGINS.join(', ')}`);
});

server.on('error', (error) => {
    if (error.code === 'EADDRINUSE') {
        console.error(`Port ${PORT} is already in use`);
    } else if (error.code === 'EACCES') {
        console.error(`Permission denied to bind to port ${PORT}`);
    } else {
        console.error('Server error:', error.message);
    }
    process.exit(1);
});