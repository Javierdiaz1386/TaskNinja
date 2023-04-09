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
async def create_task(task: dict,
                      user: UserDB = Depends(current_user)) -> TaskUser:
    """_summary_

    Args:
        task (dict): Task information to save
        user (UserDB): user authenticated

    Returns:
        TaskUser: Task created
    """
    task["username"] = user.username
    task["name"] = user.full_name
    task_insert = database_list.insert_one(task).inserted_id
    task_created = database_list.find_one({"_id": task_insert})
    task_created = task_convert(task_created)
    return TaskUser(**task_created)


@task_router.delete("/delete/{task_id}")
async def delete_task(task_id: str, user: UserDB = Depends(current_user)) -> dict:
    """

    Args:
        task_id (str): this is id task to delete
        user (UserDB):  user authenticated

    Returns:
        messague (dict): Confirmation delete
    """
    try:
        task = database_list.find_one({"_id": ObjectId(task_id)})
        if task["username"] == user.username:
            database_list.delete_one({"_id": ObjectId(task_id)})
            messague = {"messague": "task delete"}
            return messague
        else:
            return {"messague": "this task does not belong to you"}
    except:
        raise HTTPException(status_code=400, detail="Error to delete taks")


@task_router.put("/update/{id}")
async def update_task(id: str, task: dict, user: UserDB = Depends(current_user)) -> dict:
    """

    Args:
        id (str): this is id the task to update
        task (dict): New information for task
        user (UserDB): User authenticated

    Returns:
        messague (dict): Confirmation update
    """
    try:
        task_db = database_list.find_one({"_id": ObjectId(id)})
        task_db = task_convert(task_db)
        if task_db["username"] == user.username:
            database_list.update_one({"_id": ObjectId(id)}, {"$set": {"affair": task["affair"]}})

            return {"messgue": "task update"}
        else:
            return {"messague": "this task does not belong to you"}
    except HTTPException:
        raise HTTPException(status_code=400, detail="Task id invalid")



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
