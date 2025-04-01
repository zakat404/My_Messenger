from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.message import Message
from typing import Optional

async def create_message(
    db: AsyncSession,
    chat_id: int,
    sender_id: int,
    text: str,
    idempotency_key: Optional[str] = None
) -> Message:
    new_message = Message(
        chat_id=chat_id,
        sender_id=sender_id,
        text=text,
        idempotency_key=idempotency_key
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message

async def get_message_by_idempotency(db: AsyncSession, sender_id: int, key: str) -> Optional[Message]:
    query = select(Message).where(Message.sender_id == sender_id, Message.idempotency_key == key)
    result = await db.execute(query)
    return result.scalars().first()

async def get_messages_by_chat(
    db: AsyncSession,
    chat_id: int,
    limit: int = 50,
    offset: int = 0
) -> list[Message]:
    query = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.timestamp.asc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()

async def mark_message_read(db: AsyncSession, message_id: int) -> Optional[Message]:
    msg = await db.get(Message, message_id)
    if msg:
        msg.is_read = True
        await db.commit()
        await db.refresh(msg)
    return msg
