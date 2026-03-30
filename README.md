# Tic-tac-toe (servidor)

Servidor TCP em Python com a lógica do jogo da velha. Dois clientes conectam, são pareados e trocam mensagens JSON (uma linha por mensagem).

## Executar

```bash
uv sync
uv run python main.py
```

Variáveis opcionais: `TICTACTOE_HOST` (padrão `0.0.0.0`), `TICTACTOE_PORT` (padrão `5001`).

Ao subir, o terminal mostra o **IP na rede local** e o **IP público** (via [api.ipify.org](https://api.ipify.org)) com a porta, para o outro jogador conectar — na internet é comum precisar de encaminhamento de porta no roteador.

## Documentação para cliente / Pygame

Ver [docs/INTEGRACAO_FRONT.md](docs/INTEGRACAO_FRONT.md).

## Desenvolvimento

```bash
uv run pytest
uv run ruff check .
uv run mypy .
```
