from __future__ import annotations

import asyncio

from server.client_handler import handle_client
from server.matchmaker import Matchmaker
from server.network_info import print_connection_hints


class GameServer:
    """Escuta conexões e pareia jogadores em `RemoteGameSession`."""

    def __init__(self, host: str = "0.0.0.0", port: int = 5001) -> None:
        self._host = host
        self._port = port
        self._matchmaker = Matchmaker()

    async def serve(self) -> None:
        server = await asyncio.start_server(
            self._on_client,
            self._host,
            self._port,
        )
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets or ())
        print(f"Servidor escutando em {addrs}")
        await print_connection_hints(self._port)
        async with server:
            await server.serve_forever()

    async def _on_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        await handle_client(reader, writer, self._matchmaker)
