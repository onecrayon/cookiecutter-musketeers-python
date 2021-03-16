# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Dependencies

You must install the following to run the stack locally:

* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/) (included in Docker
  Desktop on Windows and Mac)
* Make

That's it! For local development, all other code is executed in Docker via Make using
the standard [3 Musketeers](https://3musketeers.io/) pattern.

### Running on Windows

**Please note:** in order to run Docker Desktop on Windows you will need a recent copy of
Windows 10 Home with [WSL 2 enabled](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

Please make sure to locate this project in your WSL 2 file system to ensure performance.

## First run

After installing the dependencies above, run `make` from the root project directory
to build your main Docker container and display the available commands you can execute.

{% if cookiecutter.use_postgres == 'True' -%}
Now that you have a functional stack, you need to setup your database:

1. Run `make migrate` to initialize your database with the latest migrations

At this point, you can execute `make run` to start a local stack, and view your
site's root at <http:localhost:8000>.

{% endif -%}

### Configuring VSCode

You can use [Visual Studio Code](https://code.visualstudio.com/) to develop directly within
the Docker container, allowing you access to the Python environment (which means
linting, access to Python tools, working code analysis for free, and bash shell access
without needing to run a make command). To do so:

1. Install [Visual Studio Code](https://code.visualstudio.com/), if you haven't already
2. Install the [Remote Development extension pack](https://aka.ms/vscode-remote/download/extension)
3. **Outside VSCode** in your favored command line, execute `make run` to launch the app container
4. **Inside VSCode** use the Remote Explorer in the left sidebar of VSC to attach to the running
   app container (named `{{ cookiecutter.directory_name }}:local`). You can find explicit instructions
   for this in the [Visual Studio Code documentation](https://code.visualstudio.com/docs/remote/containers#_attaching-to-running-containers)
5. If this is your first time attaching, open the Command Palette and type "container" then
   select "Remote-Containers: Open Container Configuration", replace the contents
   of the file with the following, save, and then close the window and re-attach to the container:

```json
{
  "workspaceFolder": "/code",
  "settings": {
    "terminal.integrated.shell.linux": "/bin/bash",
    "python.pythonPath": "/usr/local/bin/python3.9",
    "python.linting.pylintEnabled": true,
    "python.linting.enabled": true,
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "[python]": {
      "editor.codeActionsOnSave": {
        "source.organizeImports": true
      }
    },
    "editor.wordWrapColumn": 88
  },
  "remoteUser": "root",
  "extensions": [
    "editorconfig.editorconfig",
    "ms-python.python"
  ]
}
```

You will need to start the stack prior to launching VSCode to automatically attach to it.
(I am looking into ways to improve this workflow, but short-term this is the easiest
to get working consistently.)

**Please note:** you *must* run your make commands in an external shell! The VSCode Terminal
in your attached container window will provide you access to the equivalent of `make shell`,
but running the standard make commands there will result in Docker-in-Docker, which is not
desirable in this instance.

### Configuring PyCharm

You can use [PyCharm](https://www.jetbrains.com/pycharm/) to develop directly within
the Docker container, allowing you access to the Python environment (which means
linting, access to Python tools, etc.). To do so:

1. [Install PyCharm](https://www.jetbrains.com/pycharm/download/), if you haven't already
2. In your favorite Terminal, run `make up` to ensure the local stack is running
3. Open PyCharm's Settings (on Windows) or Preferences (on macOS)
4. Under Project -> Python Interpreter, click the gear icon by the Python Interpreter dropdown and choose "Add..."
5. Select "Docker Compose" as the type in the left sidebar 
6. Select `app` under the "Service" dropdown
7. Apply your changes and close the settings

#### Debugging in PyCharm

You will now have auto-completion, automatic imports, and code navigation capabilities in PyCharm.
To enable local debugging:

1. In the upper right of the main window, click "Add Configuration..."
2. Click the "+" button and choose "Python" as the template
3. Name your configuration whatever you like (e.g. `Local`)
{% if cookiecutter.project_type == "ASGI server" -%}
4. Select "Script path", switch it to "Module name", then enter `uvicorn` as the "Module name"
5. Enter `app.main:app --reload --host 0.0.0.0 --port 8000` as the "Parameters"
{% else -%}
4. Select "Script path", switch it to "Module name", then enter `gunicorn` as the "Module name"
5. Enter `--workers=2 app.main:app --reload --bind=0.0.0.0:8000` as the "Parameters"
{%- endif %}
6. Choose the Python Interpreter you setup in the previous steps
7. Apply your changes
8. In your favorite Terminal, exit the running local stack (if it is still running)
9. You can now launch a local stack (or debug a local stack) with the buttons in the upper right corner of the main
   window (the stack should auto-reload as you save files)
   
#### Automatic code formatting in PyCharm

This project is configured to use `isort` and `black` for import and code formatting, respectively.
You can trigger formatting across the full project using `make format`, or you can also setup automatic
formatting on a per-file basis within PyCharm:

1. Open PyCharm's Settings (on Windows) or Preferences (on macOS)
2. Under Tools -> File Watchers, click the "+" button and choose the "custom" template
3. Name your File Watcher whatever you like (e.g. "isort & black")
4. Configure the following settings:
    * File type: `Python`
    * Scope: `Project Files`
    * Program: `make` (macOS/Linux) or `wsl` (Windows)
    * Arguments: `format FILEPATH=$FilePathRelativeToProjectRoot$` (macOS/Linux) or
      `make format FILENAME="$UnixSeparators($FilePathRelativeToProjectRoot$)$"` (Windows)
    * Output paths to refresh: `$FilePath$`
    * Working Directory and Environment Variables -> Working directory: `$ProjectFileDir$`
    * Uncheck Advanced Options -> Auto-save edited files to trigger the watcher
    * Uncheck Advanced Options -> Trigger the watcher on external changes

If automatic formatting is behaving too slowly for your tastes, you can optionally install isort and black in
your host environment and configure them that way:

* https://github.com/pycqa/isort/wiki/isort-Plugins
* https://black.readthedocs.io/en/stable/editor_integration.html

## Development

### Installing Python dependencies

This app uses [Poetry](https://python-poetry.org/) for dependency management. To
install a new dependency from outside of the container:

```sh
$ make shell
root@123:/code$ poetry add DEPENDENCY
```

(If you are developing within Visual Studio Code, you can open the built-in terminal and skip
the `make shell` command.)

Then commit changes in your updated `poetry.lock` and `pyproject.toml`. Please see the
[Poetry docs](https://python-poetry.org/docs/) for other available commands.

You will need to shut down your container, run `make build`, and relaunch it to ensure that
newly added dependencies are available on subsequent launches. If you pull down code and stuff
starts failing in weird ways, you probably need to run `make build`.

**Please note:** `make shell` will log you into the Docker container as the root user!
This is unfortunately necessary to allow Poetry to function properly (I haven't found a
good way yet to install initial dependencies as a non-root account and have them work,
which means the shell has to be root in order to properly calculate the dependency graph).

### Update core tools

The underlying Dockerfile uses the following tools, pinned to specific release versions:

* [Poetry](https://python-poetry.org/)
* [Dockerize](https://github.com/jwilder/dockerize)

In order to update these tools, you must update their pinned version in `Dockerfile`
and (for Poetry) in `pyproject.toml` then rebuild your app container using `make build`.
