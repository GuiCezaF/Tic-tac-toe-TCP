from __future__ import annotations

import asyncio
import os

from server import GameServer


def main() -> None:
    host = os.environ.get("TICTACTOE_HOST", "0.0.0.0")
    port = int(os.environ.get("TICTACTOE_PORT", "5001"))
    asyncio.run(GameServer(host=host, port=port).serve())


if __name__ == "__main__":
    main()
