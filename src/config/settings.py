from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    # app settings
    host: str = "0.0.0.0"
    port: int = 8000

    # URL description
    regular_url_standart: str = "RFC 3986 (http://tools.ietf.org/html/rfc3986)"
    regular_url: str = '(((\w+):)?\/\/)?((\w+)(:\w+)?@)?((\w|\.|\-)+\.\w+)(:\d+)?[^"]*'
    regular_url_group: int = 7

    # Mongo DB
    mongodb_hosts: str = "localhost:27017"
    mongodb_db: str = "test"
    mongodb_tls: bool = False
    mongodb_user: str = ""
    mongodb_pw: str = ""
    mongodb_tls_ca_file: str = ""
    visited_domain_collection: str = "visited_domain"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = BaseAppSettings()
