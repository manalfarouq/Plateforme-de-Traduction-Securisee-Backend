from pydantic import BaseModel
from typing import Optional

class user_schema(BaseModel):
    username: str
    password: str
    role: str  # user  ou admin
    admin_code: Optional[str] = None  # Code requis seulement si role = "admin"