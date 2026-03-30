from __future__ import annotations

import asyncio
import socket
import urllib.error
import urllib.request


def local_outbound_ip() -> str | None:
    """
    IP da interface usada para tráfego de saída (útil na mesma LAN).
    Não envia pacotes; só escolhe a rota até 8.8.8.8.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        addr = sock.getsockname()[0]
        if isinstance(addr, str) and addr:
            return addr
        return None
    except OSError:
        return None
    finally:
        sock.close()


def public_ip(timeout: float = 3.0) -> str | None:
    """Consulta um serviço externo (sem dependências além da stdlib)."""
    url = "https://api.ipify.org"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            text = response.read().decode().strip()
            return text or None
    except (OSError, urllib.error.URLError):
        return None


async def print_connection_hints(port: int) -> None:
    """Imprime IPs que o anfitrião pode passar ao outro jogador."""
    local = local_outbound_ip()
    if local:
        print(f"IP na rede local (mesma Wi-Fi/LAN): {local}:{port}")
    else:
        print("Não foi possível detectar o IP da rede local.")

    pub = await asyncio.to_thread(public_ip)
    if pub:
        print(f"IP público (internet): {pub}:{port}")
        print(
            "Se o outro jogador estiver fora da sua rede, libere a porta "
            f"{port} no roteador (encaminhamento) e no firewall."
        )
    else:
        print(
            "IP público não obtido (sem internet ou serviço indisponível). "
            "Na mesma rede, use o IP local acima."
        )
