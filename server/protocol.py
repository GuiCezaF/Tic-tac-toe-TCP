from __future__ import annotations

import json
from typing import Any, Literal, TypedDict


def encode_line(payload: dict[str, Any]) -> bytes:
    """Uma mensagem UTF-8 terminada em newline (NDJSON)."""
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    return (raw + "\n").encode("utf-8")


class JoinMessage(TypedDict):
    type: Literal["join"]
    name: str


class MoveMessage(TypedDict):
    type: Literal["move"]
    row: int
    col: int


class WaitingMessage(TypedDict):
    type: Literal["waiting"]
    message: str


class GameStartMessage(TypedDict):
    type: Literal["game_start"]
    role: Literal["X", "O"]
    state: dict[str, Any]


class StateMessage(TypedDict):
    type: Literal["state"]
    board: list[list[int]]
    current_turn: Literal["X", "O"] | None
    phase: Literal["playing", "finished"]
    winner: str | None


class ErrorMessage(TypedDict):
    type: Literal["error"]
    code: str
    message: str


class OpponentLeftMessage(TypedDict):
    type: Literal["opponent_disconnected"]
    message: str
