from fastapi import FastAPI

app = FastAPI()

origins = [
    "http://localhost:5173",
]

@app.get("/")
def root():
    return {"message": "Hello World"}