FROM python:3.7.7-buster AS builder
RUN apt-get update && apt-get install -y --no-install-recommends --yes python3-venv gcc libpython3-dev curl && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

FROM builder AS builder-venv

COPY requirements-prod.txt /requirements-prod.txt
COPY requirements-dev.txt /requirements-dev.txt
RUN /venv/bin/pip --version
RUN /venv/bin/pip install -r /requirements-dev.txt

FROM builder-venv AS jupyter-extender

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash && \
    apt-get -y install nodejs
RUN /venv/bin/jupyter labextension install \
    @jupyterlab/toc@3.0.0 \
    @ijmbarr/jupyterlab_spellchecker@0.1.6 \
    @ryantam626/jupyterlab_code_formatter@1.2.2 \
    --no-build
RUN /venv/bin/pip install jupyterlab_code_formatter
RUN /venv/bin/jupyter serverextension enable --py jupyterlab_code_formatter
RUN /venv/bin/jupyter lab build

FROM jupyter-extender AS tester

COPY . /app
WORKDIR /app
RUN /venv/bin/pytest

FROM python:3.7.7-buster as runner
RUN apt-get update && apt-get install -y --no-install-recommends --yes vim netcat
COPY --from=tester /venv /venv
COPY --from=tester /app /app

WORKDIR /app
RUN chmod g+rwx /app
RUN mkdir /.local
RUN chmod g+rwx /.local

EXPOSE 8888

ENTRYPOINT ["/venv/bin/jupyter", "lab", "--ip=0.0.0.0", "--notebook-dir=/app/notebooks", "--port=8888"]

USER 1001

LABEL name={NAME}
LABEL version={VERSION}
