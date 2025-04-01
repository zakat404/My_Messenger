import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_send_message_without_auth():
    async with AsyncClient(app=app, base_url="http://test") as ac:

        response = await ac.post("/api/v1/message", json={
            "chat_id": 1,
            "sender_id": 1,
            "text": "Hello!",
            "idempotency_key": "unique-key-123"
        })
    assert response.status_code == 401
