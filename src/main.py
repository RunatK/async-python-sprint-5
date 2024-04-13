import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import config
from api.logon_helper import router as logon_router
from api.reference_helper import router as reference_router
from api.helper import router as helper_router
from api.file_helper import router as file_router


app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=config.PROJECT_NAME,
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    # Можно сразу сделать небольшую оптимизацию сервиса 
    # и заменить стандартный JSON-сериализатор на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse,
)

app.include_router(logon_router, prefix='/api/v1')
app.include_router(reference_router, prefix='/api/v1/references')
app.include_router(helper_router, prefix='/api/v1')
app.include_router(file_router, prefix='/api/v1')

if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host localhost --port 8080`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
        reload=True
    )