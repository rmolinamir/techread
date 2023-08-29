ARG PYTHON_VERSION=3.11.2-bullseye
ARG BUILD_ENVIRONMENT=local
ARG APP_DIR=/app

FROM python:${PYTHON_VERSION} AS base
    # Renew arguments
    ARG BUILD_ENVIRONMENT
    ARG APP_DIR

    # Install dependencies
    RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev

FROM base AS builder
    # Renew arguments
    ARG BUILD_ENVIRONMENT
    ARG APP_DIR

    COPY ./requirements .

    RUN pip wheel --wheel-dir /usr/src/app/wheels \
        -r ${BUILD_ENVIRONMENT}.txt

FROM base AS runner
    # Renew arguments
    ARG BUILD_ENVIRONMENT
    ARG APP_DIR

    # Prevents Python from writing pyc files to disc to keep the container size small.
    ENV PYTHONDONTWRITEBYTECODE 1
    # Prevents Python from buffering stdout and stderr.
    ENV PYTHONNUNBUFFERED 1
    # Set build environment.
    ENV BUILD_ENV ${BUILD_ENVIRONMENT}

    WORKDIR ${APP_DIR}

    # Install dependencies
    RUN apt-get update && apt-get install --no-install-recommends -y \
        libpq-dev \
        gettext \
        # The following will purge all build dependencies after installing them,
        # the end result is a smaller image size.
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
        && rm -rf /var/lib/apt/lists/*

    COPY --from=builder /usr/src/app/wheels /wheels/

    RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
        && rm -rf /wheels/

    # Make entrypoint executable by removing Windows line endings.
    # `chmod` will permit the script to be run when the container starts.
    COPY ./docker/local/django/entrypoint /entrypoint
    RUN sed -i 's/\r$//g' /entrypoint \
        && chmod +x /entrypoint

    # Make start executable by removing Windows line endings.
    # `chmod` will permit the script to be run when the container starts.
    COPY ./docker/local/django/start /start
    RUN sed -i 's/\r$//g' /start \
        && chmod +x /start

    # Copy project.
    COPY . ${APP_DIR}

    ENTRYPOINT [ "/entrypoint" ]
