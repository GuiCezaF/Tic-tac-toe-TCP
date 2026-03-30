from __future__ import annotations

import json
from asyncio import StreamReader
from typing import Any, cast


class JsonLineReader:
    """Acumula bytes até um '\\n' e interpreta a linha como um objeto JSON."""

    def __init__(self, reader: StreamReader) -> None:
        self._reader = reader
        self._buffer = b""

    async def read_object(self) -> dict[str, Any] | None:
        """Próximo objeto ou None se o stream fechou antes de completar uma linha."""
        while True:
            idx = self._buffer.find(b"\n")
            if idx >= 0:
                line = self._buffer[:idx]
                self._buffer = self._buffer[idx + 1 :]
                stripped = line.strip()
                if not stripped:
                    continue
                return cast(dict[str, Any], json.loads(stripped.decode("utf-8")))

            chunk = await self._reader.read(65536)
            if not chunk:
                return None
            self._buffer += chunk
