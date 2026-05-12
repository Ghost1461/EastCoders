from fastapi import FastAPI
from src.routes import router

app = FastAPI(
    title="EastCoders API",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "API çalışıyor"}