from datetime import datetime

from app.dao.text_check import check_for_malicious_code, check_value
from app.tasks.schema import Priority
from app.exceptions import (
    InputError, 
    LenError, 
    ParamIsImmutable, 
    ParamIsNotBool, 
    ParamIsNotDate,
    PriorityError
    )





def input_check(param: str, new_value: str):
    
    mutable_params = ["title", "description", "due_data", "is_completed", "priority"]
    
    
    if param not in mutable_params:
        raise ParamIsImmutable
    
    
    
    # проверка даты
    if param == "due_data": 
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except:
            raise ParamIsNotDate
    
    # проверка bool параметра
    if param == "is_completed": 
        if new_value.lower() not in ["false", "true"]:
            raise ParamIsNotBool
        else:
            if new_value.lower() == "false":
                new_value = False
                return new_value
            else:
                new_value = True
                return new_value
    
    
    # проверка текста
    if param in ["title", "description"]:
        if param == "title" and len(new_value) > 100:
            raise LenError
        if check_value(new_value) and check_for_malicious_code(new_value):
            raise InputError
            
    # проверка приоритета
    if param == "priority":
        try:
            Priority(new_value)
            return True
        except ValueError:
            raise PriorityError