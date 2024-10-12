import json
from fastapi import APIRouter, Depends, Request, Response
from pydantic import Json
from datetime import date, datetime

from app.dao.text_check import check_value, check_for_malicious_code
from app.exceptions import (
    TaskIsNotPresent, 
    ParamIsImmutable, 
    ParamIsNotDate,
    ParamIsNotBool,
    InputError,
    LenError
    )
from app.tasks.input_check import input_check
from app.tasks.schema import STasks
from app.tasks.dao import TaskDAO
from app.users.dependencies import get_current_user




router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"]
)


# ===========ДОБАВЛЕНИЕ ЗАДАЧИ======================
@router.post("/add_task")
async def add_task(task: STasks, current_user: list = Depends(get_current_user)):

    user_id = current_user["user_id"]
    task_id: int = 1
    
    while await TaskDAO.find_one(f"{user_id}_{task_id}"):
        task_id += 1
    
    
    task: dict = {
        "user_id": int(user_id),
        
        "title": task.title,
        "description": str(task.description),
        "due_data": str(task.due_data),
        "is_completed": task.is_completed,
        "priority": task.priority.value,
        
        "task_id": int(task_id),
    }
    
    
    
    data_json = json.dumps(task)

    
    await TaskDAO.add_task(data=data_json, user_id=user_id, task_id=task_id)
    
    return f"Задача номер {task_id} занесена"



# =====ВЫГРУЗКА ЧИСЛА ВСЕХ ЗАДАЧ ПОЛЬЗОВАТЕЛЯ====================  
@router.get("/tasks_count")
async def get_all_tasks(current_user: list = Depends(get_current_user)):
    
    
    user_id = current_user["user_id"]
    
    return await TaskDAO.get_all_tasks_count(user_id)
    
    
        
    
# =============ВЫГРУЗКА ЗАДАЧИ ПО АЙДИ======================
@router.get("/get_task_by_id")
async def get_task_by_id(task_id: int, current_user: list = Depends(get_current_user)):
    
    
    user_id = current_user["user_id"]
    
    task = await TaskDAO.find_one(f"{user_id}_{task_id}")
    
    if not task:
        raise TaskIsNotPresent
    
    data_dict = json.loads(task)
    
    return data_dict


# ======ВЫГРУЗКА ВСЕХ ЗАДАЧ ПОЛЬЗОВАТЕЛЯ=====================
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



# =========ИЗМЕНЕНИЕ ПАРАМЕТРОВ ЗАДАЧИ==============
@router.put("/update_task")
async def update_task(task_id: int, param: str, new_value: str, current_user: list = Depends(get_current_user)):
    
    user_id = current_user["user_id"]
    # выгрузка задачи и проверка на её наличие
    task = await TaskDAO.find_one(f"{user_id}_{task_id}")
    
    
    if not task:
        raise TaskIsNotPresent
    
    
    data_dict = json.loads(task)
    
    
    if param == "is_completed":
        new_value = input_check(param=param, new_value=new_value)
    else:
        input_check(param=param, new_value=new_value)

    
    data_dict[param] = new_value
            
    data_json = json.dumps(data_dict)

    await TaskDAO.add_task(data=data_json, user_id=user_id, task_id=task_id)    
    return f"Задача номер {task_id} изменена"
    




# =============УДАЛЕНИЕ ЗАДАЧИ==========================
@router.delete("/delete_task")
async def delete_task(task_id: int, current_user: list = Depends(get_current_user)):
    
    user_id = current_user["user_id"]
    
    
    if not await TaskDAO.find_one(f"{user_id}_{task_id}"):
        raise TaskIsNotPresent

    
    return await TaskDAO.delete(f"{user_id}_{task_id}")