import json
from fastapi import APIRouter, Depends

from app.tasks.schema import STasks
from app.tasks.dao import TaskDAO
from app.users.dependencies import get_current_user




router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)



@router.post("/add_task")
async def add_task(task: STasks, current_user: list = Depends(get_current_user)):

    user_id = current_user["user_id"]
    task_id: int = await TaskDAO.all_tasks_count(user_id)+1
    
    
    task: dict = {
        "user_id": int(user_id),
        
        "title": task.title,
        "description": task.description,
        "due_data": str(task.due_data),
        "is_completed": task.is_completed,
        "priority": str(task.priority),
        
        "task_id": int(task_id),
    }
    
    print(task)
    print("*"*50)
    print("*"*50)
    print("*"*50)
    
    
    data_json = json.dumps(task)

    
    await TaskDAO.add_task(data=data_json, user_id=user_id, task_id=task_id)
    
    return f"Задача номер {task_id} занесена"




@router.post("/all_task")
async def add_task(current_user: list = Depends(get_current_user)):
    
    
    user_id = current_user["user_id"]
    
    return await TaskDAO.all_tasks_count(user_id)