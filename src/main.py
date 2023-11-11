from fastapi import FastAPI
from src.routers.items import router

app = FastAPI()
app.include_router(router)

