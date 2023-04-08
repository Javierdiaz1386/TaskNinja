from fastapi import APIRouter, Depends, HTTPException
from db.db import database_list
from schemas.schema_task import task_convert
from models.model_task import TaskUser
from models.model_user import UserDB
from routers.user_router import current_user
from bson import ObjectId


task_router = APIRouter(prefix="/tasks",
                        tags=["tasks"]
                        )


@task_router.post("/create")
async def create_task(task: dict, user: UserDB = Depends(current_user)) -> TaskUser:
    """_summary_

    Args:
        task (dict): Task information to save
        user (UserDB): user authenticated

    Returns:
        dict: Task created
    """
    task["username"] = user.username
    task["name"] = user.full_name
    task_insert = database_list.insert_one(task).inserted_id
    task_created = database_list.find_one({"_id": task_insert})
    task_created = task_convert(task_created)
    return TaskUser(**task_created)


@task_router.delete("/delete/{task_id}")
async def delete_task(task_id: str, user: UserDB = Depends(current_user)):
    try:
        task = database_list.find_one({"_id": ObjectId(task_id)})
        if task["username"] == user.username:
            database_list.delete_one({"_id": ObjectId(task_id)})
            return {"messague": "tarea eliminada corectamente"}
    except:
        raise HTTPException(status_code=400, detail="Error al eliminar la tarea")


@task_router.put("/update/{id}")
async def update_task(id: str, task: dict, user: UserDB = Depends(current_user)) -> dict:
    try:
        database_list.update_one({"_id": ObjectId(id)}, {"$set": {"affair": task["affair"]}})
    except:
        raise HTTPException(status_code=400, detail="Id de tarea invalido")
    return {"messgue": "actualziado correctamente"}


@task_router.get("/all")
async def all_task(user: UserDB = Depends(current_user)) -> dict:
    """_summary_

    Args:
        user (str): receives the username to search their tasks

    Returns:
        dict: Returns a list with the tasks of the entered user
    """
    find_task_user = database_list.find({"username": user.username})
    task_user_dict = {"task": [task_convert(i) for i in list(find_task_user)]}
    return task_user_dict
