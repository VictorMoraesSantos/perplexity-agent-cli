# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Unreleased]

### Planejado
- Integração com LLM para processamento de linguagem natural
- Sistema de patches avançado
- Interface web opcional
- Suporte a múltiplos workspaces simultâneos

## [0.1.0] - 2026-02-09

### Adicionado
- Sistema de checkpoints com estado persistente
- 6 perfis de agente (ARCHITECT, IMPLEMENTER, DEBUGGER, REVIEWER, DOCUMENTER, OPS)
- Pipeline de execução estruturado (Etapas A-E)
- Protocolo de erro com diagnóstico automático
- 10 comandos CLI (/agent, /workspace, /status, /plan, /resume, /dry-run, /apply, /watch, /undo, /help)
- Watcher de filesystem para detecção de mudanças externas
- Modo dry-run para simulação
- Integração com Git
- Testes unitários
- Documentação completa
- CI/CD com GitHub Actions
- Scripts de setup e instalação

### Notas
- Primeira versão funcional completa
- Todas as features básicas implementadas
- Pronto para uso em produção
