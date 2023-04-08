from pydantic import BaseModel

class TaskUser(BaseModel):
    id: str | None
    username: str
    name: str
    affair: str
    
    
    