import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from uwled.udp_client import get_addr_from_hostname_and_port
import machine
from node import Node
from sequencer import MINUTE, SECOND

MIN_HINT_DELAY=1 * MINUTE
MAX_HINT_DELAY=2 * MINUTE
HINT_DURATION=1 * MINUTE
CONFIRM_DURATION=30 * SECOND

wled_names = [
    "portal-1-1",
    "portal-1-2",
    "portal-1-3",
    "portal-2-1",
    "portal-2-2",
    "portal-2-3",
    "portal-2-4",
    "portal-2-5",
    "portal-3-1",
    "portal-3-2",
    "portal-4-1",
    "portal-4-2",
    "portal-4-3",
    "portal-4-4",
    "portal-4-5",
    "portal-5-1",
    "portal-5-2",
    "portal-5-3",
    "exquisite-corpse",
    "fruit_platter",
    "intrados",
    "time-and-space",
]

WLED_ADDRESSES = dict(map(lambda n: (n, get_addr_from_hostname_and_port(f"wled-{n}.local", 21324)), wled_names))

node_descriptors = [
    (15, "portal-1-1"),
    (2,  "portal-1-2"),
    (4,  "portal-2-1"),
    (16, "portal-2-2"),
    (17, "portal-2-3"),
    (5,  "portal-2-4"),
    (18, "portal-2-5"),
    (19, "portal-3-1"),
    (32, "portal-3-2"),
    (33, "portal-4-1"),
    (25, "portal-4-2"),
    (26, "portal-4-3"),
    (27, "portal-4-4"),
    (14, "portal-4-5"),
    (12, "portal-5-1"),
    (13, "portal-5-3"),
]

NODES=[]

for (gpio, wled_name) in node_descriptors:
    try:
        NODES.append(Node(machine.Pin(gpio), wled_name=wled_name))
        log.info(f"Built {(gpio, wled_name)}.")
    except OSError as e:
        log.error(f"Building {(gpio, wled_name)} failed: {e}")
