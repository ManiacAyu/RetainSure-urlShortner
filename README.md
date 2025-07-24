```markdown
# URL Shortener Service

## Overview
A simple URL shortening service similar to bit.ly or tinyurl, built with Flask and in-memory storage. This service provides URL shortening, redirection, and analytics capabilities with thread-safe concurrent request handling.

## Features
- **URL Shortening**: Convert long URLs into 6-character alphanumeric short codes
- **Smart Redirection**: Redirect users to original URLs with click tracking
- **Analytics**: View detailed statistics including click counts and creation timestamps
- **Thread-Safe**: Handles concurrent requests safely using Python threading locks
- **Input Validation**: Validates URLs and normalizes them (adds https:// if missing)
- **Error Handling**: Comprehensive error responses with appropriate HTTP status codes

## Project Structure
```
url-shortener/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Flask application and API endpoints
│   ├── models.py            # Data models and storage classes
│   └── utils.py             # Utility functions (validation, code generation)
├── tests/
│   └── test_basic.py        # Comprehensive test suite
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore rules
└── conftest.py             # Pytest configuration
```

## Technical Architecture

### Storage System
- **In-Memory Storage**: Uses Python dictionaries stored in server RAM
- **Thread-Safe Operations**: All storage operations use threading locks
- **Data Persistence**: Data exists only during server runtime (resets on restart)
- **Performance**: O(1) lookup time for URL retrieval

### API Endpoints
1. **Health Check**: `GET /` and `GET /api/health`
2. **Shorten URL**: `POST /api/shorten`
3. **Redirect**: `GET /`
4. **Analytics**: `GET /api/stats/`

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation & Setup

1. **Clone or download the project**
   ```
   git clone 
   cd url-shortener
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Start the application**
   ```
   # Method 1: Using Flask CLI
   python -m flask --app app.main run
   
   # Method 2: Direct execution
   python app/main.py
   
   # Method 3: Using Python module
   python -m app.main
   ```

4. **Verify the setup**
   ```
   # Test health endpoint
   curl http://localhost:5000/
   ```

The API will be available at `http://localhost:5000`

### Running Tests
```
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app

# Run specific test file
pytest tests/test_basic.py -v
```

## API Documentation

### 1. Health Check Endpoints

**Basic Health Check**
```
GET /
```
**Response:**
```
{
  "status": "healthy",
  "service": "URL Shortener API"
}
```

**API Health Check**
```
GET /api/health
```
**Response:**
```
{
  "status": "ok",
  "message": "URL Shortener API is running"
}
```

### 2. Shorten URL

**Endpoint:** `POST /api/shorten`

**Request:**
```
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
```

**Response (201 Created):**
```
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123",
  "original_url": "https://www.example.com/very/long/url"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid or missing URL
- `500 Internal Server Error`: Short code generation failure

### 3. Redirect to Original URL

**Endpoint:** `GET /`

**Example:**
```
curl -L http://localhost:5000/abc123
```

**Response:** HTTP 302 redirect to original URL

**Error Responses:**
- `400 Bad Request`: Invalid short code format
- `404 Not Found`: Short code doesn't exist

### 4. Get Analytics

**Endpoint:** `GET /api/stats/`

**Example:**
```
curl http://localhost:5000/api/stats/abc123
```

**Response (200 OK):**
```
{
  "url": "https://www.example.com/very/long/url",
  "short_code": "abc123",
  "clicks": 5,
  "created_at": "2024-01-01T10:00:00.123456"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid short code format
- `404 Not Found`: Short code doesn't exist

## Usage Examples

### Complete Workflow Example
```
# 1. Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.github.com/user/very-long-repository-name"}'

# Response: {"short_code": "k3mN9x", "short_url": "http://localhost:5000/k3mN9x", ...}

# 2. Use the shortened URL (this increments click count)
curl -L http://localhost:5000/k3mN9x

# 3. Check analytics
curl http://localhost:5000/api/stats/k3mN9x

# Response: {"url": "https://www.github.com/...", "clicks": 1, "created_at": "..."}
```

### URL Validation Features
```
# URLs without scheme are automatically normalized
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "www.example.com"}'

# Response will show: "original_url": "https://www.example.com"
```

## Testing

### Test Coverage
The project includes comprehensive tests covering:
- ✅ Health check endpoints
- ✅ Successful URL shortening
- ✅ URL validation and normalization
- ✅ Error handling (invalid URLs, missing data)
- ✅ Redirect functionality
- ✅ Analytics tracking
- ✅ Click count accuracy
- ✅ Concurrent request handling
- ✅ Edge cases and error conditions

### Running Tests
```
# Run all tests with verbose output
pytest tests/ -v

# Run specific test functions
pytest tests/test_basic.py::test_shorten_url_success -v

# Run tests with coverage report
pytest tests/ --cov=app --cov-report=html
```

## Configuration

### Environment Variables
The application uses the following default configurations:
- **Host**: `0.0.0.0` (accepts connections from any IP)
- **Port**: `5000`
- **Debug Mode**: `True` (disable in production)

### Customization
You can modify the configuration in `app/main.py`:
```
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Development

### Code Organization
- **`app/main.py`**: Flask application and all API endpoints
- **`app/models.py`**: Data models (`URLMapping`) and storage class (`URLStore`)
- **`app/utils.py`**: Utility functions for URL validation and short code generation
- **`tests/test_basic.py`**: Comprehensive test suite

### Key Design Decisions
1. **In-Memory Storage**: Fast access times, simple implementation, suitable for assignment scope
2. **Thread Safety**: Uses Python threading locks for concurrent request handling
3. **6-Character Codes**: Alphanumeric codes provide 62^6 ≈ 56 billion possible combinations
4. **URL Normalization**: Automatically adds https:// scheme if missing
5. **Comprehensive Validation**: Multi-layer URL validation using regex and urlparse

### Performance Characteristics
- **URL Shortening**: O(n) where n is max_attempts for unique code generation
- **URL Retrieval**: O(1) dictionary lookup
- **Click Tracking**: O(1) with thread-safe increment
- **Memory Usage**: ~250-350 bytes per stored URL mapping

## Limitations & Production Considerations

### Current Limitations
- **Data Persistence**: All data lost on server restart
- **Single Instance**: Cannot scale across multiple servers
- **Memory Constraints**: Limited by available server RAM
- **No Authentication**: Open API without user management

### Production Recommendations
For production deployment, consider:
- **Database Storage**: PostgreSQL, MySQL, or Redis for persistence
- **Caching Layer**: Redis for high-performance lookups
- **Load Balancing**: Multiple application instances
- **Rate Limiting**: Prevent API abuse
- **Authentication**: User accounts and API keys
- **Custom Domains**: Support for branded short URLs
- **Analytics Enhancement**: Detailed tracking and reporting

## Troubleshooting

### Common Issues

**Import Errors**
```
# Ensure you're in the correct directory
cd url-shortener

# Create __init__.py if missing
touch app/__init__.py

# Add to Python path if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Port Already in Use**
```
# Find process using port 5000
lsof -i :5000

# Kill the process or use different port
python -m flask --app app.main run --port 5001
```

**Test Failures**
```
# Clear pytest cache
pytest --cache-clear tests/

# Run tests with more verbose output
pytest tests/ -v -s
```

## Contributing

### Development Setup
1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run tests to ensure everything works: `pytest tests/ -v`

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Include docstrings for all functions and classes
- Maintain thread safety for all storage operations

## License

This project is created for educational purposes as part of a coding assignment.

**Built with ❤️ using Flask and Python**
