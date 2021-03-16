# Cookiecutter template for 3 Musketeers Python app

This is a [Cookiecutter](https://cookiecutter.readthedocs.io/) template that bootstraps
a generic [3 Musketeers](https://3musketeers.io/) Python project (suitable for standalone
apps, WSGI servers, and ASGI servers).

## Why 3 Musketeers?

Python apps can be annoying to develop locally, because you have to make sure you've
got the right version of Python (which could be different across different projects),
manage dependencies, and coordinate different portions of your software stack.

A 3 Musketeers project requires you to boot up a complete local Python stack with
**a single command**. And it works exactly the same on macOS, Windows, and Linux.

You'll never look back.

## Usage

**I do not recommend using this template with a globally-installed version of Cookiecutter**
because the post-run script: 1) requires `sh` in a Unix environment; and 2) will install Poetry
in your global default Python namespace, which you probably don't want.

Instead, you should get a head-start on your 3 Musketeers local environment by installing the
following:

* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/) (included in Docker Desktop on
  Windows and macOS)
* Make (this is probably available in your terminal already)

For Windows users, you will want to install Docker Desktop on the Windows side, and place this
repository (and any projects you create with it) in your WSL 2 file system.

After installing the dependencies above, simply run `make` from the root directory! Once the
Docker container is built, you will be able to proceed through the standard Cookiecutter command
line interface to create your project. You can then move your newly created project folder
out of this project's root directory, and you'll be good to go!

Refer to the README in your new project for how to get a local server up and running (you're
halfway there already!).

### Configuration options

Most of the configuration options should be self-explanatory, but here are the implications
behind the less-obvious ones:

* `project_type`: an "Application" will not create any folders for managing views and schemas,
  whereas the two "server" options will layout a more complete project skeleton.
* `use_postgres`: if you select `True`, your project will include SQLAlchemy 1.4 (with Alembic
  for migrations), a Postgres Docker container, and `make` utilities for working with your
  database. **Please note:** SQLAlchemy 1.4 has some [key differences](https://docs.sqlalchemy.org/en/14/changelog/migration_14.html)
  from SQLAlchemy 1.3!
* `async_sqlalchemy`: if you select `True`, your project will use `asyncpg` instead of `psycopg2`
  as the database API. This is intended for use with ASGI servers that must run everything async.
  (If you plan to use FastAPI, you probably don't want this; it can run either async or sync and
  async support for SQLAlchemy is still experimental).
* `use_redis`: if you select `True`, your project will include a redis Docker container. **Please
  note:** you will need to install a redis Python library via Poetry (like `redis` or `aioredis`).
  This template does not currently make any assumptions about whether you will use async or standard
  redis connections (namely because FastAPI, a very common ASGI server, often uses non-async code).
* `use_pytest`: if you select `True`, Docker and `make` will include utilities for running tests
  with Coverage.
* `poetry_version`: allows you to specify a different version of Poetry to use for dependencies.
