import os
from logging.config import fileConfig

from alembic import context
import alembic
from sqlalchemy.ext.asyncio import async_engine_from_config

from resources.users import models as users
from resources.posts import models as posts

from config.db_config import MainMetaDB
from config.config import main_settings
from sqlalchemy import create_engine, engine_from_config, pool
import asyncio

settings = main_settings()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option('sqlalchemy.url', settings.get_database_url())
target_metadata = MainMetaDB.metadata
URL = settings.get_database_url()
URL_Local = settings.get_database_url()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_offline():
    context.configure(
        url=URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    async with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
