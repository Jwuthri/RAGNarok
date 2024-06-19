from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name="ragnarok",
    version="0.1.0",
    description="combination of large language models (LLM), retrieval-augmented generation (RAG), and super activation",
    author="Julien Wuthrich",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "anthropic==0.20.0",
        "cohere==5.0.0",
        "openai==1.17.0",
        "docstring_parser==0.16",
        "pinecone-client==3.0.0",
        "pinecone-text==0.7.2",
        "pydantic==2.6.4",
        "pydantic-settings==2.2.1",
        "pydantic_core==2.16.3",
        "python-dotenv==1.0.0",
        "python-json-logger==2.0.0",
        "rich==13.0.0",
        "serpapi==0.1.5",
        "tiktoken==0.7.0",
    ],
    zip_safe=False,
    license="MIT",
)
