from __future__ import annotations

import asyncio

from game.models import Mark, PlayError, PlayOutcome
from server.line_io import JsonLineReader
from server.matchmaker import Matchmaker
from server.protocol import encode_line
from server.remote_session import RemoteGameSession
from server.waiting_player import WaitingPlayer


def _play_error_message(outcome: PlayOutcome) -> str:
    if outcome.error is PlayError.NOT_YOUR_TURN:
        return "Não é a sua vez."
    if outcome.error is PlayError.CELL_OCCUPIED:
        return "Casa já ocupada."
    if outcome.error is PlayError.GAME_OVER:
        return "Partida já encerrada."
    if outcome.error is PlayError.OUT_OF_BOUNDS:
        return "Índice fora do tabuleiro (use 0, 1 ou 2)."
    return "Jogada inválida."


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
    matchmaker: Matchmaker,
) -> None:
    jlr = JsonLineReader(reader)
    session: RemoteGameSession | None = None
    my_mark: Mark | None = None
    wp_for_abandon: WaitingPlayer | None = None

    try:
        msg = await jlr.read_object()
        if msg is None:
            return
        if msg.get("type") != "join":
            writer.write(
                encode_line(
                    {
                        "type": "error",
                        "code": "join_required",
                        "message": "A primeira mensagem deve ser `join`.",
                    }
                )
            )
            await writer.drain()
            return

        name = str(msg.get("name", "anon"))
        wp = WaitingPlayer(name=name, writer=writer)
        wp_for_abandon = wp
        session, my_mark = await matchmaker.register(wp)
        wp_for_abandon = None

        while True:
            msg = await jlr.read_object()
            if msg is None:
                break
            if msg.get("type") != "move":
                writer.write(
                    encode_line(
                        {
                            "type": "error",
                            "code": "unknown_type",
                            "message": (
                                f"Esperado `move`, recebido {msg.get('type')!r}."
                            ),
                        }
                    )
                )
                await writer.drain()
                continue

            row, col = msg.get("row"), msg.get("col")
            if not isinstance(row, int) or not isinstance(col, int):
                writer.write(
                    encode_line(
                        {
                            "type": "error",
                            "code": "bad_move",
                            "message": "`row` e `col` devem ser inteiros.",
                        }
                    )
                )
                await writer.drain()
                continue

            assert my_mark is not None and session is not None
            outcome = await session.try_move(my_mark, row, col)
            if not outcome.ok:
                assert outcome.error is not None
                writer.write(
                    encode_line(
                        {
                            "type": "error",
                            "code": outcome.error.value,
                            "message": _play_error_message(outcome),
                        }
                    )
                )
                await writer.drain()

    except ConnectionAbortedError:
        pass
    finally:
        if wp_for_abandon is not None:
            await matchmaker.abandon_if_waiting(wp_for_abandon)
        if session is not None and my_mark is not None:
            await session.close_and_notify_other(my_mark)
        try:
            writer.close()
            await writer.wait_closed()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
