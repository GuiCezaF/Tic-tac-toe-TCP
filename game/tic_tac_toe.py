from __future__ import annotations

from typing import Literal

from game.board import BOARD_SIZE, Board
from game.models import GameSnapshot, Mark, PlayError, PlayOutcome

WinnerLiteral = Literal["X", "O", "draw"]


class TicTacToe:
    """Uma partida; X sempre começa. Estado mutável até `reset`."""

    def __init__(self) -> None:
        self._board = Board()
        self._current: Mark = Mark.X
        self._finished: bool = False
        self._winner: WinnerLiteral | None = None

    def reset(self) -> None:
        self._board = Board()
        self._current = Mark.X
        self._finished = False
        self._winner = None

    @property
    def finished(self) -> bool:
        return self._finished

    def snapshot(self) -> GameSnapshot:
        turn: str | None
        if self._finished:
            turn = None
        else:
            turn = _mark_to_role(self._current)
        snap: GameSnapshot = {
            "board": self._board.as_int_grid(),
            "current_turn": turn,
            "phase": "finished" if self._finished else "playing",
        }
        if self._finished:
            assert self._winner is not None
            snap["winner"] = self._winner
        return snap

    def play(self, row: int, col: int, mark: Mark) -> PlayOutcome:
        if self._finished:
            return PlayOutcome.fail(PlayError.GAME_OVER)
        if mark is not self._current:
            return PlayOutcome.fail(PlayError.NOT_YOUR_TURN)
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return PlayOutcome.fail(PlayError.OUT_OF_BOUNDS)
        if not self._board.is_empty(row, col):
            return PlayOutcome.fail(PlayError.CELL_OCCUPIED)

        self._board.place(row, col, mark)
        line = self._board.line_winner()
        if line is not None:
            self._finished = True
            self._winner = "X" if line is Mark.X else "O"
            return PlayOutcome.success()
        if self._board.is_full():
            self._finished = True
            self._winner = "draw"
            return PlayOutcome.success()

        self._current = Mark.O if mark is Mark.X else Mark.X
        return PlayOutcome.success()


def _mark_to_role(mark: Mark) -> Literal["X", "O"]:
    if mark is Mark.X:
        return "X"
    if mark is Mark.O:
        return "O"
    raise ValueError("EMPTY não tem papel de jogador")
