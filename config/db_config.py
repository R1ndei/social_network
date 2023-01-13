import databases
import ormar
import sqlalchemy
from config.config import main_settings
from sqlalchemy.ext.asyncio import create_async_engine

settings = main_settings()

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.get_database_url())
engine = create_async_engine(settings.get_database_url())


class MainMetaDB(ormar.ModelMeta):
    metadata = metadata
    database = database
