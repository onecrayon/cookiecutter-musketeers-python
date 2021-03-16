#!/usr/bin/env sh

set -o errexit
set -o nounset

# We are using `gunicorn` for production, see:
# http://docs.gunicorn.org/en/stable/configure.html

# Check that $ENV is set to "production",
# fail otherwise, since it may break things:
echo "ENV is $ENV"
if [ "$ENV" != 'production' ]; then
  echo 'Error: ENV is not set to "production".'
  echo 'Application will not start.'
  exit 1
fi

export ENV

# Start gunicorn:
# Docs: http://docs.gunicorn.org/en/stable/settings.html
/usr/local/bin/gunicorn app.main:app \
  {% if cookiecutter.project_type == "ASGI server" -%}
  -k uvicorn.workers.UvicornWorker `# Establish Uvicorn as our worker class` \
  {% endif -%}
  --workers=3 `# Workers generally should be (2 x num_cores) + 1` \
  --bind='0.0.0.0:10000' `# Run app on 10000 port (Render.com default)` \
  --chdir='/code'       `# Locations` \
  --log-file=- \
  --worker-tmp-dir='/dev/shm'
