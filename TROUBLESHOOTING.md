# Troubleshooting Guide

This guide helps resolve common issues with running the Client Management API.

## MongoDB Connection Issues

### Problem: Tests fail with MongoDB connection errors

Error message: `ConnectionError: MongoDB connection not established`

**Solution:**

1. First, check if MongoDB is installed and running:

```bash
# Check MongoDB status
systemctl status mongodb  # or mongod on some systems
```

2. If MongoDB is not installed, install it:

```bash
# On Ubuntu
sudo apt install mongodb

# On macOS with Homebrew
brew install mongodb-community
```

3. If MongoDB is installed but not running, start it:

```bash
# On Ubuntu
sudo systemctl start mongodb  # or mongod

# On macOS with Homebrew
brew services start mongodb-community
```

4. Alternatively, use Docker to run MongoDB:

```bash
docker run --name mongodb -p 27017:27017 -d mongo:6
```

### Problem: Application fails to start with MongoDB connection errors

Error message: `ServerSelectionTimeoutError: No servers found yet`

**Solution:**

1. Check if the MongoDB URI in your `.env` file is correct
2. Verify MongoDB is running on the specified host and port
3. Check if any firewall is blocking the connection
4. Try using `localhost` instead of `127.0.0.1` or vice versa

## Docker Issues

### Problem: Docker containers fail to build or start

**Solution:**

1. Make sure Docker and Docker Compose are installed and running
2. Check for any conflicting port usage:

```bash
# On Linux/macOS
sudo lsof -i :27017   # Check if port 27017 is in use
sudo lsof -i :8000    # Check if port 8000 is in use
```

3. Try rebuilding the containers:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## Testing Issues

### Problem: Tests fail with httpx connection errors

Error message: `httpx.ConnectError: [Errno -3] Temporary failure in name resolution`

**Solution:**

The test client is trying to make a real HTTP request instead of using the ASGI transport.

1. Verify the test client is properly configured in `tests/conftest.py`
2. Make sure you're using the `ASGITransport` for the test client

### Problem: Tests fail with event loop errors

**Solution:**

1. Make sure you're using the latest version of pytest-asyncio
2. Ensure the event loop fixture is properly configured
3. Try running tests with isolation:

```bash
pytest --asyncio-mode=strict
```

## Application Startup Issues

### Problem: Application fails to start with import errors

**Solution:**

1. Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

2. Check for any missing or incorrectly named files

### Problem: Application starts but returns 500 errors on all requests

**Solution:**

1. Check the application logs for detailed error messages
2. Verify the MongoDB connection is working
3. Make sure all required environment variables are set