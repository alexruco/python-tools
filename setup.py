#setups.py
from setuptools import setup, find_packages

setup(
    name='assets',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'json',
        're',  
        'os',
        'BeautifulSoup'
    ],
)
