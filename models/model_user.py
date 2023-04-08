from pydantic import BaseModel


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    id: str
    password: bytes
