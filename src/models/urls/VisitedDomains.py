from typing import List
from pydantic import Field
from src.models.status import Status


class VisitedDomains(Status):
    domains: List[str] = Field(default_factory=list,
                               description="List of domains that have been visited")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "domains": [
                        "ya.ru",
                        "sber.ru",
                        "stackoverflow.com"
                    ],
                    "status": "ok"
                },
                {
                    "domains": [],
                    "status": "ok"
                }
            ]
        }
    }
