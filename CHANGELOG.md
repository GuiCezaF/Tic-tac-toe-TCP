# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.1] - 31-03-2026

### Added

- Mensagem `state` com campo `winner_name` (nome do `join` do vencedor) quando a partida termina com vitória; em empate o campo não é enviado.
- Licença **MIT** (`LICENSE`) e campo `license` no `pyproject.toml`.

### Changed

- README com instruções para executar e desenvolver usando **uv** ou **venv + pip**.

## [1.0.0] - 2026-03-31

### Added

- Servidor TCP assíncrono (`asyncio`) que pareia dois jogadores e conduz partidas de jogo da velha.
- Protocolo de mensagens em **JSON**, uma linha por mensagem (NDJSON, UTF-8), documentado em `docs/INTEGRACAO_FRONT.md` e tipado em `server/protocol.py`.
- Módulo `game`: tabuleiro, regras, modelo de estado (`GameSnapshot`, jogadas, erros e desfecho da partida).
- Módulo `server`: matchmaker, sessão remota, leitura/escrita de linhas JSON, tratamento de clientes e `GameServer`.
- Configuração por ambiente: `TICTACTOE_HOST` (padrão `0.0.0.0`) e `TICTACTOE_PORT` (padrão `5001`).
- Ao iniciar, exibe dicas de conexão com IP na rede local e IP público (consulta a [api.ipify.org](https://api.ipify.org)).
- Ponto de entrada `main.py` e empacotamento via `pyproject.toml` (Hatchling).
- `requirements.txt` para instalação com `pip install -r requirements.txt` (modo editável).
- Testes automatizados com pytest (`tests/`).
- Grupo de dependências de desenvolvimento: mypy (strict), ruff e pytest.
