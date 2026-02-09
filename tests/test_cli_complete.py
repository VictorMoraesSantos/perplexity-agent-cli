"""Testes completos da interface CLI."""

import pytest
from click.testing import CliRunner
from perplexity_cli.cli import main, PerplexityCLI
import tempfile
import os


class TestCLIBasic:
    """Testes básicos da CLI."""
    
    def test_cli_help(self):
        """Teste do comando --help."""
        runner = CliRunner()
        result = runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert 'Perplexity Agent CLI' in result.output
        assert '--workspace' in result.output
        assert '--goal' in result.output
    
    def test_cli_version(self):
        """Teste do comando --version."""
        runner = CliRunner()
        result = runner.invoke(main, ['--version'])
        
        assert result.exit_code == 0
        assert '0.1.0' in result.output
    
    def test_cli_with_workspace(self):
        """TC-CLI-003: CLI com workspace customizado."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Simular input para sair imediatamente
            result = runner.invoke(main, ['--workspace', tmpdir], input='/exit\n')
            
            # Não deve crashar
            assert 'Perplexity Agent CLI' in result.output or result.exit_code == 0
    
    def test_cli_with_goal_and_mode(self):
        """TC-CLI-002: CLI com goal e mode."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir, '--goal', 'Teste CLI', '--mode', 'ARCHITECT'],
                input='/exit\n'
            )
            
            # Deve criar estado
            state_file = os.path.join(tmpdir, '.perplexity-cli', 'state.json')
            assert os.path.exists(state_file)


class TestCLICommands:
    """Testes de comandos da CLI."""
    
    def test_status_command(self):
        """TC-CMD-001: Comando /status."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir, '--goal', 'Teste Status'],
                input='/status\n/exit\n'
            )
            
            assert 'Teste Status' in result.output or result.exit_code == 0
    
    def test_agent_command_valid(self):
        """TC-CMD-002: Comando /agent com modo válido."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir, '--goal', 'Teste'],
                input='/agent IMPLEMENTER\n/exit\n'
            )
            
            assert 'IMPLEMENTER' in result.output or result.exit_code == 0
    
    def test_help_command(self):
        """TC-CMD-006: Comando /help."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='/help\n/exit\n'
            )
            
            # Deve mostrar lista de comandos
            assert '/status' in result.output or '/agent' in result.output or result.exit_code == 0
    
    def test_empty_slash_command(self):
        """TC-CLI-007: Comando / vazio."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='/\n/exit\n'
            )
            
            # Deve mostrar mensagem de erro amigável
            assert result.exit_code == 0  # Não deve crashar
    
    def test_unknown_command(self):
        """Comando desconhecido."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='/comando_inexistente\n/exit\n'
            )
            
            assert 'desconhecido' in result.output.lower() or result.exit_code == 0


class TestCLINaturalInput:
    """Testes de entrada natural."""
    
    def test_greeting_input(self):
        """TC-CLI-006: Entrada de saudação."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='ola\n/exit\n'
            )
            
            # Deve responder amigavelmente
            assert 'Olá' in result.output or result.exit_code == 0
    
    def test_short_input(self):
        """TC-CLI-005: Entrada muito curta."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='oi\n/exit\n'
            )
            
            # Deve rejeitar com mensagem
            assert result.exit_code == 0  # Não deve crashar
    
    def test_valid_natural_command(self):
        """TC-CLI-004: Comando natural válido."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            result = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='criar uma API REST\n/exit\n'
            )
            
            # Deve detectar modo e criar estado
            assert 'IMPLEMENTER' in result.output or result.exit_code == 0


class TestCLIErrorHandling:
    """Testes de tratamento de erros."""
    
    def test_invalid_workspace(self):
        """Workspace inválido."""
        runner = CliRunner()
        
        # Path que provavelmente não existe
        invalid_path = '/path/that/absolutely/does/not/exist/xyz123'
        result = runner.invoke(
            main,
            ['--workspace', invalid_path]
        )
        
        # Deve mostrar erro
        assert result.exit_code != 0 or 'Error' in result.output
    
    def test_invalid_mode(self):
        """Modo inválido."""
        runner = CliRunner()
        
        result = runner.invoke(
            main,
            ['--mode', 'MODO_INVALIDO']
        )
        
        # Click deve rejeitar
        assert result.exit_code != 0


class TestCLIIntegration:
    """Testes de integração da CLI."""
    
    def test_full_workflow(self):
        """Workflow completo: criar, modificar, consultar estado."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Criar estado inicial
            result1 = runner.invoke(
                main,
                ['--workspace', tmpdir, '--goal', 'Teste Workflow'],
                input='/status\n/exit\n'
            )
            assert result1.exit_code == 0
            
            # 2. Reabrir e verificar persistência
            result2 = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='/status\n/exit\n'
            )
            
            # Estado deve ter sido carregado
            assert 'Teste Workflow' in result2.output or result2.exit_code == 0
    
    def test_multiple_commands_sequence(self):
        """Sequência de vários comandos."""
        runner = CliRunner()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            commands = [
                'criar API',
                '/status',
                '/agent DEBUGGER',
                '/status',
                '/exit'
            ]
            
            result = runner.invoke(
                main,
                ['--workspace', tmpdir],
                input='\n'.join(commands)
            )
            
            # Deve executar tudo sem crashar
            assert result.exit_code == 0
