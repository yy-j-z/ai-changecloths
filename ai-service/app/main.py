from fastapi import FastAPI

from app.routes import health, size


def create_app() -> FastAPI:
    app = FastAPI(title="AI Fitting Mirror AI Service", version="0.1.0")
    app.include_router(health.router, prefix="/internal/v1", tags=["system"])
    app.include_router(size.router, prefix="/internal/v1/size", tags=["size"])
    return app


app = create_app()
