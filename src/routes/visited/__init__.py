from fastapi import APIRouter
from .visited_links_route import visited_links_route
from .visited_domains_route import visited_domains_route

visited_routes = APIRouter(tags=['Visited'])
visited_routes.include_router(visited_links_route)
visited_routes.include_router(visited_domains_route)
