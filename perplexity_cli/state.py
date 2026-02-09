"""Sistema de estado persistente com checkpoints."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict, field


@dataclass
class CommandResult:
    """Resultado de execução de comando."""
    cmd: str
    result: str  # 'ok' ou 'fail'
    timestamp: str
    output: str = ""


@dataclass
class ErrorInfo:
    """Informações de erro."""
    when: str
    where: str
    message: str
    log_excerpt: str = ""


@dataclass
class RunState:
    """Estado de execução do agente."""
    workspace: str
    agent_mode: str  # ARCHITECT|IMPLEMENTER|DEBUGGER|REVIEWER|DOCUMENTER|OPS
    goal: str
    current_plan_step: int = 0
    current_checkpoint: str = "CP0:init"
    last_successful_checkpoint: str = "CP0:init"
    open_questions: List[str] = field(default_factory=list)
    files_touched: List[str] = field(default_factory=list)
    commands_run: List[Dict[str, Any]] = field(default_factory=list)
    last_error: Optional[Dict[str, str]] = None
    next_action: str = ""
    plan: List[str] = field(default_factory=list)
    checkpoints: Dict[str, bool] = field(default_factory=dict)
    dry_run: bool = False
    watch_enabled: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RunState':
        """Cria instância a partir de dicionário."""
        return cls(**data)


class StateManager:
    """Gerenciador de estado persistente."""
    
    STATE_DIR = ".perplexity-cli"
    STATE_FILE = "state.json"
    
    def __init__(self, workspace: Optional[str] = None):
        self.workspace = workspace or os.getcwd()
        self.state_dir = Path(self.workspace) / self.STATE_DIR
        self.state_file = self.state_dir / self.STATE_FILE
        self.state: Optional[RunState] = None
        
    def ensure_state_dir(self) -> None:
        """Garante que o diretório de estado existe."""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
    def save(self, state: RunState) -> None:
        """Salva estado em arquivo JSON."""
        self.ensure_state_dir()
        self.state = state
        
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load(self) -> Optional[RunState]:
        """Carrega estado do arquivo JSON."""
        if not self.state_file.exists():
            return None
            
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.state = RunState.from_dict(data)
            return self.state
        except Exception as e:
            print(f"Erro ao carregar estado: {e}")
            return None
    
    def update_checkpoint(self, checkpoint: str, success: bool = True) -> None:
        """Atualiza checkpoint no estado."""
        if not self.state:
            return
            
        self.state.current_checkpoint = checkpoint
        if success:
            self.state.last_successful_checkpoint = checkpoint
            self.state.checkpoints[checkpoint] = True
        
        self.save(self.state)
    
    def add_command(self, cmd: str, result: str, output: str = "") -> None:
        """Adiciona comando executado ao histórico."""
        if not self.state:
            return
            
        cmd_result = {
            "cmd": cmd,
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "output": output[:500]  # Limita tamanho
        }
        self.state.commands_run.append(cmd_result)
        self.save(self.state)
    
    def set_error(self, where: str, message: str, log_excerpt: str = "") -> None:
        """Registra erro no estado."""
        if not self.state:
            return
            
        self.state.last_error = {
            "when": datetime.now().isoformat(),
            "where": where,
            "message": message,
            "log_excerpt": log_excerpt[:1000]
        }
        self.save(self.state)
    
    def clear_error(self) -> None:
        """Limpa último erro."""
        if self.state:
            self.state.last_error = None
            self.save(self.state)
    
    def add_file_touched(self, filepath: str) -> None:
        """Adiciona arquivo modificado à lista."""
        if not self.state:
            return
            
        if filepath not in self.state.files_touched:
            self.state.files_touched.append(filepath)
            self.save(self.state)
    
    def create_initial_state(
        self,
        goal: str,
        agent_mode: str = "ARCHITECT",
        workspace: Optional[str] = None
    ) -> RunState:
        """Cria estado inicial."""
        workspace = workspace or self.workspace
        
        state = RunState(
            workspace=workspace,
            agent_mode=agent_mode,
            goal=goal,
            current_plan_step=0,
            current_checkpoint="CP0:init",
            last_successful_checkpoint="CP0:init",
            next_action="Criar plano de execução"
        )
        
        self.save(state)
        return state
