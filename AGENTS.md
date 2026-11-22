# AGENTS.md - Diretrizes para Agentes de IA

**awesome-tools** é uma lista curada de ferramentas, utilitários e recursos de estudo para desenvolvedores. O produto é o
`README.md`: uma lista em tabelas Markdown. Os testes em Python só validam o formato, os links e a segurança.

## Stack

- Markdown (`README.md`, `SECURITY.md`, `docs/readme/` com imagens)
- Python 3 com `pytest` e `flake8` para os testes em `tests/`; dependências de desenvolvimento em `requirements-dev.txt`
- GitHub Actions: `central-validate.yml`, `central-security.yml`, `sast.yml`, `security.yml`

## Comandos

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
flake8 tests/ --max-line-length=120
```

## Estrutura

- `README.md`: a lista principal, categorizada em tabelas Markdown
- `SECURITY.md`: política de segurança do repositório
- `tests/test_readme_catalog.py`: formato das linhas, HTTPS, URLs duplicadas, lista não vazia
- `tests/test_security.py`: `.gitignore`, varredura de segredos, documentação de segurança, pinning de actions e este arquivo
- `.github/workflows/`: CI e segurança
- `docs/readme/`: imagens do README (o banner é um mockup com dados fictícios)

## Convenções

### Edição do README.md

- **Formato de linha:** adicione itens nas tabelas usando `| [Nome](URL) | Descrição. |`.
- **HTTPS:** todo link novo usa `https://`.
- **Sem rastreamento:** remova parâmetros de rastreio das URLs (`utm_*`, `ref`, `source`, `fbclid`).
- **Ordem:** mantenha as entradas organizadas e ordenadas de forma coerente dentro de cada categoria.
- **Idioma:** descrições em português (pt-BR) claro, correto e objetivo.

### Segurança

- **Segredos:** nunca commitar segredos, chaves de API, tokens, senhas ou credenciais.
- **Pin de Actions:** fixe todas as GitHub Actions de terceiros por SHA completo em `.github/workflows/`. Exceção: os reusáveis
  internos `juninmd/base-actions/...` usam sempre `@main` (política central do org; o teste de pinning os ignora).

## Gotchas

- Nunca edite `.github/workflows/` sem rodar os testes localmente antes do commit.
- `tests/test_security.py` também valida este arquivo: ele precisa existir, não começar com cerca de código e mencionar pytest.
- Não remova a menção a pytest daqui sem atualizar o teste.
