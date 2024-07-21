# setup.py
from setuptools import setup, find_packages

setup(
    name='python-tools',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4'  # Only third-party libraries should be here
    ],
)
