from setuptools import setup, find_packages

setup(
    name="langchain-document-qa",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "langchain>=0.3.0",
        "langchain-community>=0.3.0",
        "langchain-openai>=0.2.0",
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.32.0",
    ],
)
