from httpx import AsyncClient
import pytest

from datetime import datetime



@pytest.mark.parametrize(
    "title, description, due_data, is_completed, priority, status_code",
    [
        ("title", "No way", datetime(2015, 10, 15), True, "medium", 200),
        ("Second", "No way", datetime(2015, 10, 20), False, "medium", 200),
    ]
)

async def test_add_task(
    title, 
    description, 
    due_data,
    is_completed, 
    priority, 
    status_code, 
    authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/tasks/add_task", json={
        "title": title,
        "description": description,
        "due_data": str(due_data),
        "is_completed": is_completed,
        "priority": priority,
    })
    
    assert response.status_code == status_code
    
    
    
    
@pytest.mark.parametrize("status_code", [(200)])
async def test_get_tasks_count(status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/tasks/tasks_count")
    
    assert response.status_code == status_code
    
    

    