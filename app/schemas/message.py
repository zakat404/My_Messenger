from pydantic import BaseModel
from datetime import datetime

class MessageOut(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
    is_read: bool


    class Config:
        from_attributes = True
