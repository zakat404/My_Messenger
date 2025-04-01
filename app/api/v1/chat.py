from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.chat import ChatType
from app.schemas.chat import ChatCreate
from app.schemas.message import MessageOut
from app.services.chat_service import create_new_chat, get_chat_details
from app.services.message_service import get_chat_history

router = APIRouter()

@router.post("/chat")
async def create_chat_endpoint(
    chat_data: ChatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if chat_data.type == ChatType.group and current_user.id not in chat_data.member_ids:
        chat_data.member_ids.append(current_user.id)

    new_chat = await create_new_chat(
        db, chat_data.name, chat_data.type, chat_data.member_ids
    )
    return {
        "id": new_chat.id,
        "name": new_chat.name,
        "type": new_chat.type.value
    }

@router.get("/history/{chat_id}", response_model=List[MessageOut])
async def get_chat_history_endpoint(
    chat_id: int,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    messages = await get_chat_history(db, chat_id, limit, offset)
    return messages
