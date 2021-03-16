"""app.models

Data models using SQLAlchemy declarative_base. E.g.:

    from app.db import AlchemyBase

    class MyModel(AlchemyBase):
        __tablename__ = 'my_model'

This module needs to hoist all models to the root-level. For instance:

    from .my_model import MyModel

This allows the Alembic migration logic to automatically detect all models
(when running Alembic migrations it uses `from app import models` to expose
all models to the generation logic).
"""
