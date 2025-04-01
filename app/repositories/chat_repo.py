from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.chat import Chat, ChatType
from app.models.group import chat_members
from typing import List

async def create_chat(db: AsyncSession, name: str, chat_type: ChatType, member_ids: List[int]) -> Chat:
    new_chat = Chat(name=name, type=chat_type)
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)

    if chat_type == ChatType.group and member_ids:
        await add_members_to_chat(db, new_chat.id, member_ids)

    return new_chat

async def add_members_to_chat(db: AsyncSession, chat_id: int, member_ids: List[int]):
    for user_id in member_ids:
        await db.execute(chat_members.insert().values(chat_id=chat_id, user_id=user_id))
    await db.commit()

async def get_chat(db: AsyncSession, chat_id: int) -> Chat:
    return await db.get(Chat, chat_id)
