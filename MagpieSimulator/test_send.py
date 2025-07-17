#!/usr/bin/env python3
import sys
import requests
import socket
from typing import Dict, List, Any
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener

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
url: str = f"http://{mdns_name}._http._tcp.local./json/state"

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


class MDNSListener(ServiceListener):
    def __init__(self, target_name):
        self.target_name = target_name
        self.address = None

    def add_service(self, zeroconf, type_, name):
        if self.target_name in name:
            info = zeroconf.get_service_info(type_, name)
            if info:
                self.address = socket.inet_ntoa(info.addresses[0])


def resolve_mdns_ip(mdns_name: str) -> str:
    zeroconf = Zeroconf()
    listener = MDNSListener(mdns_name)
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    import time

    timeout = 3
    for _ in range(timeout * 10):
        if listener.address:
            break
        time.sleep(0.1)
    zeroconf.close()
    if not listener.address:
        raise Exception(f"Could not resolve mDNS name: {mdns_name}")
    return listener.address


def test_send(url: str, payload: Dict[str, Any]) -> None:
    """
    Test sending a request using requests (synchronous, resolves mDNS to IP).
    """
    try:
        ip = resolve_mdns_ip(mdns_name)
        url_ip = f"http://{ip}:{port}/json/state"
        resp = requests.post(url_ip, json=payload, timeout=2)
        print(f"Sent to {mdns_name} ({url_ip}): {payload}")
        print(f"Response: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Failed to send: {e}")


test_send(url, payload)
