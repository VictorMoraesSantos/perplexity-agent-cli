"""Operações de filesystem."""

import os
from pathlib import Path
from typing import List, Optional
from rich.console import Console

from .state import StateManager


class FileSystemOps:
    """Operações de sistema de arquivos com suporte a dry-run."""
    
    def __init__(self, state_manager: StateManager, console: Optional[Console] = None):
        self.state_manager = state_manager
        self.console = console or Console()
    
    def _is_dry_run(self) -> bool:
        """Verifica se está em modo dry-run."""
        return self.state_manager.state.dry_run if self.state_manager.state else False
    
    def read_file(self, filepath: str) -> str:
        """Lê conteúdo de um arquivo.
        
        Args:
            filepath: Caminho do arquivo
            
        Returns:
            Conteúdo do arquivo
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            self.console.print(f"[red]Erro ao ler {filepath}:[/red] {e}")
            raise
    
    def write_file(self, filepath: str, content: str) -> bool:
        """Escreve conteúdo em um arquivo.
        
        Args:
            filepath: Caminho do arquivo
            content: Conteúdo a escrever
            
        Returns:
            True se sucesso
        """
        if self._is_dry_run():
            self.console.print(f"[yellow][DRY-RUN] Escreveria em:[/yellow] {filepath}")
            self.console.print(f"[dim]Conteúdo: {len(content)} caracteres[/dim]")
            return True
        
        try:
            # Criar diretórios se necessário
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Registrar arquivo modificado
            self.state_manager.add_file_touched(filepath)
            
            self.console.print(f"[green]✓ Arquivo escrito:[/green] {filepath}")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Erro ao escrever {filepath}:[/red] {e}")
            return False
    
    def list_dir(self, dirpath: str, recursive: bool = False) -> List[str]:
        """Lista arquivos em um diretório.
        
        Args:
            dirpath: Caminho do diretório
            recursive: Se deve listar recursivamente
            
        Returns:
            Lista de caminhos de arquivos
        """
        try:
            if recursive:
                files = []
                for root, _, filenames in os.walk(dirpath):
                    for filename in filenames:
                        files.append(os.path.join(root, filename))
                return files
            else:
                return [
                    os.path.join(dirpath, f)
                    for f in os.listdir(dirpath)
                    if os.path.isfile(os.path.join(dirpath, f))
                ]
        except Exception as e:
            self.console.print(f"[red]Erro ao listar {dirpath}:[/red] {e}")
            return []
    
    def create_dir(self, dirpath: str) -> bool:
        """Cria um diretório.
        
        Args:
            dirpath: Caminho do diretório
            
        Returns:
            True se sucesso
        """
        if self._is_dry_run():
            self.console.print(f"[yellow][DRY-RUN] Criaria diretório:[/yellow] {dirpath}")
            return True
        
        try:
            os.makedirs(dirpath, exist_ok=True)
            self.console.print(f"[green]✓ Diretório criado:[/green] {dirpath}")
            return True
        except Exception as e:
            self.console.print(f"[red]Erro ao criar {dirpath}:[/red] {e}")
            return False
    
    def delete_file(self, filepath: str) -> bool:
        """Deleta um arquivo.
        
        Args:
            filepath: Caminho do arquivo
            
        Returns:
            True se sucesso
        """
        if self._is_dry_run():
            self.console.print(f"[yellow][DRY-RUN] Deletaria:[/yellow] {filepath}")
            return True
        
        try:
            os.remove(filepath)
            self.console.print(f"[green]✓ Arquivo deletado:[/green] {filepath}")
            return True
        except Exception as e:
            self.console.print(f"[red]Erro ao deletar {filepath}:[/red] {e}")
            return False
    
    def file_exists(self, filepath: str) -> bool:
        """Verifica se arquivo existe.
        
        Args:
            filepath: Caminho do arquivo
            
        Returns:
            True se existe
        """
        return os.path.exists(filepath)
    
    def copy_file(self, src: str, dst: str) -> bool:
        """Copia um arquivo.
        
        Args:
            src: Arquivo origem
            dst: Arquivo destino
            
        Returns:
            True se sucesso
        """
        if self._is_dry_run():
            self.console.print(f"[yellow][DRY-RUN] Copiaria:[/yellow] {src} -> {dst}")
            return True
        
        try:
            import shutil
            shutil.copy2(src, dst)
            self.console.print(f"[green]✓ Arquivo copiado:[/green] {src} -> {dst}")
            return True
        except Exception as e:
            self.console.print(f"[red]Erro ao copiar:[/red] {e}")
            return False
