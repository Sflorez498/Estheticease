# API Documentation

## Authentication

### Login
- **Endpoint**: `/token`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

## Users

### Get Current User
- **Endpoint**: `/users/me`
- **Method**: `GET`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "username": "string",
    "email": "string",
    "full_name": "string",
    "disabled": "boolean"
  }
  ```

## Error Codes

- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid input data

## Security

- All endpoints require JWT authentication except `/token`
- Rate limiting is implemented
- CORS is configured for security
