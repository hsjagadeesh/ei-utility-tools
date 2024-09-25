from setuptools import setup, find_packages
from ei_cli.version import VERSION

with open('ei_cli/requirements.txt') as f:
    required_pkgs = f.read().splitlines()

setup(
    name='ei-cli',
    version=VERSION,
    maintainer="Rainier Devops",
    maintainer_email="rainier-devops@cisco.com",
    url="https://cto-github.cisco.com/Edge/ei-utility-tools",
    packages=find_packages(),
    install_requires=required_pkgs,
    entry_points={
        'console_scripts': [
            'ei-cli=ei_cli.cli:main',  # CLI command registration
        ],
    },
    description='Command Line Module for EI Local Manager Orchestration',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Cisco System India Pvt Ltd",
        "Operating System :: OS Independent",
    ]
)
