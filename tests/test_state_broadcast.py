from __future__ import annotations

from game import Mark, TicTacToe
from server.remote_session import build_state_broadcast_payload


def test_winner_name_when_x_wins() -> None:
    g = TicTacToe()
    assert g.play(0, 0, Mark.X).ok
    assert g.play(1, 0, Mark.O).ok
    assert g.play(0, 1, Mark.X).ok
    assert g.play(1, 1, Mark.O).ok
    assert g.play(0, 2, Mark.X).ok
    names = {Mark.X: "Alice", Mark.O: "Bob"}
    body = build_state_broadcast_payload(g.snapshot(), names)
    assert body["winner"] == "X"
    assert body["winner_name"] == "Alice"


def test_winner_name_when_o_wins() -> None:
    g = TicTacToe()
    assert g.play(0, 0, Mark.X).ok
    assert g.play(1, 0, Mark.O).ok
    assert g.play(0, 1, Mark.X).ok
    assert g.play(1, 1, Mark.O).ok
    assert g.play(2, 2, Mark.X).ok
    assert g.play(1, 2, Mark.O).ok
    names = {Mark.X: "Alice", Mark.O: "Bob"}
    body = build_state_broadcast_payload(g.snapshot(), names)
    assert body["winner"] == "O"
    assert body["winner_name"] == "Bob"


def test_no_winner_name_on_draw() -> None:
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
    body = build_state_broadcast_payload(
        g.snapshot(), {Mark.X: "Alice", Mark.O: "Bob"}
    )
    assert body["winner"] == "draw"
    assert "winner_name" not in body


def test_no_winner_name_while_playing() -> None:
    g = TicTacToe()
    assert g.play(0, 0, Mark.X).ok
    body = build_state_broadcast_payload(
        g.snapshot(), {Mark.X: "Alice", Mark.O: "Bob"}
    )
    assert body["phase"] == "playing"
    assert "winner_name" not in body
