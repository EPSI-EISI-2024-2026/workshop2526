import pytest

@pytest.fixture(scope="session")
def api_client():
    from src.wigor_client import WigorClient
    client = WigorClient(username="test_user", password="test_password")
    yield client
    client.logout()  # Ensure logout after tests are done

@pytest.fixture
def sample_schedule():
    return {
        "courses": [
            {"name": "Math", "time": "09:00"},
            {"name": "Science", "time": "10:00"},
        ]
    }