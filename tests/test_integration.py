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
        assert "0.1.0" in result.output or "version" in result.output.lower()
    
    def test_cli_help(self):
        """Testa comando --help."""
        result = subprocess.run(
            ["perplexity-cli", "--help"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "workspace" in result.output.lower()
    
    @pytest.mark.slow
    def test_full_workflow(self):
        """Testa workflow completo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Iniciar CLI com objetivo
            # 2. Executar comandos
            # 3. Verificar estado final
            # (requer entrada interativa - mock complexo)
            pytest.skip("Requer entrada interativa")
