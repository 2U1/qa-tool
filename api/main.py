from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from database import connect_and_init_db, close_db_connection

from domain.vlm import vlm_router
from domain.user import user_router

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connection)


app.include_router(vlm_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"))
app.mount("/images", StaticFiles(directory="../frontend/dist/images"))

@app.get("/")
def index():
    return FileResponse('../frontend/dist/index.html')