from fastapi import FastAPI
from app.routes.submit import router as submit_router
from app.routes.summary import router as summary_router
from app.routes.ask import router as ask_router

app = FastAPI(title="GreenPack AI Service")

app.include_router(submit_router)
app.include_router(summary_router)
app.include_router(ask_router)


@app.get("/")
def home():
    return {"message": "GreenPack AI Service Running"}