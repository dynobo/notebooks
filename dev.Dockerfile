FROM python:3.7.7-buster AS builder
RUN apt-get update && apt-get install -y --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

FROM builder AS builder-venv

COPY requirements-prod.txt /requirements-prod.txt
COPY requirements-dev.txt /requirements-dev.txt
RUN /venv/bin/pip --version
RUN /venv/bin/pip install -r /requirements-dev.txt

FROM builder-venv AS tester

COPY . /app
WORKDIR /app
RUN /venv/bin/pytest

FROM python:3.7.7-buster as runner
RUN apt-get update && apt-get install -y --no-install-recommends --yes vim netcat
COPY --from=tester /venv /venv
COPY --from=tester /app /app

WORKDIR /app

ENTRYPOINT ["/venv/bin/python3", "-m", "notebooks"]
USER 1001

LABEL name={NAME}
LABEL version={VERSION}
