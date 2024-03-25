import logging

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from src.handlers import get_visited_domains_handler
from src.models import Status

visited_domains_route = APIRouter()


@visited_domains_route.get("/visited_domains", responses={
    200: {
        "model": Status,
        "content": {
            "application/json": {
                "example": {"status": "ok"}
            }
        }
    },
    422: {
        "model": Status,
        "content": {
            "application/json": {
                "example": {"status": f"from and to params can't find"}
            }
        }
    }
})
async def get_visited_domains_route(from_param: int = Query(1545221231, alias="from"),
                                    to_param: int = Query(1545217638, alias="to")) -> JSONResponse:
    logging.info(f"Start getting visited domains from {from_param} till {to_param}")
    return await get_visited_domains_handler(from_param=from_param, to_param=to_param)
