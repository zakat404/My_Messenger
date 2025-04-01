import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "secret"
        }
        reg_response = await ac.post("/api/v1/auth/register", json=register_data)
        assert reg_response.status_code == 200, reg_response.text
        reg_data = reg_response.json()
        assert "id" in reg_data
        assert reg_data["email"] == "testuser@example.com"

        login_response = await ac.post("/api/v1/auth/login", json=register_data)
        assert login_response.status_code == 200, login_response.text
        login_data = login_response.json()
        assert "access_token" in login_data
        assert login_data["token_type"] == "bearer"
