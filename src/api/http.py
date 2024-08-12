import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.applications import Starlette
from api.v1.routers import ping, async_ping, read_state
from starlette.applications import Starlette
from elasticapm.contrib.starlette import ElasticAPM

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: Starlette):
    logger.info('Started an application.')
    yield

app = FastAPI()
app.add_middleware(ElasticAPM)

app.include_router(ping.router)
app.include_router(async_ping.router)
app.include_router(read_state.router)