import unittest
from unittest.mock import patch, MagicMock
from src.wigor_client import WigorClient

class TestWigorClient(unittest.TestCase):

    @patch('src.wigor_client.requests.get')
    def test_fetch_schedule_success(self, mock_get):
        # Arrange
        client = WigorClient('username', 'password')
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'schedule': 'mock_schedule_data'}
        mock_get.return_value = mock_response

        # Act
        schedule = client.fetch_schedule()

        # Assert
        self.assertEqual(schedule, {'schedule': 'mock_schedule_data'})
        mock_get.assert_called_once_with('https://api.wigorservices.com/schedule', auth=('username', 'password'))

    @patch('src.wigor_client.requests.get')
    def test_fetch_schedule_failure(self, mock_get):
        # Arrange
        client = WigorClient('username', 'password')
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Act & Assert
        with self.assertRaises(Exception) as context:
            client.fetch_schedule()
        self.assertEqual(str(context.exception), 'Failed to fetch schedule: 404')

    @patch('src.wigor_client.requests.post')
    def test_authenticate_success(self, mock_post):
        # Arrange
        client = WigorClient('username', 'password')
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'token': 'mock_token'}
        mock_post.return_value = mock_response

        # Act
        token = client.authenticate()

        # Assert
        self.assertEqual(token, 'mock_token')
        mock_post.assert_called_once_with('https://api.wigorservices.com/auth', json={'username': 'username', 'password': 'password'})

    @patch('src.wigor_client.requests.post')
    def test_authenticate_failure(self, mock_post):
        # Arrange
        client = WigorClient('username', 'password')
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        # Act & Assert
        with self.assertRaises(Exception) as context:
            client.authenticate()
        self.assertEqual(str(context.exception), 'Authentication failed: 401')

if __name__ == '__main__':
    unittest.main()