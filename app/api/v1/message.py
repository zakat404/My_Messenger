# v1 message
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.services.message_service import send_message, read_message
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class SendMessageRequest(BaseModel):
    chat_id: int
    text: str
    idempotency_key: Optional[str] = None

@router.post("/message")
async def send_message_endpoint(
    req: SendMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    msg = await send_message(db, req.chat_id, current_user.id, req.text, req.idempotency_key)
    return {"message_id": msg.id, "status": "sent"}

@router.post("/message/read/{message_id}")
async def read_message_endpoint(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_msg = await read_message(db, message_id)
    if not updated_msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message_id": message_id, "is_read": updated_msg.is_read}
