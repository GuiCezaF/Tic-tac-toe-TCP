from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Literal, NotRequired, TypedDict


class Mark(IntEnum):
    """Valor da célula no tabuleiro e no JSON (0 vazio, 1 X, 2 O)."""

    EMPTY = 0
    X = 1
    O = 2


class PlayError(StrEnum):
    """Motivo de falha quando uma jogada não é aplicada."""

    NOT_YOUR_TURN = "not_your_turn"
    CELL_OCCUPIED = "cell_occupied"
    GAME_OVER = "game_over"
    OUT_OF_BOUNDS = "out_of_bounds"


@dataclass(frozen=True)
class PlayOutcome:
    """Resultado de tentar aplicar uma jogada na partida."""

    error: PlayError | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

    @staticmethod
    def success() -> PlayOutcome:
        return PlayOutcome(error=None)

    @staticmethod
    def fail(reason: PlayError) -> PlayOutcome:
        return PlayOutcome(error=reason)


class GameSnapshot(TypedDict):
    """Estado serializável da partida para o protocolo de rede."""

    board: list[list[int]]
    current_turn: Literal["X", "O"] | None
    phase: Literal["playing", "finished"]
    winner: NotRequired[Literal["X", "O", "draw"] | None]
    # Preenchido só na rede quando phase == "finished" e há vencedor (não em empate).
    winner_name: NotRequired[str]
