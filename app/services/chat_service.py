from app.models.chat import ChatType
from app.repositories.chat_repo import create_chat, get_chat
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

async def create_new_chat(db: AsyncSession, name: str, chat_type: ChatType, member_ids: List[int]):
    return await create_chat(db, name, chat_type, member_ids)

async def get_chat_details(db: AsyncSession, chat_id: int):
    return await get_chat(db, chat_id)
