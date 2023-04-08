from fastapi import FastAPI
from routers.task_router import task_router
from routers.user_router import user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)
origins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def home() -> dict:
    return {
        "messague": "this is home"
    }
