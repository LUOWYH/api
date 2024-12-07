from fastapi import FastAPI
from app.api.v1 import Yiyan

app = FastAPI()

app.include_router(Yiyan.router, prefix="/api/v1")