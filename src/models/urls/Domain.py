from datetime import datetime

from pydantic import BaseModel, Field


class Domain(BaseModel):
    domain: str = Field(default_factory=str,
                        description="List of urls that have been visited")
    created_at: datetime
