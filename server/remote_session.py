from __future__ import annotations

import asyncio

from game.models import GameSnapshot, Mark, PlayError, PlayOutcome
from game.tic_tac_toe import TicTacToe
from server.protocol import encode_line
from server.waiting_player import WaitingPlayer


def build_state_broadcast_payload(
    snap: GameSnapshot, player_names: dict[Mark, str]
) -> dict[str, object]:
    """Monta o corpo de `state`.

    Acrescenta `winner_name` apenas se houver vencedor (não em empate).
    """
    body: dict[str, object] = {"type": "state", **snap}
    if snap.get("phase") == "finished":
        winner = snap.get("winner")
        if winner == "X":
            body["winner_name"] = player_names[Mark.X]
        elif winner == "O":
            body["winner_name"] = player_names[Mark.O]
    return body


class RemoteGameSession:
    """Isola estado da partida e envia o mesmo snapshot para ambos os clientes."""

    def __init__(self, first: WaitingPlayer, second: WaitingPlayer) -> None:
        self._game = TicTacToe()
        self._writers: dict[Mark, asyncio.StreamWriter] = {
            Mark.X: first.writer,
            Mark.O: second.writer,
        }
        self._player_names: dict[Mark, str] = {Mark.X: first.name, Mark.O: second.name}
        self._lock = asyncio.Lock()
        self._closed = False

    async def broadcast_game_start(self, mark: Mark, snapshot: GameSnapshot) -> None:
        role = "X" if mark is Mark.X else "O"
        payload = {"type": "game_start", "role": role, "state": dict(snapshot)}
        line = encode_line(payload)
        self._writers[mark].write(line)
        await self._writers[mark].drain()

    async def send_initial_to_both(self) -> None:
        """Chamado uma única vez ao formar o par: mesmo tabuleiro, papéis distintos."""
        snap = self._game.snapshot()
        await self.broadcast_game_start(Mark.X, snap)
        await self.broadcast_game_start(Mark.O, snap)

    async def try_move(self, mark: Mark, row: int, col: int) -> PlayOutcome:
        async with self._lock:
            if self._closed:
                return PlayOutcome.fail(PlayError.GAME_OVER)
            outcome = self._game.play(row, col, mark)
            if outcome.ok:
                await self._broadcast_state_unlocked()
            return outcome

    async def _broadcast_state_unlocked(self) -> None:
        snap = self._game.snapshot()
        body = build_state_broadcast_payload(snap, self._player_names)
        data = encode_line(body)
        for w in self._writers.values():
            w.write(data)
            await w.drain()

    async def close_and_notify_other(self, leaver_mark: Mark | None) -> None:
        """Encerra a sessão; avisa o oponente se a partida tinha começado."""
        async with self._lock:
            if self._closed:
                return
            self._closed = True
            msg = encode_line(
                {
                    "type": "opponent_disconnected",
                    "message": "O outro jogador desconectou.",
                }
            )
            for mark, w in self._writers.items():
                if leaver_mark is None or mark is not leaver_mark:
                    try:
                        w.write(msg)
                        await w.drain()
                    except (BrokenPipeError, ConnectionResetError, OSError):
                        pass
