#!/usr/bin/env sh

set -o errexit
set -o nounset

cmd="$*"

services_ready () {
	# Check that all services are up and running
    # TODO: Add new services here, if you need them
	dockerize \
		{% if cookiecutter.use_postgres == 'True' -%}
		-wait 'tcp://db:5432' \
		{% endif -%}
		{%- if cookiecutter.use_redis == 'True' -%}
		-wait 'tcp://redis:6379' \
		{% endif -%}
		-timeout 5s
}

# We need this line to make sure that this container is started
# after the ones with postgres:
until [ -n "${STANDALONE:-''}" ] || { services_ready; }; do
	>&2 echo 'Services unavailable - sleeping...'
done

if [ -n "${STANDALONE:-''}" ]; then
	>&2 echo ''
else
	>&2 echo 'All services up - continuing...'
fi

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
