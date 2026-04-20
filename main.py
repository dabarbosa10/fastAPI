from fastapi import FastAPI
from routes import router

app = FastAPI(title="Movies API")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the Movies API"}

