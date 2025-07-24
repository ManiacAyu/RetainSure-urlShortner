# URL Shortener Service

## Overview
A simple URL shortening service similar to bit.ly or TinyURL, built with Flask and in-memory storage.  
Features:
- Convert long URLs into 6-character alphanumeric short codes
- Redirect to original URLs with click tracking
- View analytics (click count, creation timestamp)
- Thread-safe concurrent handling
- URL validation and normalization
- Clear JSON API and error responses

---

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py        # makes app/ a Python package
│   ├── main.py            # Flask app and endpoints
│   ├── models.py          # URLMapping & URLStore classes
│   └── utils.py           # URL validation & code generation
├── tests/
│   └── test_basic.py      # pytest test suite
├── requirements.txt       # Python dependencies
├── README.md              # this file
├── .gitignore             # files/folders to ignore in Git
└── conftest.py            # pytest configuration (adds project root to PYTHONPATH)
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```
# 1. Clone the repo
git clone https://github.com/ManiacAyu/RetainSure-urlShortner.git
cd RetainSure-urlShortner

# 2. Install dependencies
pip install -r requirements.txt
```

### Running the Application

```
# Option A: Flask CLI
export FLASK_APP=app.main      # Windows: set FLASK_APP=app.main
export FLASK_ENV=development   # Windows: set FLASK_ENV=development
flask run

# Option B: Direct execution
python app/main.py

# Option C: As a module
python -m app.main
```

By default, the API listens on `http://127.0.0.1:5000`.

---

## API Documentation

### 1. Health Check

**GET /**  
_Response 200_  
```
{ "status": "healthy", "service": "URL Shortener API" }
```

**GET /api/health**  
_Response 200_  
```
{ "status": "ok", "message": "URL Shortener API is running" }
```

---

### 2. Shorten URL

**POST /api/shorten**  
_Request JSON_  
```
{ "url": "https://www.example.com/very/long/url" }
```
_Response 201_  
```
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123",
  "original_url": "https://www.example.com/very/long/url"
}
```

_Error Responses_  
- 400 Bad Request: missing or invalid URL  
- 500 Internal Server Error: code generation failure

---

### 3. Redirect

**GET /**  
_Follows a 302 redirect to the original URL_

_Error Responses_  
- 400 Bad Request: short code must be 6 alphanumeric chars  
- 404 Not Found: short code not found

---

### 4. Analytics

**GET /api/stats/**  
_Response 200_  
```
{
  "url": "https://www.example.com/very/long/url",
  "short_code": "abc123",
  "clicks": 5,
  "created_at": "2024-01-01T10:00:00.123456"
}
```

_Error Responses_  
- 400 Bad Request: invalid short code format  
- 404 Not Found: short code not found

---

## Usage Examples

### Complete Workflow

```
# 1. Shorten a URL
curl -X POST http://localhost:5000/api/shorten   -H "Content-Type: application/json"   -d '{"url": "https://www.github.com/user/very-long-repository-name"}'

# Response: {"short_code": "k3mN9x", "short_url": "http://localhost:5000/k3mN9x", ...}

# 2. Use the shortened URL (increments click count)
curl -L http://localhost:5000/k3mN9x

# 3. Check analytics
curl http://localhost:5000/api/stats/k3mN9x
```

### URL Normalization

```
# URLs without scheme are automatically normalized
curl -X POST http://localhost:5000/api/shorten   -H "Content-Type: application/json"   -d '{"url": "www.example.com"}'

# Response will show: "original_url": "https://www.example.com"
```

---

## Testing

### Test Coverage
✅ Health check endpoints  
✅ URL shortening with validation  
✅ Error handling (invalid URLs, missing data)  
✅ Redirect functionality  
✅ Analytics tracking  
✅ Concurrent request handling  
✅ Edge cases and error conditions

### Running Tests

```
# Run all tests
pytest tests/ -v

# With coverage report
pytest --cov=app --cov-report=html

# Specific test
pytest tests/test_basic.py::test_shorten_url_success -v
```

---

## Technical Details

### Storage System
- **In-Memory**: Python dictionaries in server RAM
- **Thread-Safe**: Uses threading locks for concurrent access
- **Performance**: O(1) lookups, ~250-350 bytes per URL
- **Limitation**: Data lost on server restart

### Design Decisions
1. **6-Character Codes**: 62^6 ≈ 56 billion combinations
2. **Thread Safety**: Proper locking for concurrent requests
3. **URL Validation**: Multi-layer validation (regex + urlparse)
4. **Auto-normalization**: Adds https:// if missing
5. **Comprehensive Testing**: 12+ test cases covering core functionality

---

## Configuration

### Default Settings
- Host: `0.0.0.0` (accepts all connections)
- Port: `5000`
- Debug: `True` (disable in production)

### Customization
Edit `app/main.py`:
```
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## Troubleshooting

### Common Issues

**Import Errors**
```
# Ensure correct directory
cd url-shortener

# Create missing __init__.py
touch app/__init__.py

# Add to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Port in Use**
```
# Find process on port 5000
lsof -i :5000

# Use different port
python -m flask --app app.main run --port 5001
```

**Test Failures**
```
# Clear pytest cache
pytest --cache-clear tests/

# Verbose output
pytest tests/ -v -s
```

---

## Production Considerations

### Current Limitations
- Data lost on restart (in-memory storage)
- Single server instance only
- No authentication or rate limiting
- Memory constraints

### Production Recommendations
- **Database**: PostgreSQL/MySQL for persistence
- **Caching**: Redis for high-performance lookups
- **Scaling**: Load balancer with multiple instances
- **Security**: Authentication, rate limiting, input sanitization
- **Monitoring**: Logging, metrics, health checks

---

## Contributing

### Development Setup
1. Fork the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests: `pytest tests/ -v`

### Code Style
- Follow PEP 8 guidelines
- Meaningful variable/function names
- Docstrings for all functions and classes
- Maintain thread safety

---

## License

This project is created for educational purposes as part of a coding assignment.

**Built with ❤️ using Flask and Python**

For questions or issues, check the troubleshooting section or run the test suite for expected behavior examples.
