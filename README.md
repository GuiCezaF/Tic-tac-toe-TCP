# Tic-tac-toe (servidor)

Servidor TCP em Python com a lógica do jogo da velha. Dois clientes conectam, são pareados e trocam mensagens JSON (uma linha por mensagem).

## Requisitos

- Python **3.12 ou superior**

## Executar o servidor

Variáveis opcionais: `TICTACTOE_HOST` (padrão `0.0.0.0`), `TICTACTOE_PORT` (padrão `5001`).

Ao subir, o terminal mostra o **IP na rede local** e o **IP público** (via [api.ipify.org](https://api.ipify.org)) com a porta, para o outro jogador conectar — na internet é comum precisar de encaminhamento de porta no roteador.

### Com [uv](https://docs.astral.sh/uv/)

Na raiz do repositório:

```bash
uv sync
uv run python main.py
```

### Com venv e pip

Na raiz do repositório:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python main.py
```

No **Windows** (PowerShell ou CMD), troque a ativação do ambiente por `.venv\Scripts\activate`.

O `requirements.txt` instala o pacote em modo editável (`-e .`), então os módulos `game` e `server` ficam importáveis ao rodar `main.py` a partir da raiz do projeto.

## Documentação para cliente / Pygame

Ver [docs/INTEGRACAO_FRONT.md](docs/INTEGRACAO_FRONT.md).

## Desenvolvimento (testes e linters)

Versões alinhadas ao `[dependency-groups]` / `pyproject.toml`.

### Com uv

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
uv run mypy .
```

### Com pip

Com o venv ativo e o pacote já instalado (`pip install -r requirements.txt`):

```bash
pip install "pytest>=8.3" "mypy>=1.15" "ruff>=0.11"
pytest
ruff check .
mypy .
```

## Licença

Este projeto está sob a **licença MIT**. Veja o arquivo [LICENSE](LICENSE).
