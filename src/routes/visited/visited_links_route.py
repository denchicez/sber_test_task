import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.config import settings
from src.models import VisitedLinks, Status
from src.handlers import save_visited_links_handler

visited_links_route = APIRouter()


@visited_links_route.post("/visited_links", responses={
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
                "example": {"status": f"links are not correct! Format will be {settings.regular_url_standart}"}
            }
        }
    }
})
async def save_visited_links_route(visited_links: VisitedLinks) -> JSONResponse:
    logging.info(f"Start save visited links: {visited_links}")
    return await save_visited_links_handler(visited_links=visited_links)
