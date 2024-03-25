import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .visited import visited_routes
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from src.models import Status
from src.database.mongodb import create_or_check_indexes
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting server")
    await create_or_check_indexes(collection_name=settings.visited_domain_collection, index_cur=[('created_at', 1)])
    yield
    logging.info("Shutdown server")



app = FastAPI(lifespan=lifespan)
app.include_router(visited_routes)


@app.exception_handler(RequestValidationError)
def handle_validation_error(request, exc) -> JSONResponse:
    return Status(status=exc.errors()[0]["msg"], status_code=HTTP_422_UNPROCESSABLE_ENTITY).get_response()
