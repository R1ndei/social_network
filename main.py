from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.config import main_settings
from config.db_config import database
import uvicorn
from routes.routes import routes

settings = main_settings()

origins = ["*"]


def get_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION,
        docs_url=settings.API_PATH_V1 + "docs",
        redoc_url=settings.API_PATH_V1 + "redoc",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.database = database
    app.state._database = database

    app.include_router(routes)

    return app


app = get_application()


@app.on_event("startup")
async def startup():
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown():
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


if __name__ == '__main__':
    uvicorn.run(get_application(), host="0.0.0.0", port=8010)
