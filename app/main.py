from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from database import connect_and_init_db, close_db_connection

from domain.qa import qa_router

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
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


app.include_router(qa_router.router)