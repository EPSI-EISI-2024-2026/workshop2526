# Wigor Services API Documentation

## Overview

This document provides an overview of the Wigor Services API used in the Wigor Schedule Windows application. It outlines the available endpoints, request and response formats, and usage examples to help developers integrate with the API effectively.

## Base URL

The base URL for the Wigor Services API is:

```
https://api.wigorservices.com/v1
```

## Authentication

The API requires authentication via either a username and password or cookies. Ensure that you have valid credentials before making requests.

### Authentication Endpoint

- **Endpoint:** `/auth`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response:**
  - **Success (200):**
    ```json
    {
      "token": "your_auth_token"
    }
    ```
  - **Error (401):**
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

## Schedule Endpoint

To retrieve the user's schedule, use the following endpoint:

- **Endpoint:** `/schedule`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer your_auth_token`
- **Response:**
  - **Success (200):**
    ```json
    {
      "schedule": [
        {
          "date": "2023-10-01",
          "events": [
            {
              "title": "Meeting with team",
              "time": "10:00 AM"
            }
          ]
        }
      ]
    }
    ```
  - **Error (401):**
    ```json
    {
      "error": "Unauthorized access"
    }
    ```

## Usage Example

Here is a simple example of how to authenticate and fetch the schedule using Python:

```python
import requests

# Authenticate
auth_response = requests.post('https://api.wigorservices.com/v1/auth', json={
    'username': 'your_username',
    'password': 'your_password'
})

if auth_response.status_code == 200:
    token = auth_response.json()['token']
    
    # Fetch schedule
    schedule_response = requests.get('https://api.wigorservices.com/v1/schedule', headers={
        'Authorization': f'Bearer {token}'
    })
    
    if schedule_response.status_code == 200:
        schedule = schedule_response.json()
        print(schedule)
    else:
        print('Error fetching schedule:', schedule_response.json())
else:
    print('Authentication failed:', auth_response.json())
```

## Conclusion

This document serves as a guide for developers to interact with the Wigor Services API. Ensure to handle errors appropriately and secure user credentials during the authentication process. For further details, refer to the API documentation provided by Wigor Services.