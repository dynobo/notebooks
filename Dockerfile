FROM dynobo/docker-jupyter-extended:0.3.5
COPY ./requirements.txt /home/requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /home/requirements.txt
WORKDIR /home