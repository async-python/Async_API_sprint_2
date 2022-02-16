import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv

from core.logger import LOGGING

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

load_dotenv()

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'movies')

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
ELASTIC_USER = os.getenv('ELASTIC_USER')
ELASTIC_PASSWORD = os.getenv('ELASTIC_PASSWORD')
ELASTIC_INDEX_FILM = os.getenv('ELASTIC_INDEX_FILM', 'movie')
