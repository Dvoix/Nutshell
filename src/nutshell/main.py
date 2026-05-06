import uvicorn
from fastapi import FastAPI

from nutshell.config import settings

from nutshell.links import views 

app = FastAPI()

app.include_router(views.router)

if __name__ == "__main__":
    uvicorn.run(
        "src.nutshell.main:app",
        settings.run.host,
        settings.run.port,
        reload=True,
    )
