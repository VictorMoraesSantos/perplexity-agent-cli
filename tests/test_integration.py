"""Testes de integração end-to-end."""

import pytest
import tempfile
import subprocess
from pathlib import Path


@pytest.mark.integration
class TestCLIIntegration:
    """Testes de integração do CLI completo."""
    
    def test_cli_version(self):
        """Testa comando --version."""
        result = subprocess.run(
            ["perplexity-cli", "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "0.1.0" in result.stdout or "version" in result.stdout.lower()
    
    def test_cli_help(self):
        """Testa comando --help."""
        result = subprocess.run(
            ["perplexity-cli", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "workspace" in result.stdout.lower()
    
    @pytest.mark.slow
    def test_full_workflow(self):
        """Testa workflow completo."""
        pytest.skip("Requer entrada interativa")
