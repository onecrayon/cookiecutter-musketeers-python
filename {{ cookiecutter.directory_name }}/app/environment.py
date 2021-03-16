"""app.environment

Configuration settings, loaded from environment variables

Typical usage:

    from app.environment import settings

## Adding new environment variables

You must define your new environment variable in 2-3 places:

1. Your environment:
    * LOCAL: `environments/local.env` to set the default local value
    * PRODUCTION: actual environment variables (the environments files are only automatically
      loaded by Docker; they will not be available in most production environments)
2. The Python equivalent in the ApplicationSettings class in this file
"""
from pydantic import BaseSettings


class ApplicationSettings(BaseSettings):
    env: str
    debug: bool = False

    {%- if cookiecutter.use_postgres == 'True' %}

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "db"
    postgres_port: int = 5432
    {%- endif -%}
    {%- if cookiecutter.use_redis == 'True' %}

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_max_connections = 10
    {%- endif -%}
    {%- if cookiecutter.use_postgres == 'True' %}

    @property
    def postgres_url(self) -> str:
        """Database connection URL"""
        return (
            f"postgresql+{% if cookiecutter.async_sqlalchemy == 'True' %}asyncpg{% else %}psycopg2{% endif %}://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}"
            f":{self.postgres_port}/{self.postgres_db}"
        )
    {%- endif -%}
    {%- if cookiecutter.use_redis %}

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"
    {%- endif %}


# Configure settings object from environment variables
settings = ApplicationSettings()
