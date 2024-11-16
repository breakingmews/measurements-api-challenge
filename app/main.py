import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from .config import settings
from .dependencies.database import (
    create_db_and_tables,
    get_measurements_count,
    import_dataset,
)
from .dto import Info

logging.basicConfig(**settings.logging)  # type: ignore[arg-type]
_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _log.info("Application startup")

    create_db_and_tables()
    import_dataset()

    yield
    _log.info("Application shutting down")


app = FastAPI(lifespan=lifespan)


@app.get("/info")
async def info(dataset_size: int = Depends(get_measurements_count)) -> Info:
    _log.error(dataset_size)
    return Info(status="running", dataset_size=dataset_size)
