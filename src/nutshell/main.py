import uvicorn
from nutshell.config import settings
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        "src.nutshell.main:app",
        settings.run.host,
        settings.run.port,
        reload=True,
    )
