# AGENTS.md - Diretrizes para Agentes de IA

Este repositório (**awesome-tools**) é uma lista curada de ferramentas, utilitários e recursos de aprendizado para desenvolvedores, organizada em tabelas Markdown.

## Estrutura do Repositório

- `README.md`: Lista principal de recursos categorizados em tabelas Markdown.
- `tests/`: Testes automatizados em Python para validação de segurança e documentação.
- `.github/`: Configurações de CI/CD e workflows do GitHub Actions.

## Comandos para Desenvolvimento e Teste

Instale as dependências de desenvolvimento e execute as verificações do projeto:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
flake8 tests/ --max-line-length=120
```

## Regras para Edição do README.md

- **Formato de linha:** Adicionar itens nas tabelas Markdown usando o padrão `| [Nome](URL) | Descrição. |`.
- **Protocolo HTTPS:** Todos os links adicionados devem obrigatoriamente utilizar o protocolo `https://`.
- **Sem rastreamento:** Remover parâmetros de rastreio de URLs (como `utm_*`, `ref`, `source`, `fbclid`).
- **Ordem:** Manter as entradas organizadas e ordenadas de forma coerente por categoria.
- **Idioma:** Descrições devem ser escritas em português (pt-BR) claro, correto e objetivo.

## Regras de Segurança e Boas Práticas

- **Segredos:** Nunca commitar segredos, chaves de API, tokens, senhas ou credenciais.
- **Pin de Actions:** Fixar todas as GitHub Actions por commit SHA completo em `.github/workflows/`.
- **Workflows e CI:** Nunca editar arquivos em `.github/workflows/` sem rodar os testes localmente antes do commit.
