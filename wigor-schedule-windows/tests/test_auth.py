import unittest
from src.auth import validate_credentials, UserSession

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.valid_username = "test_user"
        self.valid_password = "test_password"
        self.invalid_username = "invalid_user"
        self.invalid_password = "invalid_password"
        self.session = UserSession()

    def test_validate_credentials_with_valid_username(self):
        result = validate_credentials(self.valid_username, self.valid_password)
        self.assertTrue(result)

    def test_validate_credentials_with_invalid_username(self):
        result = validate_credentials(self.invalid_username, self.valid_password)
        self.assertFalse(result)

    def test_validate_credentials_with_invalid_password(self):
        result = validate_credentials(self.valid_username, self.invalid_password)
        self.assertFalse(result)

    def test_user_session_creation(self):
        self.session.create_session(self.valid_username)
        self.assertEqual(self.session.username, self.valid_username)

    def test_user_session_invalidation(self):
        self.session.create_session(self.valid_username)
        self.session.invalidate_session()
        self.assertIsNone(self.session.username)

if __name__ == '__main__':
    unittest.main()