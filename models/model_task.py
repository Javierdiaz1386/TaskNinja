from pydantic import BaseModel
from typing import Optional

class TaskUser(BaseModel):
    id: Optional[str]
    username: str
    name: str
    affair: str
    
    
    