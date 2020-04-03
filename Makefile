up:
	@docker-compose up jupyterlab

test:
	@docker-compose up test

version:
	@echo $(TAG)

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

venv:
	rm -rf .venv
	@python3 -m venv .venv
	@.venv/bin/pip install --upgrade pip
	@.venv/bin/pip install -r requirements-dev.txt

