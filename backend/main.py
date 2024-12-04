from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.base_class import Base

from apis.base import api_router
from apps.base import app_router
from fastapi.staticfiles import StaticFiles


def configure_staticfiles(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
#    create_tables()  # We only need this if we don't want alembic to create our tables
    include_router(app)
    configure_staticfiles(app)
    return app

app = start_application()

# Comment this out before you start the webapp to avoid conflict
"""""
@app.get("/")
def hello():
    return {"message": "This ia a test from me"}
"""""