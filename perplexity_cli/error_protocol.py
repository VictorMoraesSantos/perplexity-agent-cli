"""Protocolo de tratamento de erros."""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel

from .state import StateManager


@dataclass
class Hypothesis:
    """Hipótese de causa de erro."""
    description: str
    likelihood: str  # 'high', 'medium', 'low'
    fix_suggestion: str


class ErrorProtocol:
    """Protocolo obrigatório para tratamento de erros."""
    
    def __init__(self, state_manager: StateManager, console: Console):
        self.state_manager = state_manager
        self.console = console
        self.max_auto_diagnoses = 2
    
    def handle_error(
        self,
        error_location: str,
        error_message: str,
        log_excerpt: str = ""
    ) -> bool:
        """
        Trata erro seguindo protocolo.
        
        Retorna True se erro foi resolvido automaticamente.
        """
        # 1. Capturar e registrar erro
        self.console.print(f"\n[red bold]✗ ERRO DETECTADO[/red bold]")
        self.console.print(f"[red]Local:[/red] {error_location}")
        self.console.print(f"[red]Mensagem:[/red] {error_message}\n")
        
        self.state_manager.set_error(error_location, error_message, log_excerpt)
        
        # 2. Executar até 2 ações de diagnóstico automáticas
        self.console.print("[cyan]Executando diagnóstico automático...[/cyan]\n")
        
        diagnostic_results = self._run_auto_diagnostics(
            error_location,
            error_message,
            log_excerpt
        )
        
        # 3. Propor hipóteses
        hypotheses = self._generate_hypotheses(
            error_message,
            diagnostic_results
        )
        
        self.console.print("[bold]Hipóteses:[/bold]\n")
        
        for i, hyp in enumerate(hypotheses, 1):
            color = {
                'high': 'red',
                'medium': 'yellow',
                'low': 'blue'
            }.get(hyp.likelihood, 'white')
            
            self.console.print(f"{i}. [{color}][{hyp.likelihood.upper()}][/{color}] {hyp.description}")
            self.console.print(f"   Sugestão: {hyp.fix_suggestion}\n")
        
        # 4. Aplicar correção (primeira hipótese)
        if hypotheses:
            self.console.print(f"[cyan]Aplicando correção baseada na hipótese principal...[/cyan]")
            success = self._apply_fix(hypotheses[0])
            
            if success:
                self.console.print("[green]✓ Correção aplicada[/green]")
                self.state_manager.clear_error()
                return True
        
        # 5. Se falhar, parar e pedir direção ao usuário
        self.console.print("\n[yellow]⚠ Não foi possível corrigir automaticamente[/yellow]")
        self._present_options_to_user(hypotheses)
        
        return False
    
    def _run_auto_diagnostics(
        self,
        location: str,
        message: str,
        log: str
    ) -> List[str]:
        """Executa até 2 ações de diagnóstico."""
        results = []
        
        # Diagnóstico 1: Verificar stacktrace
        self.console.print("  1. Analisando stacktrace...")
        if "Traceback" in log or "Error" in log:
            results.append("Stacktrace presente no log")
        else:
            results.append("Sem stacktrace claro")
        
        # Diagnóstico 2: Verificar versões/dependências
        self.console.print("  2. Verificando dependências...")
        # Simplificado
        results.append("Verificação de dependências pendente")
        
        self.console.print()
        return results
    
    def _generate_hypotheses(
        self,
        error_message: str,
        diagnostic_results: List[str]
    ) -> List[Hypothesis]:
        """Gera hipóteses de causa."""
        hypotheses = []
        
        # Hipótese principal (genérica)
        hypotheses.append(Hypothesis(
            description="Erro de sintaxe ou import faltando",
            likelihood="high",
            fix_suggestion="Verificar imports e sintaxe do código"
        ))
        
        # Hipótese alternativa
        hypotheses.append(Hypothesis(
            description="Problema de configuração ou ambiente",
            likelihood="medium",
            fix_suggestion="Verificar variáveis de ambiente e paths"
        ))
        
        return hypotheses
    
    def _apply_fix(self, hypothesis: Hypothesis) -> bool:
        """Aplica correção baseada em hipótese."""
        # Simplificado - em implementação real faria a correção
        self.console.print(f"  Tentando: {hypothesis.fix_suggestion}")
        return False  # Simula falha para demonstrar fluxo
    
    def _present_options_to_user(self, hypotheses: List[Hypothesis]) -> None:
        """Apresenta opções ao usuário."""
        self.console.print("\n[bold]Opções:[/bold]")
        self.console.print("  1. Tentar hipótese alternativa")
        self.console.print("  2. Fazer correção manual e usar /resume")
        self.console.print("  3. Pular este passo e continuar")
        self.console.print("  4. Abortar tarefa")
        self.console.print("\nUse comandos do CLI para prosseguir.")
    
    def capture_error(self, where: str, message: str, log_excerpt: str = "") -> None:
        """Método auxiliar para capturar erro."""
        self.state_manager.set_error(where, message, log_excerpt)
    
    def diagnose(self) -> dict:
        """Retorna diagnóstico do último erro."""
        if not self.state_manager.state or not self.state_manager.state.last_error:
            return {'hypotheses': []}
        
        error = self.state_manager.state.last_error
        results = self._run_auto_diagnostics(
            error['where'],
            error['message'],
            error.get('log_excerpt', '')
        )
        
        hypotheses = self._generate_hypotheses(error['message'], results)
        
        return {
            'hypotheses': [
                {
                    'description': h.description,
                    'likelihood': h.likelihood,
                    'fix': h.fix_suggestion
                }
                for h in hypotheses
            ]
        }
    
    def propose_fix(self) -> Optional[dict]:
        """Propõe correção para o erro."""
        diagnosis = self.diagnose()
        if not diagnosis['hypotheses']:
            return None
        
        main_hypothesis = diagnosis['hypotheses'][0]
        return {
            'action': 'fix',
            'suggestion': main_hypothesis['fix'],
            'description': main_hypothesis['description']
        }
    
    def apply_fix(self, fix: dict) -> bool:
        """Aplica uma correção."""
        # Implementação simplificada
        self.console.print(f"[cyan]Aplicando:[/cyan] {fix.get('suggestion', 'correção')}")
        return False  # Simula que precisa implementação manual


# Alias para compatibilidade com testes
ErrorHandler = ErrorProtocol
