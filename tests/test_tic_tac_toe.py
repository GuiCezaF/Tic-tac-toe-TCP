from __future__ import annotations

import pytest

from game import Mark, PlayError, TicTacToe


def test_x_wins_first_row() -> None:
    g = TicTacToe()
    assert g.play(0, 0, Mark.X).ok
    assert g.play(1, 0, Mark.O).ok
    assert g.play(0, 1, Mark.X).ok
    assert g.play(1, 1, Mark.O).ok
    r = g.play(0, 2, Mark.X)
    assert r.ok
    assert g.finished
    assert g.snapshot()["winner"] == "X"


def test_draw() -> None:
    g = TicTacToe()
    moves = [
        (0, 0, Mark.X),
        (0, 1, Mark.O),
        (0, 2, Mark.X),
        (1, 1, Mark.O),
        (1, 0, Mark.X),
        (1, 2, Mark.O),
        (2, 1, Mark.X),
        (2, 0, Mark.O),
        (2, 2, Mark.X),
    ]
    for r, c, m in moves:
        assert g.play(r, c, m).ok
    assert g.finished
    assert g.snapshot()["winner"] == "draw"


def test_not_your_turn() -> None:
    g = TicTacToe()
    r = g.play(0, 0, Mark.O)
    assert not r.ok
    assert r.error is PlayError.NOT_YOUR_TURN


def test_occupied_cell() -> None:
    g = TicTacToe()
    assert g.play(1, 1, Mark.X).ok
    assert g.play(0, 0, Mark.O).ok
    r = g.play(1, 1, Mark.X)
    assert not r.ok
    assert r.error is PlayError.CELL_OCCUPIED


def test_out_of_bounds() -> None:
    g = TicTacToe()
    r = g.play(3, 0, Mark.X)
    assert not r.ok
    assert r.error is PlayError.OUT_OF_BOUNDS


def test_reset() -> None:
    g = TicTacToe()
    assert g.play(0, 0, Mark.X).ok
    g.reset()
    snap = g.snapshot()
    assert snap["phase"] == "playing"
    assert snap["current_turn"] == "X"
    assert snap["board"] == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def test_play_after_game_over() -> None:
    g = TicTacToe()
    assert g.play(0, 0, Mark.X).ok
    assert g.play(1, 0, Mark.O).ok
    assert g.play(0, 1, Mark.X).ok
    assert g.play(1, 1, Mark.O).ok
    assert g.play(0, 2, Mark.X).ok
    r = g.play(2, 2, Mark.O)
    assert not r.ok
    assert r.error is PlayError.GAME_OVER


@pytest.mark.parametrize(
    "winning_cells",
    [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ],
)
def test_all_lines_win_for_x(winning_cells: list[tuple[int, int]]) -> None:
    g = TicTacToe()
    other = {(r, c) for r in range(3) for c in range(3)} - set(winning_cells)
    other_list = sorted(other)

    for i, (wr, wc) in enumerate(winning_cells):
        assert g.play(wr, wc, Mark.X).ok
        if i < len(winning_cells) - 1 and i < len(other_list):
            orow, ocol = other_list[i]
            if g.finished:
                break
            assert g.play(orow, ocol, Mark.O).ok

    assert g.finished
    assert g.snapshot()["winner"] == "X"
