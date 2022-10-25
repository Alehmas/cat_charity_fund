from fastapi import FastAPI

# Импортируем роутер.
from app.api.endpoints.charity_project import router
from app.core.config import settings

app = FastAPI(title=settings.app_title)

# Подключаем роутер.
app.include_router(router) 