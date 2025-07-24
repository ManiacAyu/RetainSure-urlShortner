from flask import Flask, jsonify, request, redirect
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import URLMapping, url_store
from app.utils import validate_url, generate_short_code, normalize_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """Shorten a URL"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'URL is required',
                'message': 'Please provide a URL in the request body'
            }), 400
        
        original_url = data['url']
        
        # Normalize and validate URL
        normalized_url = normalize_url(original_url)
        
        if not validate_url(normalized_url):
            return jsonify({
                'error': 'Invalid URL',
                'message': 'Please provide a valid URL'
            }), 400
        
        # Generate short code
        try:
            short_code = generate_short_code()
        except RuntimeError as e:
            return jsonify({
                'error': 'Service temporarily unavailable',
                'message': 'Unable to generate short code. Please try again.'
            }), 500
        
        # Create and store mapping
        mapping = URLMapping(normalized_url, short_code)
        url_store.store_mapping(short_code, mapping)
        
        # Return response
        short_url = f"{request.host_url}{short_code}"
        
        return jsonify({
            'short_code': short_code,
            'short_url': short_url,
            'original_url': normalized_url
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

@app.route('/<short_code>')
def redirect_url(short_code):
    """Redirect to original URL"""
    try:
        # Validate short code format
        if not short_code or not short_code.isalnum() or len(short_code) != 6:
            return jsonify({
                'error': 'Invalid short code',
                'message': 'Short code must be 6 alphanumeric characters'
            }), 400
        
        # Get mapping
        mapping = url_store.get_mapping(short_code)
        
        if not mapping:
            return jsonify({
                'error': 'Not found',
                'message': 'Short URL not found'
            }), 404
        
        # Increment click count
        url_store.increment_clicks(short_code)
        
        # Redirect to original URL
        return redirect(mapping.original_url, code=302)
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """Get analytics for a short code"""
    try:
        # Validate short code format
        if not short_code or not short_code.isalnum() or len(short_code) != 6:
            return jsonify({
                'error': 'Invalid short code',
                'message': 'Short code must be 6 alphanumeric characters'
            }), 400
        
        # Get mapping
        mapping = url_store.get_mapping(short_code)
        
        if not mapping:
            return jsonify({
                'error': 'Not found',
                'message': 'Short URL not found'
            }), 404
        
        # Return analytics
        return jsonify(mapping.to_dict()), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
