# Configuration settings for the Wigor Schedule application

API_BASE_URL = "https://api.wigorservices.com/v1"
DEFAULT_TIMEOUT = 10  # seconds

# Configuration for authentication
AUTH_ENDPOINT = f"{API_BASE_URL}/auth"
SCHEDULE_ENDPOINT = f"{API_BASE_URL}/schedule"

# Default values
DEFAULT_USERNAME = ""
DEFAULT_PASSWORD = ""

# Function to load configuration from a file (if needed)
def load_config(file_path):
    import json
    try:
        with open(file_path, 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print(f"Configuration file not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the configuration file: {file_path}")
        return {}