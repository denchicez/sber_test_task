import logging
import re
from datetime import datetime
from typing import List, Set

from pydantic import BaseModel, Field, model_validator, PrivateAttr
from src.config import settings


class VisitedLinks(BaseModel):
    links: List[str] = Field(default_factory=list,
                             description="List of urls that have been visited")
    _created_at: datetime = PrivateAttr(default_factory=datetime.utcnow)
    _domains: Set[str] = set()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "links": [
                        "https://ya.ru/",
                        "https://ya.ru/search/?text=мемы+с+котиками",
                        "https://sber.ru",
                        "https://stackoverflow.com/questions/65724760/how-it-is"
                    ]
                },
                {
                    "urls": [],
                }
            ]
        }
    }

    @model_validator(mode="after")
    def extract_domains(cls, values):
        matched_links = [re.match(settings.regular_url, link) for link in values.links]
        is_correct_link = lambda link: link is None or len(link.groups()) <= settings.regular_url_group
        bad_links = list(filter(is_correct_link, matched_links))
        if bad_links:
            logging.warning(f"Found bad urls")
            raise ValueError(f"urls are not equals {settings.regular_url_standart}")
        values._domains.update([matched_link.group(settings.regular_url_group) for matched_link in matched_links])
        return values

    def get_domains(self) -> Set[str]:
        return self._domains

    def get_created_at(self) -> datetime:
        return self._created_at
