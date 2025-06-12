# Documentación de la API Estheticease

## Autenticación

### Iniciar Sesión
- **Endpoint**: `/token`
- **Método**: `POST`
- **Cuerpo de la Solicitud**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Respuesta**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

¡Importante! El token obtenido debe incluirse en las siguientes peticiones como `Bearer token` en el header `Authorization`.

## Usuarios

### Obtener Usuario Actual
- **Endpoint**: `/users/me`
- **Método**: `GET`
- **Autenticación**: Requerida
- **Respuesta**:
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
