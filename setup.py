from setuptools import setup, find_packages

setup(
    name="rizzume",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.0.1",
        "gunicorn==20.1.0",
        "flask-cors==3.0.10",
    ],
)
