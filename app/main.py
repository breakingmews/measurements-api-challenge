import logging
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .dependencies.database import create_db_and_tables, engine, import_dataset
from .router import measurements, router

logging.config.dictConfig(settings.logging)  # type: ignore[arg-type]
_log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _log.info("Application startup")

    engine.connect()
    create_db_and_tables()
    import_dataset()

    yield
    _log.info("Application shutting down")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(measurements, prefix="/api/v1")
