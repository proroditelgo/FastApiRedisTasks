import json
from fastapi import APIRouter, Depends, Request, Response

from app.exceptions import TaskIsNotPresent
from app.tasks.schema import STasks
from app.tasks.dao import TaskDAO
from app.users.dependencies import get_current_user




router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


#  добавление задачи
@router.post("/add_task")
async def add_task(task: STasks, current_user: list = Depends(get_current_user)):

    user_id = current_user["user_id"]
    task_id: int = 1
    
    while await TaskDAO.find_one(f"{user_id}_{task_id}"):
        task_id += 1
    
    
    task: dict = {
        "user_id": int(user_id),
        
        "title": task.title,
        "description": task.description,
        "due_data": str(task.due_data),
        "is_completed": task.is_completed,
        "priority": task.priority.name,
        
        "task_id": int(task_id),
    }
    
    
    
    data_json = json.dumps(task)

    
    await TaskDAO.add_task(data=data_json, user_id=user_id, task_id=task_id)
    
    return f"Задача номер {task_id} занесена"



# выгрузка числа всех задач пользователя  
@router.get("/tasks_count")
async def get_all_tasks(current_user: list = Depends(get_current_user)):
    
    
    user_id = current_user["user_id"]
    
    return await TaskDAO.get_all_tasks_count(user_id)
    
    
        
    
# выгрузка задачи по айди
@router.get("/get_task_by_id")
async def get_task_by_id(task_id: int, current_user: list = Depends(get_current_user)):
    
    
    user_id = current_user["user_id"]
    
    task = await TaskDAO.find_one(f"{user_id}_{task_id}")
    
    if not task:
        raise TaskIsNotPresent
    
    data_dict = json.loads(task)
    
    return data_dict


# выгрузка всех задач пользователя
@router.get("/get_all_user_tasks")
async def get_all_user_tasks(
                            request: Request, 
                            response: Response, 
                            task_count: int, 
                            current_user: list = Depends(get_current_user)
                            ):
    
    
    user_id = current_user["user_id"]
    
    task_viewed = int(request.cookies.get("task_viewed"))
    
    # если нет просмотров - выставляется начальное значение в 0
    if not task_viewed:
        task_viewed = 0
        
    # выгрузка данных
    result = await TaskDAO.get_all_user_tasks(user_id=user_id, task_count=task_count, task_viewed=task_viewed)
    dict_values = result[0]
    end_of_data = result[1]
    
    # если переменная с концом данных о задачах False - прибавляются просмотры
    # если True - просмотры обнуляются для последующей итерации
    if not end_of_data:
        task_viewed += int(task_count)
        response.set_cookie("task_viewed", task_viewed, httponly=True)
    else:
        response.set_cookie("task_viewed", 0, httponly=True)
    
    
    return dict_values



# изменение параметров задачи
@router.get("/update_task")
async def update_task(task_id: int, current_user: list = Depends(get_current_user)):
    
    
    user_id = current_user["user_id"]
    
    task = await TaskDAO.find_one(f"{user_id}_{task_id}")
    
    if not task:
        raise TaskIsNotPresent
    
    data_dict = json.loads(task)
    
    return data_dict



# удаление задачи
@router.delete("/delete_task")
async def delete_task(task_id: int, current_user: list = Depends(get_current_user)):
    
    user_id = current_user["user_id"]
    
    
    if not await TaskDAO.find_one(f"{user_id}_{task_id}"):
        raise TaskIsNotPresent

    
    return await TaskDAO.delete(f"{user_id}_{task_id}")