"""Sistema de watch de filesystem."""

import time
from pathlib import Path
from typing import Optional, Callable, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from rich.console import Console


class FileChangeHandler(FileSystemEventHandler):
    """Handler de eventos de arquivo."""
    
    def __init__(
        self,
        console: Console,
        callback: Optional[Callable[[str, str], None]] = None
    ):
        self.console = console
        self.callback = callback
        self.ignored_patterns = {
            '.git', '__pycache__', '.pyc', '.perplexity-cli',
            'node_modules', '.venv', 'venv'
        }
    
    def should_ignore(self, path: str) -> bool:
        """Verifica se path deve ser ignorado."""
        path_obj = Path(path)
        
        for part in path_obj.parts:
            if any(pattern in part for pattern in self.ignored_patterns):
                return True
        
        return False
    
    def on_modified(self, event: FileSystemEvent) -> None:
        """Arquivo modificado."""
        if event.is_directory or self.should_ignore(event.src_path):
            return
        
        self.console.print(f"[yellow]🔄 Modificado:[/yellow] {event.src_path}")
        
        if self.callback:
            self.callback("modified", event.src_path)
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Arquivo criado."""
        if event.is_directory or self.should_ignore(event.src_path):
            return
        
        self.console.print(f"[green]➕ Criado:[/green] {event.src_path}")
        
        if self.callback:
            self.callback("created", event.src_path)
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        """Arquivo deletado."""
        if event.is_directory or self.should_ignore(event.src_path):
            return
        
        self.console.print(f"[red]❌ Deletado:[/red] {event.src_path}")
        
        if self.callback:
            self.callback("deleted", event.src_path)


class FileSystemWatcher:
    """Watcher de filesystem."""
    
    def __init__(
        self,
        workspace: str,
        console: Console,
        callback: Optional[Callable[[str, str], None]] = None
    ):
        self.workspace = Path(workspace)
        self.console = console
        self.callback = callback
        self.observer: Optional[Observer] = None
        self.is_watching = False
    
    def start(self) -> bool:
        """Inicia watcher."""
        if self.is_watching:
            self.console.print("[yellow]Watcher já está ativo[/yellow]")
            return False
        
        try:
            event_handler = FileChangeHandler(self.console, self.callback)
            self.observer = Observer()
            self.observer.schedule(
                event_handler,
                str(self.workspace),
                recursive=True
            )
            self.observer.start()
            self.is_watching = True
            
            self.console.print(f"[green]✓ Watcher ativo em:[/green] {self.workspace}")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Erro ao iniciar watcher:[/red] {e}")
            return False
    
    def stop(self) -> bool:
        """Para watcher."""
        if not self.is_watching or not self.observer:
            return False
        
        try:
            self.observer.stop()
            self.observer.join()
            self.is_watching = False
            
            self.console.print("[green]✓ Watcher parado[/green]")
            return True
            
        except Exception as e:
            self.console.print(f"[red]Erro ao parar watcher:[/red] {e}")
            return False
    
    def __del__(self):
        """Destrutor - garante que observer seja parado."""
        if self.is_watching:
            self.stop()
