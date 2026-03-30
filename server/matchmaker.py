from __future__ import annotations

import asyncio

from game.models import Mark
from server.remote_session import RemoteGameSession
from server.waiting_player import WaitingPlayer


class Matchmaker:
    """Primeiro cliente aguarda; o segundo fecha o par (X = primeiro, O = segundo)."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._pending: (
            tuple[WaitingPlayer, asyncio.Future[tuple[RemoteGameSession, Mark]]] | None
        ) = None

    async def register(self, player: WaitingPlayer) -> tuple[RemoteGameSession, Mark]:
        loop = asyncio.get_running_loop()
        future: asyncio.Future[tuple[RemoteGameSession, Mark]] | None = None

        async with self._lock:
            if self._pending is None:
                future = loop.create_future()
                self._pending = (player, future)
            else:
                first, first_future = self._pending
                self._pending = None
                session = RemoteGameSession(first, player)
                await session.send_initial_to_both()
                first_future.set_result((session, Mark.X))
                return session, Mark.O

        assert future is not None
        await self._send_waiting(player)
        return await future

    async def abandon_if_waiting(self, player: WaitingPlayer) -> None:
        """Se este jogador era o único na fila, libera o slot (ex.: desconexão)."""
        async with self._lock:
            if self._pending is None:
                return
            waiting, fut = self._pending
            if waiting is not player:
                return
            self._pending = None
            if not fut.done():
                msg = "desconectado antes do oponente"
                fut.set_exception(ConnectionAbortedError(msg))

    @staticmethod
    async def _send_waiting(player: WaitingPlayer) -> None:
        from server.protocol import encode_line

        payload = {
            "type": "waiting",
            "message": "Aguardando outro jogador conectar.",
        }
        player.writer.write(encode_line(payload))
        await player.writer.drain()
