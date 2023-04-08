def task_convert(list: dict) -> dict:
    """_summary_

    Args:
        list (dict): Receive a database task 

    Returns:
        dict: The task entered into a python dictionary
    """
    return {"id": str(list["_id"]),
            "username": list["username"],
            "name": list["name"],
            "affair": list["affair"]}