import pytest
import json
import sys
import os

if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.models import url_store

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        url_store._mappings.clear()
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_api_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_shorten_url_success(client):
    url_data = {'url': 'https://www.example.com'}
    response = client.post('/api/shorten', 
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert 'original_url' in data
    assert len(data['short_code']) == 6
    assert data['original_url'] == 'https://www.example.com'

def test_shorten_url_without_scheme(client):
    url_data = {'url': 'www.example.com'}
    response = client.post('/api/shorten',
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['original_url'] == 'https://www.example.com'

def test_shorten_url_invalid_url(client):
    url_data = {'url': 'not-a-valid-url'}
    response = client.post('/api/shorten',
                          data=json.dumps(url_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_shorten_url_missing_url(client):
    response = client.post('/api/shorten',
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_redirect_success(client):
    url_data = {'url': 'https://www.example.com'}
    shorten_response = client.post('/api/shorten',
                                  data=json.dumps(url_data),
                                  content_type='application/json')
    
    short_code = shorten_response.get_json()['short_code']
    
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.location == 'https://www.example.com'

def test_redirect_not_found(client):
    response = client.get('/abcd12')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_redirect_invalid_short_code(client):
    response = client.get('/abc')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_stats_success(client):
    url_data = {'url': 'https://www.example.com'}
    shorten_response = client.post('/api/shorten',
                                  data=json.dumps(url_data),
                                  content_type='application/json')
    
    short_code = shorten_response.get_json()['short_code']
    
    client.get(f'/{short_code}')
    client.get(f'/{short_code}')
    
    response = client.get(f'/api/stats/{short_code}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['url'] == 'https://www.example.com'
    assert data['clicks'] == 2
    assert 'created_at' in data

def test_stats_not_found(client):
    response = client.get('/api/stats/abcd12')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_concurrent_access(client):
    url_data = {'url': 'https://www.example.com'}
    shorten_response = client.post('/api/shorten',
                                  data=json.dumps(url_data),
                                  content_type='application/json')
    
    short_code = shorten_response.get_json()['short_code']
    
    for _ in range(5):
        response = client.get(f'/{short_code}')
        assert response.status_code == 302
    
    stats_response = client.get(f'/api/stats/{short_code}')
    data = stats_response.get_json()
    assert data['clicks'] == 5
