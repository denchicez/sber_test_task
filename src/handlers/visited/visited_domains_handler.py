import logging
from datetime import datetime, timezone

from fastapi import HTTPException
from starlette.responses import JSONResponse

from src.config import settings
from src.models import VisitedDomains, Status
import src.database.mongodb as db


async def get_visited_domains_handler(from_param: int, to_param: int) -> JSONResponse:
    from_datetime = datetime.fromtimestamp(from_param, tz=timezone.utc)
    to_datetime = datetime.fromtimestamp(to_param, tz=timezone.utc)
    query = {
        "created_at": {
            "$gte": from_datetime,
            "$lte": to_datetime
        }
    }
    logging.info(f"Get visited domains from {from_param} to {to_param}")
    try:
        domains = await db.get_uniq_field_by_query(
            collection=settings.visited_domain_collection,
            field="domain",
            query=query
        )
    except HTTPException as err:
        return Status(status=err.detail, status_code=err.status_code).get_response()
    logging.info("Successfully retrieved visited domains")
    return VisitedDomains(domains=domains, status="ok").get_response()
