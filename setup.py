from setuptools import setup, find_packages

setup(
    name="trainme",
    version="0.1.0",
    description="Conversational running trainer that syncs to Garmin Connect",
    packages=find_packages(),
    install_requires=[
        "garmin-connect>=0.2.8",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "click>=8.1.0",
    ],
    entry_points={
        'console_scripts': [
            'trainme=src.trainme_cli:cli',
        ],
    },
    python_requires=">=3.7",
)
