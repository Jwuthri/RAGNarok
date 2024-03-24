from setuptools import find_packages, setup

setup(
    name="src",
    version="0.1.0",
    description="combination of large language models (LLM), retrieval-augmented generation (RAG), and super activation",
    author="Julien Wuthrich",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license="MIT",
)
