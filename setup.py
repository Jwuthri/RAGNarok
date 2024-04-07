from setuptools import find_packages, setup


def read_requirements():
    with open("requirements.txt", "r") as req:
        return req.read().splitlines()


setup(
    name="src",
    version="0.1.0",
    description="combination of large language models (LLM), retrieval-augmented generation (RAG), and super activation",
    author="Julien Wuthrich",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    zip_safe=False,
    license="MIT",
)
