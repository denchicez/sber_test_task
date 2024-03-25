import logging

from pymongo.errors import InvalidURI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import HTTPException
from urllib.parse import quote
from src.config.settings import settings


def get_client():
    url = f"mongodb://{quote(settings.mongodb_user)}:{quote(settings.mongodb_pw)}@{quote(settings.mongodb_hosts)}" \
          f"/?authSource={quote(settings.mongodb_db)}"

    if not settings.mongodb_user:
        url = f"mongodb://{quote(settings.mongodb_hosts)}/?authSource={quote(settings.mongodb_db)}"

    try:
        if settings.mongodb_tls:
            client = AsyncIOMotorClient(url, tls=settings.mongodb_tls, tlsCAFile=settings.mongodb_tls_ca_file)
        else:
            client = AsyncIOMotorClient(url)
    except InvalidURI as e:
        logging.warning(f"Problem with connection to database : {e}")
        client = None
    return client


mongo_db_client = get_client()


def get_db():
    try:
        return mongo_db_client[settings.mongodb_db]
    except Exception as e:
        logging.warning(f"Problem with connection to database : {e}")


db = get_db()


async def create_or_check_indexes(collection_name: str, index_cur: list[tuple[str, int]]):
    collection = db[collection_name]
    index_info = await collection.index_information()
    if index_cur in [index["key"] for index in index_info.values()]:
        logging.info(f"Index {index_cur} in collection {collection_name} already successfully created.")
    else:
        await collection.create_index(index_cur)
        logging.info(f"Index {index_cur} in collection {collection_name} successfully created.")


async def get_uniq_field_by_query(collection: str, field: str, query: dict) -> list:
    try:
        return await db[collection].distinct(field, query)
    except Exception as e:
        message = f"Error while retrieving unique objects {field} on query {query}: {str(e)}"
        logging.warning(message)
        raise HTTPException(status_code=500, detail=message)


async def inset_item(item: dict, collection) -> str:
    try:
        # Попытка вставить объект
        result = await db[collection].insert_one(item)
        if result.inserted_id:
            message = f"Object successfully inserted {result.inserted_id}"
            logging.info(message)
            return str(result.inserted_id)
        else:
            # Ошибка вставки объекта
            message = f"Error of insert {item}"
            logging.warning(message)
            raise HTTPException(status_code=500, detail=message)
    except Exception as e:
        message = f"Error of insert {item}: {str(e)}"
        logging.warning(message)
        raise HTTPException(status_code=500, detail=message)
