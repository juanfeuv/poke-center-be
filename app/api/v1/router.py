from fastapi import APIRouter

from app.api.v1.endpoints import users, health

api_router = APIRouter()

# Users
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Health
api_router.include_router(health.router, prefix="/health", tags=["Health"])
