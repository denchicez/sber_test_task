from datetime import datetime

from mongomock_motor import AsyncMongoMockClient
import pytest
from pydantic import ValidationError

from src.config import settings
from src.models import VisitedLinks, Status, Domain
from src.routes.visited.visited_links_route import save_visited_links_route


@pytest.mark.asyncio
async def test_base_save_visited_links_route(mocker):
    db = AsyncMongoMockClient()['test']
    mocker.patch('src.database.mongodb.db', db)

    visited_links = VisitedLinks(links=[
        "https://ya.ru/",
        "https://ya.ru/search/?text=мемы+с+котиками",
        "https://sber.ru",
        "https://stackoverflow.com/questions/65724760/how-it-is"
    ])
    visited_links._created_at = datetime(2024, 3, 24, 23, 0, 0, 0)
    response = await save_visited_links_route(visited_links=visited_links)
    assert response.status_code == 200
    assert Status.model_validate_json(response.body) == Status(status="ok")

    domains_in_db = []
    async for domain in db.get_collection(settings.visited_domain_collection).find().sort([("domain", -1)]):
        domains_in_db.append(Domain.model_validate(domain))
    need_in_db = [
        Domain(domain="ya.ru", created_at=visited_links.get_created_at()),
        Domain(domain="stackoverflow.com", created_at=visited_links.get_created_at()),
        Domain(domain="sber.ru", created_at=visited_links.get_created_at()),
    ]
    assert domains_in_db == need_in_db


@pytest.mark.asyncio
async def test_strange_save_visited_links_route(mocker):
    db = AsyncMongoMockClient()['test']
    mocker.patch('src.database.mongodb.db', db)

    visited_links = VisitedLinks(links=[])
    visited_links._created_at = datetime(2024, 3, 24, 23, 0, 0, 0)
    domains_in_db = []
    async for domain in db.get_collection(settings.visited_domain_collection).find().sort([("domain", -1)]):
        domains_in_db.append(Domain.model_validate(domain))
    response = await save_visited_links_route(visited_links=visited_links)
    assert response.status_code == 200
    assert Status.model_validate_json(response.body) == Status(status="ok")
    assert domains_in_db == []


@pytest.mark.asyncio
async def test_strange_save_visited_links_route(mocker):
    db = AsyncMongoMockClient()['test']
    mocker.patch('src.database.mongodb.db', db)

    visited_links = VisitedLinks(links=[])
    visited_links._created_at = datetime(2024, 3, 24, 23, 0, 0, 0)
    domains_in_db = []
    async for domain in db.get_collection(settings.visited_domain_collection).find().sort([("domain", -1)]):
        domains_in_db.append(Domain.model_validate(domain))
    response = await save_visited_links_route(visited_links=visited_links)
    assert response.status_code == 200
    assert Status.model_validate_json(response.body) == Status(status="ok")
    assert domains_in_db == []


@pytest.mark.asyncio
async def test_bad_links_save_visited_links_route(mocker):
    db = AsyncMongoMockClient()['test']
    mocker.patch('src.database.mongodb.db', db)
    with pytest.raises(ValidationError):
        VisitedLinks(links=[
            "https://ya.ru/",
            "https://ya.ru/search/?text=мемы+с+котиками",
            "https://sber.ru",
            "i don't know what it"
        ])
