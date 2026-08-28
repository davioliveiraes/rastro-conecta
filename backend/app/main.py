from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version=settings.api_version,
    )
    application.include_router(
        health_router,
        prefix=f"/api/{settings.api_version}",
    )
    return application


app = create_app()

