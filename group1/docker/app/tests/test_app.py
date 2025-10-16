import sys
import os
import pytest

# Ensure the 'docker/app' directory is on sys.path so 'src' package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as c:
        yield c

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'POUDLARD - Demo App' in rv.data
