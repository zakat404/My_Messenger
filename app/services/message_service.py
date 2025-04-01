from app.repositories.message_repo import (
    create_message,
    get_message_by_idempotency,
    get_messages_by_chat,
    mark_message_read
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import Optional

async def send_message(
    db: AsyncSession,
    chat_id: int,
    sender_id: int,
    text: str,
    idempotency_key: Optional[str] = None
):
    if idempotency_key:
        existing = await get_message_by_idempotency(db, sender_id, idempotency_key)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate message"
            )
    return await create_message(db, chat_id, sender_id, text, idempotency_key)

async def get_chat_history(db: AsyncSession, chat_id: int, limit: int = 50, offset: int = 0):
    return await get_messages_by_chat(db, chat_id, limit, offset)

async def read_message(db: AsyncSession, message_id: int):
    return await mark_message_read(db, message_id)
