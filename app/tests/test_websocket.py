import pytest
import json
from httpx import AsyncClient, WebSocketDisconnect
from app.main import app

@pytest.mark.asyncio
async def test_websocket_echo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        login_data = {
            "email": "testuser@example.com",
            "password": "secret",
            "name": "Test User"
        }
        login_response = await ac.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["access_token"]

    # Подключаемся по WebSocket
    async with AsyncClient(app=app, base_url="http://test") as ac:
        try:
            ws = await ac.ws_connect(f"/ws?token={token}")
            await ws.send_json({
                "action": "send_message",
                "payload": {"chat_id": 1, "text": "Hello WebSocket!"}
            })
            data = await ws.receive_json()
            assert data["action"] == "new_message"
            assert data["payload"]["text"] == "Hello WebSocket!"
        except WebSocketDisconnect:
            pytest.fail("WebSocket disconnected unexpectedly")
