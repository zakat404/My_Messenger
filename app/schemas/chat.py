from pydantic import BaseModel
from app.models.chat import ChatType

class ChatCreate(BaseModel):
    name: str
    type: ChatType
    member_ids: list[int] = []
