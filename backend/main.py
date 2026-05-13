from fastapi import FastAPI
from app.routers import router
from app.core.database import Base, engine
from app import models

app = FastAPI(
    title="EastCoders API",
    version="1.0.0"
)

app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "API çalışıyor"}