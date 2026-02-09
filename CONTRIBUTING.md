# Contribuindo para Perplexity Agent CLI

Obrigado pelo interesse em contribuir! 🎉

## Como Contribuir

### 1. Setup do Ambiente

```bash
git clone https://github.com/VictorMoraesSantos/perplexity-agent-cli.git
cd perplexity-agent-cli
python3 -m venv venv
source venv/bin/activate
./scripts/dev-setup.sh
```

### 2. Criar Branch

```bash
git checkout -b feature/minha-feature
# ou
git checkout -b fix/meu-bug
```

### 3. Fazer Alterações

- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize documentação se necessário
- Use commits semânticos (feat:, fix:, docs:, etc.)

### 4. Executar Testes

```bash
./scripts/run-tests.sh
```

### 5. Submeter PR

```bash
git push origin feature/minha-feature
```

Então abra um Pull Request no GitHub.

## Padrões de Código

### Commits Semânticos

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Alterações na documentação
- `test:` - Adicionar/modificar testes
- `refactor:` - Refatoração de código
- `style:` - Formatação, ponto e vírgula, etc.
- `chore:` - Atualizações de build, dependências, etc.

### Formatação

```bash
black perplexity_cli
isort perplexity_cli
```

### Linting

```bash
flake8 perplexity_cli --max-line-length=120
```

## Estrutura de Testes

```python
def test_feature_description():
    """Descrição clara do que testa."""
    # Arrange
    setup_data = ...
    
    # Act
    result = function_under_test(setup_data)
    
    # Assert
    assert result == expected
```

## Reportar Bugs

Ao reportar bugs, inclua:

1. Versão do Python
2. Versão do CLI (`perplexity-cli --version`)
3. Passos para reproduzir
4. Comportamento esperado vs. obtido
5. Logs relevantes

## Sugerir Features

Features devem:

1. Alinhar com a filosofia de checkpoints e rastreabilidade
2. Ser descritas claramente com casos de uso
3. Considerar impacto em features existentes

## Dúvidas?

Abra uma [Discussion](https://github.com/VictorMoraesSantos/perplexity-agent-cli/discussions) no GitHub.
