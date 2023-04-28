from fastapi import APIRouter, Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models.model_user import User, UserDB
from db.db import database_user
from schemas.schema_user import user_transform
from jose import jwt, JWTError
from datetime import timedelta, datetime
import bcrypt

ALGORITHM = "HS256"
TOKEN_DURATION = 1
SECRET = "a38996063e4db0b313485d7a7cf690325019d16f5913d2f076a3ec20c42abb44"

user_router = APIRouter(prefix="/user",
                        tags=["user"]
                        )

oauth2 = OAuth2PasswordBearer("/login")


def search_userdb(username: str) -> UserDB:
    """

    Args:
        username: Username to search in db

    Returns:
        UserDb: User with information
    """
    try:
        user = database_user.find_one({"username": username})
        user = user_transform(user)
        return UserDB(**user)
    except:
        raise HTTPException(status_code=400, detail="Usuairo no encontrado")


def search_user(username: str) -> User:
    """

    Args:
        username: User to search in db

    Returns:
        User: User information not id
    """
    try:
        user = database_user.find_one({"username": username})
        return User(**user)
    except:
        raise HTTPException(status_code=400, detail="Usuairo no encontrado")


def auth_user(token: str = Depends(oauth2)) -> str:
    """

    Args:
        token: tokenJWT obtained in /login

    Returns:
        username: return username decode Tokenjwt
    """
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("username")
        return username
    except JWTError:
        raise HTTPException(status_code=400, detail="Error al iniciar sesion")


def current_user(username: str = Depends(auth_user)) -> User:
    """

    Args:
        username: Username obtained on auth_user

    Returns:
        User: object with information the user authenticated
    """
    if username is None:
        raise HTTPException(status_code=400, detail="Usuario no puede ser None")
    user = search_user(username)

    return user


@user_router.post("/create")
async def user_create(user: UserDB) -> User:
    """

    Args:
        user: this is user information to save

    Returns: User created

    """

    v_user = database_user.find_one({"username": user["username"]})
    if isinstance(v_user, dict):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed = bcrypt.hashpw(user["password"].encode(), bcrypt.gensalt())
    user["password"] = hashed
    id_user_created = database_user.insert_one(user).inserted_id
    user_in_db = database_user.find_one({"_id": id_user_created})

    user_in_db = User(**user_in_db)
    return user_in_db


@user_router.post("/login")
async def user_login(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    """

    Args:
        user: form with username and password

    Returns: Token JWT

    """
    user_on_db = search_userdb(user.username)
    print(type("s"))
    if not bcrypt.checkpw(user.password.encode(), user_on_db.password):
        raise HTTPException(status_code=400, detail="Contrasenna incorrecta")

    expire_token = datetime.utcnow() + timedelta(minutes=TOKEN_DURATION)
    access_token = {"sub": user_on_db.full_name,
                    "username": user_on_db.username,
                    "exp": expire_token}
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
            "token_type": "bearer"}


@user_router.get("/me")
async def me_user(user: UserDB = Depends(current_user)):
    return user
