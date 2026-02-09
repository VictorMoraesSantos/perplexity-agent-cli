"""Testes da interface CLI."""

import pytest
from click.testing import CliRunner
from perplexity_cli.cli import main


def test_cli_version():
    """Testa comando --version."""
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert 'version' in result.output.lower()


def test_cli_help():
    """Testa comando --help."""
    runner = CliRunner()
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'workspace' in result.output.lower()
    assert 'goal' in result.output.lower()
