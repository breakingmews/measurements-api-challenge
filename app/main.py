from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from .dependencies import get_dataset, load_dataset
from .dto import Info


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Application startup")
        app.state.dataset = await load_dataset()
    except Exception as e:
        print("Failed to load dataset during startup")
        raise e

    yield
    print("Application shutting down")


app = FastAPI(lifespan=lifespan)


@app.get("/info")
async def info(dataset=Depends(get_dataset)) -> Info:
    return Info(status="running", dataset_size=len(dataset))
