# Client Management API

A REST API for client management using FastAPI with async operations and best practices.

## Features

- Async-first implementation using FastAPI and Motor
- MongoDB integration
- RESTful API endpoints
- Comprehensive error handling
- Background tasks
- Middleware for request logging, timing, and identification
- Comprehensive test suite

## Requirements

- Python 3.11+
- MongoDB 6.0+
- Docker and Docker Compose (optional)

## Installation

### Local Development

1. Clone this repository
2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example` and update the values as needed
5. Ensure MongoDB is running locally or use Docker Compose to start MongoDB
6. Start the application using the provided script:
   ```bash
   ./run.sh
   ```
   
   Or manually:
   ```bash
   uvicorn app.main:app --reload
   ```

### Using Docker

1. Clone this repository
2. Make sure Docker and Docker Compose are installed
3. Create a `.env` file based on `.env.example` (optional, defaults are set in docker-compose.yml)
4. Start the application using the provided script:
   ```bash
   ./docker-run.sh
   ```
   
   Or manually:
   ```bash
   docker-compose up
   ```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

If you encounter any issues running the application or tests, please refer to the [Troubleshooting Guide](TROUBLESHOOTING.md).

## Testing

### Test Requirements

Before running the tests, make sure you have:

1. MongoDB running locally (required for repository and API tests)
2. All dependencies installed

### Running Tests

Run the tests using the provided script:

```bash
./run_tests.sh
```

Or manually:

```bash
pytest
```

To run a specific test file:

```bash
./run_tests.sh tests/api/test_clientes.py
```

To run tests with verbose output:

```bash
./run_tests.sh -v
```

### Troubleshooting Tests

If tests are failing with MongoDB connection errors, make sure MongoDB is installed and running:

```bash
# Install MongoDB on Ubuntu
sudo apt install mongodb

# Check MongoDB status
sudo systemctl status mongodb

# Start MongoDB if not running
sudo systemctl start mongodb
```

### Running Tests with Docker

The simplest way to run tests is with Docker Compose, which will automatically set up MongoDB:

```bash
# Run all tests using the provided script
./docker-test.sh

# Run specific tests with the script
./docker-test.sh pytest tests/api/test_clientes.py -v

# Or run tests directly with docker-compose
docker-compose run test
```

Alternatively, you can just use Docker to run MongoDB for testing:

```bash
docker run --name mongodb-test -p 27017:27017 -d mongo:6
```

## Project Structure

```
.
├── app                      # Application code
│   ├── api                  # API endpoints and dependencies
│   │   ├── dependencies     # API dependencies
│   │   └── endpoints        # API endpoint handlers
│   ├── core                 # Core modules
│   ├── database             # Database connection
│   ├── repositories         # Data access layer
│   ├── schemas              # Pydantic models
│   └── utils                # Utility functions
├── tests                    # Test suite
│   ├── api                  # API tests
│   └── repositories         # Repository tests
├── .env.example             # Example environment variables
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```