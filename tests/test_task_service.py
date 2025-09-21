import pytest
from httpx import ASGITransport, AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        request_body = {
            "title": "Test",
                "description": "Desc",
                "category": "electrical",
                "location_id": "room_101",
                "priority": "high"
        } # исходные данные убрать из теста
        user_id = "user_123"

        
        response = await ac.post(f"/api/v1/tasks?created_by={user_id}", json=request_body)

        # далее этап проверки результата ровно один ассерт,  


def asserts ():
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test"
        assert data["status"] == "new"


# подготовка
# три части,



# сделать в тестах чёткую структуру