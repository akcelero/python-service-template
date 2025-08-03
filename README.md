# Python service template

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

[![CI/CD](https://github.com/akcelero/python-service-template/actions/workflows/run-tests.yaml/badge.svg?query=branch%3Amaster)](https://github.com/akcelero/python-service-template/actions/)

---

A production-ready template for building scalable Python microservices with FastAPI, featuring modern development tools and best practices.

## Features

- FastAPI Framework: High-performance async web framework with automatic API documentation
- Authentication: JWT token handling with joserfc
- Database Integration: SQLAlchemy ORM with PostgreSQL for production and SQLite for testing
- Testing Suite: Comprehensive test setup with pytest
- Code Quality:
  - Pre-configured tools for maintaining high code standards
  - Ruff: Lightning-fast Python linter and formatter
  - MyPy: Static type checking
  - Bandit: Security vulnerability scanner
- Development Workflow: Streamlined development with Just command runner
- Database Migrations: Alembic for database schema management
- Containerization: Docker and Docker Compose configuration included

## Tech Stack

### Core Dependencies
- FastAPI - Modern web framework for building APIs
- Uvicorn - Lightning-fast ASGI server
- SQLAlchemy - Python SQL toolkit and ORM
- Alembic - Database migration tool
- joserfc - JWT token handling

### Development Tools
- Ruff - Python linting and formatting
- MyPy - Static type checking
- Bandit - Security testing
- pytest - Testing framework
- Just - Command runner
- Pre-commit - Git hooks framework

## Quick Start
### Prerequisites
- Python 3.13+
- Docker and Docker Compose
- Just command runner
- uv package manager

## Installation
1. Clone or use this template:
```bash
git clone git@github.com:akcelero/python-service-template.git
cd python-service-template
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the development environment:
```bash
just build  # Build and start with Docker
# or
just up     # Start services
```

5. Run database migrations:
```bash
just migrate
```

### Testing
The template includes comprehensive testing setup:
- Unit Tests: Fast, isolated tests for individual components
- Integration Tests: Database and API endpoint testing
- Security Tests: Automated vulnerability scanning
```bash
# Run all tests
just test

# Run specific test file
just pytest tests/test_specific.py
```

## Database

Development
- PostgreSQL: Production-grade database for development
- Automatic migrations: Schema changes managed with Alembic

Testing
- SQLite: Fast, in-memory database for tests
- Isolated transactions: Each test runs in isolation

## Environment Variables
Ensure these are set in production:
- DATABASE_URL: PostgreSQL connection string
- JWT_SECRET_KEY: Secret for JWT token signing
- ENVIRONMENT: Set to "production"

## API Documentation
When running the service, interactive API documentation is available at:<br>
Swagger UI: http://localhost:8000/docs<br>
ReDoc: http://localhost:8000/redoc

## License
This template is open source and available under the MIT License.<br>
Ready to build your next microservice? This template provides everything you need to get started quickly while maintaining production-ready standards. Happy coding! 🚀
