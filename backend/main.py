from fastapi import FastAPI
from app.routers import router
from app.core.database import Base, engine
from app import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="EastCoders API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "API çalışıyor"}