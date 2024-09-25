from setuptools import setup, find_packages
from version import *

setup(
    name='ei-cli',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'PyYAML==6.0.1',
    ],
    entry_points={
        'console_scripts': [
            'ei-cli=ei_cli.cli:main',  # CLI command registration
        ],
    },
    description='ei-cli utility to deploy|undeploy pipelines',
)
