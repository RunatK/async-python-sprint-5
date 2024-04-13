import os

PG_HOST = os.getenv('POSTGRES_HOST', 'localhost')
PG_PORT = os.getenv('POSTGRES_PORT', 5432)
PG_DB_NAME = os.getenv('POSTGRES_DB', 'postgres')
PG_USER_NAME = os.getenv('POSTGRES_USER', 'postgres')
PG_USER_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Jazhby2003')
PG_ENGINE = os.getenv('POSTGRES_ENGINE', 'postgresql+asyncpg')
PG_DSN = f"{PG_ENGINE}://{PG_USER_NAME}:{PG_USER_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"