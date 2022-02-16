from pathlib import Path

from pydantic import BaseSettings


class TestSettings(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str
    elastic_host: str = 'localhost'
    elastic_port: int = 9200
    elastic_user: str = 'elastic'
    elastic_scheme: str = 'http'
    elastic_index_film: str = 'movie'
    elastic_index_genre: str = 'genre'
    elastic_index_person: str = 'person'

    class Config:
        env_file = './.env'
