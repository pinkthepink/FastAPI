#!/bin/bash

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the FastAPI application
uvicorn app.main:app --reload