#!/usr/bin/env python3
import sys
import requests
from typing import Dict, List, Any
import asyncio
import aiohttp
from aiohttp_asyncmdnsresolver.api import AsyncMDNSResolver

from config import BASE_PORT, WLED_NAMES

COLOR_MAP: Dict[str, List[int]] = {
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "white": [255, 255, 255],
    "yellow": [255, 255, 0],
    "cyan": [0, 255, 255],
    "magenta": [255, 0, 255],
    # Add more as needed
}

PRIDE_FX_ID: int = 68  # WLED effect ID for "Pride"

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <mdns_name> <color|pride>")
    sys.exit(1)

mdns_name: str = sys.argv[1]
mode: str = sys.argv[2].lower()

if mdns_name not in WLED_NAMES:
    print(f"Error: {mdns_name} not found in WLED_NAMES")
    sys.exit(1)

index: int = WLED_NAMES.index(mdns_name)
port: int = BASE_PORT + index
url: str = f"http://{mdns_name}._http._tcp.local.:{port}/json/state"

payload: Dict[str, Any]
if mode == "pride":
    payload = {"on": True, "fx": PRIDE_FX_ID}
else:
    color = COLOR_MAP.get(mode)
    if not color:
        print(f"Unknown color: {mode}")
        sys.exit(1)
    payload = {
        "on": True,
        "seg": [{"id": 0, "col": [color]}, {"id": 1, "col": [color]}],
    }

try:
    print(f"Sending to {mdns_name} ({url}): {payload}")
    resp = requests.post(url, json=payload, timeout=2)
    print(f"Response: {resp.status_code} {resp.text}")
except Exception as e:
    print(f"Failed to send: {e}")


def test_send() -> None:
    """
    Test sending a request using aiohttp and aiohttp-asyncmdnsresolver to resolve mDNS names.
    """

    async def send():
        mdns_name = WLED_NAMES[0]  # Example: use the first name for test
        mode = "red"  # Example: use red for test
        index = WLED_NAMES.index(mdns_name)
        port = BASE_PORT + index
        url = f"http://{mdns_name}._http._tcp.local.:{port}/json/state"

        # Use aiohttp with AsyncMDNSResolver
        resolver = AsyncMDNSResolver()
        connector = aiohttp.TCPConnector(resolver=resolver)
        async with aiohttp.ClientSession(connector=connector) as session:
            if mode == "pride":
                payload = {"on": True, "fx": PRIDE_FX_ID}
            else:
                color = COLOR_MAP.get(mode)
                if not color:
                    print(f"Unknown color: {mode}")
                    return
                payload = {
                    "on": True,
                    "seg": [
                        {"id": 0, "col": [color]},
                        {"id": 1, "col": [color]},
                    ],
                }
            try:
                async with session.post(url, json=payload, timeout=2) as resp:
                    text = await resp.text()
                    print(f"Sent to {mdns_name} ({url}): {payload}")
                    print(f"Response: {resp.status} {text}")
            except Exception as e:
                print(f"Failed to send: {e}")

    asyncio.run(send())
