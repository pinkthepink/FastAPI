# Petshop API - FastAPI Version

This is the FastAPI implementation of the Petshop Management API.

## Requirements

- Python 3.8+
- MongoDB

## Project Structure

```
python/
├── app/
│   ├── api/
│   │   ├── dependencies.py      # Dependency injection
│   │   ├── api_router.py        # API router
│   │   └── endpoints/           # API endpoints
│   ├── core/                    # Core configuration
│   │   ├── config.py            # Settings
│   │   ├── errors.py            # Exception classes
│   │   └── security.py          # Security utils
│   ├── database/                # Database connections
│   │   └── mongodb.py           # MongoDB connection
│   ├── middleware/              # Custom middleware
│   ├── models/                  # Pydantic models
│   ├── schemas/                 # Request/response models
│   ├── utils/                   # Utility functions
│   │   └── error_handlers.py    # Error handling
│   └── main.py                  # Application entry point
├── tests/                       # Test files
├── .env.example                 # Environment variables example
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure your environment variables
5. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the server is running, you can access:
- API documentation at `/docs`
- Alternative documentation at `/redoc`

## Technologies Used

- FastAPI - Web framework
- Motor - Async MongoDB driver
- Pydantic - Data validation
- Uvicorn - ASGI server

## Development

### Running Tests

```
pytest
```

### Linting

```
flake8 app tests
```

### Formatting

```
black app tests
```