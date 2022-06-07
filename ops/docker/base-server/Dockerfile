FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# This can be either development or production.
# When set to development, all the development libraries will be installed.
ARG BUILD_TYPE=production

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    dumb-init \
    git \
    curl \
    awscli \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install pipenv

RUN addgroup --system django \
    && adduser --system --ingroup django django

COPY --chown=django:django . /app

WORKDIR /app

RUN mkdir /app/requirements
RUN pipenv lock -r > /app/requirements/production.txt
RUN pipenv lock -r --dev > /app/requirements/development.txt
RUN if [$BUILD_TYPE = 'production']; \
    then pip install --no-cache-dir -r requirements/production.txt; \
    else pip install --no-cache-dir -r requirements/development.txt; fi


