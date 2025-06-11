from fastapi import HTTPException
from typing import Optional

class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
        error_code: Optional[str] = None,
        headers: Optional[dict] = None
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )
        self.error_code = error_code

class NotFoundException(APIException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail, error_code="NOT_FOUND")

class UnauthorizedException(APIException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail, error_code="UNAUTHORIZED")

class ForbiddenException(APIException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail, error_code="FORBIDDEN")

class ValidationException(APIException):
    def __init__(self, detail: str = "Invalid input"):
        super().__init__(status_code=422, detail=detail, error_code="VALIDATION_ERROR")
