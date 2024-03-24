#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = RAGNarok
PYTHON_INTERPRETER = python3.10

ifeq (,$(shell which zsh))
    EXPORT_FILE="bashrc"
else
   EXPORT_FILE="zshrc"
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Format code with black
format:
	./venv/bin/python -m black src

## Install Python dev Dependencies
dev-install: requirements.dev.txt
	./venv/bin/python -m pip install -U pip setuptools wheel
	./venv/bin/python -m pip install -r requirements.dev.txt

## Install Python Dependencies
prod-install: requirements.txt
	./venv/bin/python -m pip install -U pip setuptools wheel
	./venv/bin/python -m pip install -r requirements.txt

## Lint
lint: dev-install
	./venv/bin/python -m black --config=.black .
	./venv/bin/python -m isort --profile=black .

## Clean venv
clean_venv:
	rm -rf venv

## Clean project
clean:
	rm -rf __pycache__
	rm -rf pytest_cache
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".coverage*" -delete

## Clean venv
clean_venv:
	rm -rf venv

## Tests
tox: create_environment requirements.dev.txt
	rm -rf .tox
	./venv/bin/python -m tox

## Run Tests
cov-test:
	./venv/bin/python -m pytest -ra -v --disable-warnings --cov-report=html:coverage --cov-config=pyproject.toml --cov-report=term-missing --cov=. --cov-fail-under=5 ./tests

## Run Tests
cicd-test:
	./venv/bin/python -m pytest -ra -v --disable-warnings --cov-report=html:coverage --cov-config=pyproject.toml --cov-report=term-missing --cov=. --cov-fail-under=5 ./tests

## Run Test
test: lint
	./venv/bin/python -m pytest -ra -v --disable-warnings --cov-report=html:coverage --cov-config=pyproject.toml --cov-report=term-missing --cov=. --cov-fail-under=5 ./tests

## Run End-to-end test
test_e2e: lint
	./venv/bin/python -m pytest -ra -v -m e2e --disable-warnings --cov-report=html:coverage --cov-config=pyproject.toml --cov-report=term-missing --cov=. --cov-fail-under=5 ./tests

## Run End-to-end test
test_not_e2e: lint
	./venv/bin/python -m pytest -ra -v -m "not e2e" --disable-warnings --cov-report=html:coverage --cov-config=pyproject.toml --cov-report=term-missing --cov=. --cov-fail-under=5 ./tests

## commit
commit: lint
	git commit -m "$(m)"

## Set up python interpreter environment
create_environment:
	$(PYTHON_INTERPRETER) -m pip install virtualenv
	@echo ">>> Installing virtualenv if not already installed.\nMake sure the following lines are in shell startup file"
	@bash -c "${PYTHON_INTERPRETER} -m venv venv"
	@echo "$(PWD)/venv/bin/activate"
	@echo "alias work_on_$(PROJECT_NAME)=\"source $(PWD)/venv/bin/activate\" >> ~/.$(EXPORT_FILE)"
	@bash -c "grep -qxF 'alias work_on_$(PROJECT_NAME)=\"source $(PWD)/venv/bin/activate\"' ~/.$(EXPORT_FILE) || echo 'alias work_on_$(PROJECT_NAME)=\"source $(PWD)/venv/bin/activate\"' >> ~/.$(EXPORT_FILE)"
	@echo ">>> New virtualenv created. Activate with:\nwork_on_$(PROJECT_NAME)"

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################
## Install spacy models
install_spacy_models:
	$(PYTHON_INTERPRETER) -m spacy download xx_ent_wiki_sm

## Build doc
build_doc:
	cd docs && sphinx-apidoc -o source/ ../src && make clean && make html

## Run streamlit app
run_st: dev-install
	./venv/bin/python -m streamlit run streamlit_app.py

# Run the fastapi
run_fastapi_uvicorn:
	uvicorn src.interface.wsgi.app:app --workers 4 --host 0.0.0.0 --port 80

## Run the fastapi
run_fastapi_gunicorn:
	gunicorn -c src/interface/wsgi/gunicorn_hooks.py src.interface.wsgi.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80

## Build imagegit a
build_linux_image:
	docker buildx build --platform linux/amd64 -t gcr.io/image-linux/$(PROJECT_NAME):latest -f Dockerfile .

## Build local image
build_mac_image:
	docker build -t gcr.io/image-mac/$(PROJECT_NAME):latest -f Dockerfile .

## Push image
push_image:
	docker push gcr.io/image-linux/$(PROJECT_NAME):latest

## Run the docker image
run_docker:
	docker-compose up

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
