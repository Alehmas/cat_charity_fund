from fastapi import APIRouter

from app.api.endpoints import charity_router, donate_router

main_router = APIRouter()
main_router.include_router(
    charity_router, prefix='/charity_project', tags=['Charity Project'])
main_router.include_router(
    donate_router, prefix='/donation', tags=['Donation'])
