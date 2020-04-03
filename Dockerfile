FROM dynobo/docker-jupyter-extended:0.3.4
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt