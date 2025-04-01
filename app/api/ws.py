import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List

from app.auth.security import decode_access_token
from app.db.database import get_db
from app.services.message_service import send_message
from app.services.chat_service import get_chat_details

router = APIRouter()

active_connections: Dict[int, List[WebSocket]] = {}

async def get_user_id_from_token(token: str) -> int:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.WS_1008_POLICY_VIOLATION, detail="Invalid token")
    return int(payload["sub"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    try:
        user_id = await get_user_id_from_token(token)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    if user_id not in active_connections:
        active_connections[user_id] = []
    active_connections[user_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            action = msg.get("action")
            payload = msg.get("payload", {})

            if action == "send_message":
                chat_id = payload.get("chat_id")
                text = payload.get("text")
                idempotency_key = payload.get("idempotency_key")

                chat = await get_chat_details(db, chat_id)
                if not chat:
                    await websocket.send_text(json.dumps({
                        "action": "error",
                        "payload": {"message": f"Chat with id {chat_id} does not exist."}
                    }))
                    continue

                new_msg = await send_message(db, chat_id, user_id, text, idempotency_key)

                for ws_conn in active_connections.get(user_id, []):
                    await ws_conn.send_text(json.dumps({
                        "action": "new_message",
                        "payload": {
                            "id": new_msg.id,
                            "chat_id": new_msg.chat_id,
                            "sender_id": new_msg.sender_id,
                            "text": new_msg.text,
                            "timestamp": str(new_msg.timestamp),
                            "is_read": new_msg.is_read
                        }
                    }))

            elif action == "read":
                message_id = payload.get("message_id")
                await websocket.send_text(json.dumps({
                    "action": "read_ack",
                    "payload": {"message_id": message_id, "status": "read"}
                }))
            else:
                await websocket.send_text(json.dumps({"error": "Unknown action"}))

    except WebSocketDisconnect:
        active_connections[user_id].remove(websocket)
