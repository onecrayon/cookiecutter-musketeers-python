from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.environment import settings

# Setup base engine and session class
engine = create_engine(settings.postgres_url, echo=settings.debug)
SessionLocal = sessionmaker(bind=engine)

# Setup our declarative base
meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
AlchemyBase = declarative_base(metadata=meta)