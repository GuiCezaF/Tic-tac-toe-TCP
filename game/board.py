from __future__ import annotations

from game.models import Mark

BOARD_SIZE = 3


class Board:
    """Grade fixa 3x3; não valida turno — só ocupação e limites."""

    def __init__(self) -> None:
        self._cells: list[list[Mark]] = [
            [Mark.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]

    def get(self, row: int, col: int) -> Mark:
        return self._cells[row][col]

    def is_empty(self, row: int, col: int) -> bool:
        return self._cells[row][col] is Mark.EMPTY

    def is_full(self) -> bool:
        return all(
            self._cells[r][c] is not Mark.EMPTY
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
        )

    def place(self, row: int, col: int, mark: Mark) -> None:
        """Grava marca assumindo célula vazia e índices válidos (uso interno)."""
        self._cells[row][col] = mark

    def as_int_grid(self) -> list[list[int]]:
        """Cópia para JSON (valores int de Mark)."""
        return [
            [int(self._cells[r][c]) for c in range(BOARD_SIZE)]
            for r in range(BOARD_SIZE)
        ]

    def line_winner(self) -> Mark | None:
        """Retorna X ou O se alguma linha/coluna/diagonal está completa; senão None."""
        lines: list[list[tuple[int, int]]] = []
        for i in range(BOARD_SIZE):
            lines.append([(i, j) for j in range(BOARD_SIZE)])
            lines.append([(j, i) for j in range(BOARD_SIZE)])
        lines.append([(i, i) for i in range(BOARD_SIZE)])
        lines.append([(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)])

        for coords in lines:
            marks = [self.get(r, c) for r, c in coords]
            if marks[0] is not Mark.EMPTY and marks[0] == marks[1] == marks[2]:
                return marks[0]
        return None
