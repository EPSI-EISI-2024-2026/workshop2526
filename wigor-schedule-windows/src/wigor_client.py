class WigorClient:
    def __init__(self, username=None, cookies=None):
        self.username = username
        self.cookies = cookies
        self.api_base_url = "https://api.wigorservices.com"
        self.session = None

    def authenticate(self):
        if self.username:
            # Logic for authenticating with username
            self.session = self._authenticate_with_username(self.username)
        elif self.cookies:
            # Logic for authenticating with cookies
            self.session = self._authenticate_with_cookies(self.cookies)
        else:
            raise ValueError("No credentials provided for authentication.")

    def _authenticate_with_username(self, username):
        # Placeholder for actual authentication logic
        # This should return a session object or token
        return f"Session for {username}"

    def _authenticate_with_cookies(self, cookies):
        # Placeholder for actual cookie-based authentication logic
        # This should return a session object or token
        return f"Session with cookies: {cookies}"

    def fetch_schedule(self):
        if not self.session:
            raise RuntimeError("Client is not authenticated. Please authenticate first.")
        
        # Logic to fetch the schedule from the API
        schedule_endpoint = f"{self.api_base_url}/schedule"
        response = self._make_api_request(schedule_endpoint)
        return response

    def _make_api_request(self, endpoint):
        # Placeholder for actual API request logic
        # This should handle GET requests and return the response
        return f"Fetched data from {endpoint}"