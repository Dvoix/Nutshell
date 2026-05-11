import uvicorn
from fastapi import FastAPI

from nutshell.api import router as api_router
from nutshell.config import settings

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.nutshell.main:app",
        settings.run.host,
        settings.run.port,
        reload=True,
    )
