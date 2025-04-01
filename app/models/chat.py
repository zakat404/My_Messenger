import enum
from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base

class ChatType(enum.Enum):
    private = "private"
    group = "group"

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    type = Column(Enum(ChatType), nullable=False)
