RAGNarok
==============================

combination of large language models (LLM), retrieval-augmented generation (RAG), and super activation

CodeCov
------------
![image](https://codecov.io/gh/Jwuthri/RAGNarok/graphs/tree.svg?token=17KV5BQOE2)

Setup
------------
Please use the `makefile` to setup your project!

```
make create_environment  # will create a virtual-env and create an alias to connect
make dev-install  # this will install all required dependencies
pre-commit install
```
Please use `make lint` to clean your project, it will run `black, isort, and flake8`, *black* is already available in pre-commit hook

#### Build the doc:

```
make build_doc
cd docs/_build/html
open  with your browser -> index.html
```

Variables .env
------------
Please create your .env with command
```
cp .env.template .env
```

In order to run properly the project please fill the ``PINECONE_API_KEY`` and ``OPENAI_API_KEY`` and ``PINECONE_INDEX`` and ``PINECONE_ENV``
environment variables within `.env`.

Run the tests
------------
Please use `make tox` to run your tests, it will create its own python-env and run tests through different python version

or you can use
```
make test  # to run all test
make test_e2e  # to only run e2e test
test_not_e2e  # to skip e2e test
```

Using the project
------------
Please use the following commands:
```
## using your env:
make run_fastapi_uvicorn  # basic app using uvicorn 4 works
make run_fastapi_gunicorn  # to use the production config
## using docker:
make build_linux_image or build_mac_image
make run_docker  # to run the docker locally
```

Project Organization
------------

    ├── LICENSE
    │
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    │
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures         <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    │
    ├── src                <- Source code for use in this project.
    │   ├── core            <- Scripts to download or generate data
    │   │
    │   ├── infrastructure  <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── interface       <- Scripts to train models and then use trained models to make predictions
    │   │
    │   ├── usecases        <- Scripts to train models and then use trained models to make predictions
    │   │
    │   └── queries         <- Scripts to train models and then use trained models to make predictions
    │
    └── tox.ini             <- tox file with settings for running tox; see tox.readthedocs.io
--------
