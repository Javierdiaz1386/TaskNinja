def user_transform(user: dict) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "full_name": user["full_name"],
            "password": user["password"],
            "email": user["email"],
            "disable": user["disable"]
            }
