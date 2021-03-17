#!/bin/sh

echo '##############################'
echo 'Generating Poetry lock file...'
echo '##############################'

pip install "poetry=={{ cookiecutter.poetry_version }}"

poetry lock

echo '###########################'
echo 'Cleaning up file listing...'
echo '###########################'

if [ '{{ cookiecutter.project_type }}' = 'Application' ]; then
	rm -r app/schemas
	rm -r app/views
fi
if [ '{{ cookiecutter.use_postgres }}' = 'False' ]; then
	rm -r app/models
	rm -r migrations
	rm alembic.ini
	rm app/db.py
fi
if [ '{{ cookiecutter.use_pytest }}' = 'False' ]; then
	rm -r app/tests
	rm .coveragerc
	rm docker-compose.test.yml
	rm environments/test.env
elif [ '{{ cookiecutter.async_sqlalchemy }}' = 'True' ]; then
	rm app/tests/conftest.py
fi

echo '#########################################'
echo 'All done! Search for TODO to get started.'
echo '#########################################'
