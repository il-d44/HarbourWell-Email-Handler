from dataclasses import dataclass
from typing import Optional 

@dataclass
class Global_State:
    email: Optional[dict] = None
    category: Optional[str] = None
    draft_reply: Optional[str] = None 
    status: Optional[str] = "start"
    error: Optional[str] = None








