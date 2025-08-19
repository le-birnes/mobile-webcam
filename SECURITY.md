# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of Mobile Webcam seriously. If you discover a security vulnerability, please follow these steps:

### Private Disclosure

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please send a report privately to [security email]. Include the following details:

- Type of vulnerability
- Full paths of source code files affected
- Location of affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact assessment

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Initial Response**: We will send a more detailed response within 72 hours indicating next steps
- **Fix Timeline**: We aim to release security fixes within 5 business days for critical issues
- **Credit**: We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   - Regularly run `npm audit` and `pip-audit`
   - Update to the latest version of Mobile Webcam

2. **Secure Configuration**
   - Use strong SSL certificates (not self-signed in production)
   - Configure proper CORS origins (avoid wildcards)
   - Use environment variables for sensitive configuration

3. **Network Security**
   - Run on trusted networks only
   - Consider VPN access for remote usage
   - Monitor access logs

### For Developers

1. **Dependency Management**
   - Pin exact versions in production
   - Regularly audit for vulnerabilities
   - Use tools like Dependabot for updates

2. **Code Security**
   - Never commit secrets, keys, or certificates
   - Validate all inputs from WebSocket messages
   - Implement proper error handling

3. **SSL/TLS**
   - Enable certificate validation by default
   - Provide clear warnings when disabled
   - Use strong cipher suites

## Known Security Considerations

### WebSocket Security

- The application broadcasts video streams to all connected clients
- No authentication mechanism is currently implemented
- Consider implementing authentication for production use

### SSL Certificate Validation

- The Python bridge supports disabling SSL verification for development
- This should never be used in production environments
- Always use valid certificates in production

### CORS Configuration

- Wildcard CORS origins (`*`) are supported but not recommended
- Configure specific allowed origins for production use
- Monitor for unauthorized cross-origin requests

## Security Features

### Implemented

- ✅ Environment-based configuration
- ✅ Configurable CORS policies
- ✅ SSL certificate validation (configurable)
- ✅ Connection limits and message size limits
- ✅ Security headers (X-Frame-Options, X-Content-Type-Options)
- ✅ Graceful error handling
- ✅ Input validation for image processing

### Recommended for Production

- 🔄 Authentication and authorization
- 🔄 Rate limiting
- 🔄 Audit logging
- 🔄 Network-level access controls
- 🔄 Regular security scanning

## Vulnerability Disclosure History

No vulnerabilities have been reported to date.

Last updated: 2025-08-19