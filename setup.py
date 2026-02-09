from setuptools import setup, find_packages

setup(
    name="perplexity-agent-cli",
    version="0.2.0",
    description="Agente conversacional de engenharia de software",
    author="Victor Moraes",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "watchdog>=3.0.0",
        "gitpython>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "perplexity-cli=perplexity_cli.cli:main",
        ]
    },
    python_requires=">=3.9",
)
