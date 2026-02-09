"""Operações de filesystem."""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict
import subprocess
import hashlib

from rich.console import Console


class FileSystemOps:
    """Operações de sistema de arquivos."""
    
    def __init__(self, workspace: str, console: Console, dry_run: bool = False):
        self.workspace = Path(workspace)
        self.console = console
        self.dry_run = dry_run
    
    def read_file(self, filepath: str) -> Optional[str]:
        """Lê arquivo."""
        path = self.workspace / filepath
        
        if not path.exists():
            self.console.print(f"[red]Erro:[/red] Arquivo não existe: {filepath}")
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.console.print(f"[green]✓[/green] Lido: {filepath} ({len(content)} bytes)")
            return content
        except Exception as e:
            self.console.print(f"[red]Erro ao ler {filepath}:[/red] {e}")
            return None
    
    def write_file(self, filepath: str, content: str) -> bool:
        """Escreve arquivo."""
        path = self.workspace / filepath
        
        if self.dry_run:
            self.console.print(f"[yellow][DRY-RUN][/yellow] Escreveria: {filepath}")
            return True
        
        try:
            # Criar diretórios se necessário
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.console.print(f"[green]✓[/green] Escrito: {filepath}")
            return True
        except Exception as e:
            self.console.print(f"[red]Erro ao escrever {filepath}:[/red] {e}")
            return False
    
    def list_dir(self, dirpath: str = ".", recursive: bool = False) -> List[str]:
        """Lista diretório."""
        path = self.workspace / dirpath
        
        if not path.exists():
            self.console.print(f"[red]Erro:[/red] Diretório não existe: {dirpath}")
            return []
        
        try:
            if recursive:
                files = []
                for root, dirs, filenames in os.walk(path):
                    for filename in filenames:
                        rel_path = os.path.relpath(
                            os.path.join(root, filename),
                            self.workspace
                        )
                        files.append(rel_path)
                return files
            else:
                items = [item.name for item in path.iterdir()]
                return items
        except Exception as e:
            self.console.print(f"[red]Erro ao listar {dirpath}:[/red] {e}")
            return []
    
    def grep(self, pattern: str, filepath: Optional[str] = None) -> Dict[str, List[str]]:
        """Busca padrão em arquivos."""
        results = {}
        
        try:
            if filepath:
                # Buscar em arquivo específico
                cmd = ["grep", "-n", pattern, str(self.workspace / filepath)]
            else:
                # Buscar recursivamente
                cmd = ["grep", "-rn", pattern, str(self.workspace)]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.workspace
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if ':' in line:
                        file_line = line.split(':', 1)
                        file = file_line[0]
                        if file not in results:
                            results[file] = []
                        results[file].append(line)
            
            return results
        except Exception as e:
            self.console.print(f"[red]Erro ao fazer grep:[/red] {e}")
            return {}
    
    def run_command(self, cmd: str) -> tuple[int, str, str]:
        """Executa comando."""
        if self.dry_run:
            self.console.print(f"[yellow][DRY-RUN][/yellow] Executaria: {cmd}")
            return (0, "", "")
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.workspace
            )
            
            return (result.returncode, result.stdout, result.stderr)
        except Exception as e:
            return (-1, "", str(e))
    
    def git_status(self) -> Optional[str]:
        """Retorna git status."""
        returncode, stdout, stderr = self.run_command("git status --short")
        
        if returncode == 0:
            return stdout
        else:
            self.console.print(f"[yellow]Aviso:[/yellow] Git não disponível ou não é repo git")
            return None
    
    def git_diff(self, filepath: Optional[str] = None) -> Optional[str]:
        """Retorna git diff."""
        cmd = "git diff" + (f" {filepath}" if filepath else "")
        returncode, stdout, stderr = self.run_command(cmd)
        
        if returncode == 0:
            return stdout
        else:
            return None
    
    def file_hash(self, filepath: str) -> Optional[str]:
        """Calcula hash MD5 de arquivo."""
        path = self.workspace / filepath
        
        if not path.exists():
            return None
        
        try:
            with open(path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return None
