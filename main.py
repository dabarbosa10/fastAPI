from fastapi import FastAPI
from routes import router
from database import create_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(title="Movies API", lifespan=lifespan)
app.include_router(router)


@app.get("/")
def root():
    return {"message": "Welcome to the Movies API"}
