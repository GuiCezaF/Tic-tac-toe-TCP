# Integração de cliente (ex.: Pygame)

Este documento descreve o contrato de rede do servidor. Os tipos lógicos correspondentes no código Python estão em [`server/protocol.py`](../server/protocol.py) (`TypedDict`) e o estado do tabuleiro em [`game/models.py`](../game/models.py) (`GameSnapshot`).

## Transporte

- Protocolo: **TCP**.
- Endereço padrão: host `0.0.0.0` no servidor (aceita de qualquer interface); variáveis de ambiente `TICTACTOE_HOST` e `TICTACTOE_PORT` (padrão **5001**).
- Texto **UTF-8**.
- **Uma mensagem JSON por linha**, terminada em `\n` (formato NDJSON). O cliente deve acumular `recv` num buffer e processar linha a linha.

## Valores do tabuleiro

Cada célula é um inteiro:

| Valor | Significado |
|------|-------------|
| `0`  | vazio       |
| `1`  | X           |
| `2`  | O           |

Índices `row` e `col` vão de **0 a 2**. **X** começa a partida.

## Mensagens cliente → servidor

### `join` (obrigatória como primeira mensagem)

```json
{"type":"join","name":"Alice"}
```

### `move`

Só é aceita depois do pareamento e do `game_start`.

```json
{"type":"move","row":1,"col":2}
```

## Mensagens servidor → cliente

### `waiting`

Enviada ao primeiro jogador conectado, até chegar o segundo.

```json
{"type":"waiting","message":"Aguardando outro jogador conectar."}
```

### `game_start`

Enviada **uma vez** a cada jogador quando o par é formado. O campo `state` segue o mesmo formato do snapshot em `state`.

```json
{"type":"game_start","role":"X","state":{"board":[[0,0,0],[0,0,0],[0,0,0]],"current_turn":"X","phase":"playing"}}
```

### `state`

Broadcast após cada jogada **válida** (ambos recebem a mesma mensagem).

```json
{"type":"state","board":[[1,0,0],[0,2,0],[0,0,0]],"current_turn":"X","phase":"playing"}
```

Quando a partida termina:

```json
{"type":"state","board":[[1,1,1],[0,2,0],[0,0,0]],"current_turn":null,"phase":"finished","winner":"X","winner_name":"Alice"}
```

`winner` pode ser `"X"`, `"O"` ou `"draw"`.

Quando há vencedor (`"X"` ou `"O"`), o servidor inclui **`winner_name`**: o valor de `name` enviado na mensagem `join` pelo jogador vencedor. Em empate (`"draw"`) esse campo **não** é enviado.

### `error`

Erro de protocolo ou jogada inválida (só para o cliente que enviou a jogada).

```json
{"type":"error","code":"not_your_turn","message":"Não é a sua vez."}
```

Códigos usados pela lógica de jogo: `not_your_turn`, `cell_occupied`, `game_over`, `out_of_bounds`. Protocolo: `join_required`, `unknown_type`, `bad_move`.

### `opponent_disconnected`

O outro jogador fechou a conexão.

```json
{"type":"opponent_disconnected","message":"O outro jogador desconectou."}
```

## Checklist Pygame (ou outro front)

1. `socket.create_connection((host, port))` no thread principal ou em thread auxiliar.
2. Enviar `join` com `\n` no final da string UTF-8.
3. Loop: ler bytes, acumular até `\n`, `json.loads` na linha, atualizar modelo local (tabuleiro, `current_turn`, `phase`, `winner`, e `winner_name` quando presente).
4. Desenhar o tabuleiro a partir de `board` e do seu `role` recebido em `game_start`.
5. No clique: se `current_turn` for o seu `role` e `phase == "playing"`, calcular `(row, col)` e enviar `move`.
6. Não bloquear o loop de eventos: use thread + fila (`queue.Queue`) ou `asyncio` com integração ao relógio do Pygame.

## Teste manual rápido

Em dois terminais (com o servidor rodando):

```bash
printf '%s\n' '{"type":"join","name":"p1"}' | nc -q 1 127.0.0.1 5001
```

```bash
printf '%s\n' '{"type":"join","name":"p2"}' | nc -q 1 127.0.0.1 5001
```

Depois envie linhas `move` em cada terminal conforme o turno.
