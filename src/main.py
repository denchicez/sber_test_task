import uvicorn

from src.config import settings
from src.routes import app

if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
