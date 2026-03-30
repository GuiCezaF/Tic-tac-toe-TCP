from __future__ import annotations

from asyncio import StreamWriter
from dataclasses import dataclass


@dataclass
class WaitingPlayer:
    """Cliente na fila até formar par; `writer` envia mensagens assíncronas."""

    name: str
    writer: StreamWriter
