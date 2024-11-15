import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from .config import settings
from .dependencies import get_dataset, load_dataset
from .dto import Info

logging.basicConfig(**settings.logging)  # type: ignore[arg-type]
_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        _log.info("Application startup")
        app.state.dataset = await load_dataset()
    except Exception as e:
        _log.error("Failed to load dataset during startup")
        raise e

    yield
    _log.info("Application shutting down")


app = FastAPI(lifespan=lifespan)


@app.get("/info")
async def info(dataset=Depends(get_dataset)) -> Info:
    return Info(status="running", dataset_size=len(dataset))
