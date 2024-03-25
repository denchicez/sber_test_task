from datetime import datetime
import pytest
from mongomock_motor import AsyncMongoMockClient

from src.models import VisitedLinks, VisitedDomains
from src.routes.visited.visited_domains_route import get_visited_domains_route
from src.routes.visited.visited_links_route import save_visited_links_route


@pytest.mark.asyncio
async def test_base_visited_domains_route(mocker):
    db = AsyncMongoMockClient()['test']
    mocker.patch('src.database.mongodb.db', db)
    visited_links = VisitedLinks(links=[
        "https://ya.ru/",
        "https://ya.ru/search/?text=мемы+с+котиками",
        "https://sber.ru",
        "https://stackoverflow.com/questions/65724760/how-it-is"
    ])
    visited_links._created_at = datetime(2024, 3, 24, 23, 0, 0, 0)
    await save_visited_links_route(visited_links=visited_links)
    created_tmstmp = int(visited_links.get_created_at().strftime('%s'))

    response = await get_visited_domains_route(from_param=created_tmstmp, to_param=created_tmstmp)
    assert response.status_code == 200
    assert set(VisitedDomains.model_validate_json(response.body).domains) == {'stackoverflow.com', 'sber.ru', 'ya.ru'}

    response = await get_visited_domains_route(from_param=created_tmstmp + 1, to_param=created_tmstmp + 1)
    assert response.status_code == 200
    assert len(VisitedDomains.model_validate_json(response.body).domains) == 0

    response = await get_visited_domains_route(from_param=created_tmstmp - 1, to_param=created_tmstmp - 1)
    assert response.status_code == 200
    assert len(VisitedDomains.model_validate_json(response.body).domains) == 0
