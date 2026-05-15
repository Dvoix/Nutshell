import uvicorn
from fastapi import FastAPI

from backend.src.api import router as api_router
from backend.src.config import settings

from backend.src.models_registry import *

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "backend.src.main:app",
        settings.run.host,
        settings.run.port,
        reload=True,
    )
