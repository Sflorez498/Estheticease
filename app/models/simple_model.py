from pydantic import BaseModel
from typing import Optional

class SimpleResponse(BaseModel):
    message: str
    success: bool
    data: Optional[dict] = None
