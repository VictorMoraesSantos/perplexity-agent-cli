#!/usr/bin/env python3
"""Exemplo de uso programático do Perplexity CLI."""

import os
import sys
from pathlib import Path

# Adicionar path do projeto
sys.path.insert(0, str(Path(__file__).parent.parent))

from perplexity_cli.state import StateManager
from perplexity_cli.models import AgentMode
from perplexity_cli.executor import ExecutionPipeline


def main():
    """Exemplo de criação e execução de tarefa."""
    
    # 1. Configurar workspace
    workspace = os.path.expanduser("~/test-project")
    os.makedirs(workspace, exist_ok=True)
    
    print(f"Workspace: {workspace}")
    
    # 2. Criar state manager
    manager = StateManager(workspace)
    
    # 3. Criar estado inicial
    state = manager.create_initial_state(
        goal="Criar estrutura de projeto Python",
        mode=AgentMode.ARCHITECT.value
    )
    
    print(f"\n✓ Estado criado:")
    print(f"  Objetivo: {state.goal}")
    print(f"  Modo: {state.agent_mode}")
    print(f"  Checkpoint: {state.current_checkpoint}")
    
    # 4. Criar executor
    executor = ExecutionPipeline(manager)
    
    # 5. Definir critérios de pronto (Etapa A)
    criteria = [
        "Estrutura de pastas criada",
        "setup.py configurado",
        "README.md inicial criado"
    ]
    
    executor.define_criteria(criteria)
    print(f"\n✓ Critérios de pronto definidos: {len(criteria)} itens")
    
    # 6. Criar plano com checkpoints (Etapa C)
    plan_items = [
        {"step": 1, "action": "Criar estrutura src/", "checkpoint": "CP1:structure"},
        {"step": 2, "action": "Configurar setup.py", "checkpoint": "CP2:setup"},
        {"step": 3, "action": "Criar README.md", "checkpoint": "CP3:docs"}
    ]
    
    executor.create_plan(plan_items)
    print(f"\n✓ Plano criado: {len(plan_items)} etapas")
    
    # 7. Executar plano (Etapa D - simulado)
    print("\n[DRY-RUN] Executando plano...")
    
    for item in plan_items:
        print(f"\n  [{item['step']}] {item['action']}")
        print(f"      Checkpoint: {item['checkpoint']}")
        # Aqui entrariam as operações reais de filesystem
        manager.update_checkpoint(item['checkpoint'])
    
    # 8. Salvar estado final
    manager.save()
    
    print("\n✓ Execução completa!")
    print(f"Estado salvo em: {manager.state_file}")


if __name__ == "__main__":
    main()
