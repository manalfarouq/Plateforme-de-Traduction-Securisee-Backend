from pydantic import BaseModel

class user_schema(BaseModel):
    username: str
    password: str
    role: str  # user  ou admin
    admin_code: str = None # Code requis seulement si role = "admin"