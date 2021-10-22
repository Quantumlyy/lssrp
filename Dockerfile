FROM nikolaik/python-nodejs:python3.9-nodejs16-alpine

WORKDIR /usr/src/app
EXPOSE ${PORT:-80}

# Install Pipenv
RUN pip install pipenv

# PostgreSQL + cryptography
RUN apk update && \
	apk add --no-cache libpq curl && \
	apk add --no-cache --virtual .build-deps postgresql-dev gcc musl-dev libffi-dev

RUN npm i -g rimraf

# Copy and install Pipfile before everything else for better caching
COPY Pipfile* ./

# Sync (install) packages
RUN PIP_NO_CACHE_DIR=true pipenv install --system --deploy --ignore-pipfile && \
	pip install --no-cache-dir gunicorn

RUN apk del .build-deps

COPY . .

ENV NPM_BIN_PATH=/usr/local/bin/npm
RUN python manage.py tailwind install
RUN python manage.py tailwind build

RUN python manage.py compilemessages

COPY ./docker-entrypoint.sh /usr/local/bin/

# HEALTHCHECK --interval=30s --timeout=20s --retries=15 \
#     CMD curl --silent 'http://localhost:${PORT:-80}/prijava' || exit 1

CMD ["docker-entrypoint.sh"]
