// Basic configuration tests for the mobile webcam server
const { describe, test, expect, beforeEach, afterEach } = require('@jest/globals');

describe('Configuration Tests', () => {
    let originalEnv;

    beforeEach(() => {
        // Store original environment
        originalEnv = { ...process.env };
    });

    afterEach(() => {
        // Restore original environment
        process.env = originalEnv;
    });

    test('should use default port when PORT is not set', () => {
        delete process.env.PORT;
        const defaultPort = process.env.PORT || 8443;
        expect(defaultPort).toBe(8443);
    });

    test('should use environment PORT when set', () => {
        process.env.PORT = '9000';
        const port = process.env.PORT || 8443;
        expect(port).toBe('9000');
    });

    test('should use default SERVER_IP when not set', () => {
        delete process.env.SERVER_IP;
        const defaultServerIP = process.env.SERVER_IP || 'localhost';
        expect(defaultServerIP).toBe('localhost');
    });

    test('should parse ALLOWED_ORIGINS correctly', () => {
        process.env.ALLOWED_ORIGINS = 'http://localhost:3000,https://example.com';
        const allowedOrigins = process.env.ALLOWED_ORIGINS.split(',').map(origin => origin.trim());
        expect(allowedOrigins).toEqual(['http://localhost:3000', 'https://example.com']);
    });
});