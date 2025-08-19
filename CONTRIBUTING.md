# Contributing to Mobile Webcam

Thank you for your interest in contributing to the Mobile Webcam project! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

### Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/le-birnes/mobile-webcam.git
   cd mobile-webcam
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```

5. Generate SSL certificates for development:
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.cert -days 365 -nodes
   ```

## Development Workflow

### Code Style

- **JavaScript**: We use ESLint and Prettier for code formatting
- **Python**: We use Black and flake8 for code formatting
- **Commits**: Use conventional commit messages

### Running Locally

1. Start the HTTPS server:
   ```bash
   npm start
   ```

2. Start the camera bridge (in another terminal):
   ```bash
   npm run bridge
   ```

### Testing

- Run JavaScript tests: `npm test`
- Run Python tests: `pytest`
- Run linting: `npm run lint` and `flake8 *.py`
- Run formatting: `npm run format` and `black *.py`

### Pre-commit Checks

Before committing, ensure:

1. All tests pass
2. Code is properly formatted
3. No linting errors
4. Security audit passes: `npm audit`

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation if needed
7. Submit a pull request

### Pull Request Guidelines

- Provide a clear description of the changes
- Include tests for new features
- Update documentation as needed
- Follow the existing code style
- Reference any related issues

## Security

- Never commit SSL certificates, private keys, or sensitive credentials
- Use environment variables for configuration
- Report security vulnerabilities privately to the maintainers

## Code Review

All submissions require review. We use GitHub pull requests for this purpose. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

## Issues

Please use the GitHub issue tracker to:

- Report bugs
- Request features
- Ask questions

When reporting bugs, include:

- Operating system and version
- Node.js and Python versions
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.