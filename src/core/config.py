import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'ShortURL')
PROJECT_HOST = os.getenv('PROJECT_HOST', 'localhost')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

# Security
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "b303982095bb9fc130eed9eeae74f6f3cde6afa5f8584230265f96c6a87be07f77c6f2824924033acce90ad29104f13568796dff6cac1879b9abc6fd943b2c46")   # should be kept secret
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY', "0037837d450770020fd7b831ad21b877a7702c0d18960546d892d05600d869e4a1b0bfbcbc4be89ab2600207e7b27b157d2ac5df32bfb5f3fa8760336761a82e")    # should be kept secret

# База данных
PG_HOST = os.getenv('POSTGRES_HOST', 'localhost')
PG_PORT = os.getenv('POSTGRES_PORT', 5432)
PG_DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
PG_USER_NAME = os.getenv('POSTGRES_USER', 'postgres')
PG_USER_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Jazhby2003')
PG_ENGINE = os.getenv('POSTGRES_ENGINE', 'postgresql+asyncpg')
PG_DSN = f"{PG_ENGINE}://{PG_USER_NAME}:{PG_USER_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

STATIC_DIR = os.getenv('STATIC_DIR', "static")

CONNECTED_SERVERS = {
    "postgres": {
        "host": PG_HOST,
        "port": PG_PORT,
    }
}

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 