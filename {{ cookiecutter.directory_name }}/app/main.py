"""app.main

Configures the main Python app logic
"""
import logging

from .environment import settings

__version__ = "{{ cookiecutter.version }}"

# Configure our logging level
logging.basicConfig(level=logging.WARNING if not settings.debug else logging.DEBUG)

{% if cookiecutter.project_type == 'Application' -%}
# TODO: Define your main application logic
if __name__ == '__main__':
    print('Hello world!')
{%- else -%}
# TODO: Create your main application named `app`
app = None

# TODO: define app routes, main function, etc. here
{%- endif %}
