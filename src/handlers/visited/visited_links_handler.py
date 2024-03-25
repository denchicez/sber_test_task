import asyncio
import logging
from typing import Set

from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.config import settings
import src.database.mongodb as db
from src.models import VisitedLinks, Status, Domain


async def save_visited_links_handler(visited_links: VisitedLinks) -> JSONResponse:
    str_domains: Set[str] = visited_links.get_domains()
    created_at = visited_links.get_created_at()
    save_tasks = []
    for str_domain in str_domains:
        domain = Domain(domain=str_domain, created_at=created_at)
        save_tasks.append(db.inset_item(domain.model_dump(), settings.visited_domain_collection))
    results = await asyncio.gather(*save_tasks, return_exceptions=True)
    bad_results = list(filter(lambda result: type(result) is HTTPException, results))
    if bad_results:
        message_format = ",".join([bad_result.detail for bad_result in bad_results])
        return Status(status=message_format, status_code=500).get_response()
    logging.info("Successfully saved visited links")
    return Status(status="ok", status_code=200).get_response()
