#!/usr/bin/env python3
import sys
import requests
import json

from config import BASE_PORT, WLED_NAMES

COLOR_MAP = {
    "red": [255, 0, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "white": [255, 255, 255],
    "yellow": [255, 255, 0],
    "cyan": [0, 255, 255],
    "magenta": [255, 0, 255],
    # Add more as needed
}

PRIDE_FX_ID = 68  # WLED effect ID for "Pride"

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <mdns_name> <color|pride>")
    sys.exit(1)

mdns_name = sys.argv[1]
mode = sys.argv[2].lower()

if mdns_name not in WLED_NAMES:
    print(f"Error: {mdns_name} not found in WLED_NAMES")
    sys.exit(1)

index = WLED_NAMES.index(mdns_name)
port = BASE_PORT + index
url = f"http://127.0.0.1:{port}/json/state"

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
    resp = requests.post(url, json=payload, timeout=2)
    print(f"Sent to {mdns_name} ({url}): {payload}")
    print(f"Response: {resp.status_code} {resp.text}")
except Exception as e:
    print(f"Failed to send: {e}")
