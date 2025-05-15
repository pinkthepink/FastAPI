import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    # Create tables if they don't exist
    # In production, you'd use Alembic migrations instead
    from app.db.base import Base
    from app.models import User, Client
    
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Create initial superuser if it doesn't exist
    from app.db.session import AsyncSessionLocal
    from app.crud.user import user
    from app.schemas.user import UserCreate
    
    async with AsyncSessionLocal() as session:
        # Check if superuser exists
        superuser = await user.get_by_email(session, email=settings.FIRST_SUPERUSER)
        if not superuser:
            superuser_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                full_name="Initial Super User",
            )
            await user.create(session, obj_in=superuser_in)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Client Management API"}