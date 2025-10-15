import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

from uwledclient import WLEDNode
import machine
from node import Node
from sequencer import MINUTE, SECOND

MIN_HINT_DELAY=1 * MINUTE
MAX_HINT_DELAY=2 * MINUTE
HINT_DURATION=1 * MINUTE
CONFIRM_DURATION=30 * SECOND

node_descriptors = [
    (15, "http://wled-portal-1-1.local"),
    (2,  "http://wled-portal-1-2.local"),
    (4,  "http://wled-portal-2-1.local"),
    (16, "http://wled-portal-2-2.local"),
    (17, "http://wled-portal-2-3.local"),
    (5,  "http://wled-portal-2-4.local"),
    (18, "http://wled-portal-2-5.local"),
    (19, "http://wled-portal-3-1.local"),
    (32, "http://wled-portal-3-2.local"),
    (33, "http://wled-portal-4-1.local"),
    (25, "http://wled-portal-4-2.local"),
    (26, "http://wled-portal-4-3.local"),
    (27, "http://wled-portal-4-4.local"),
    (14, "http://wled-portal-4-5.local"),
    (12, "http://wled-portal-5-1.local"),
    (13, "http://wled-portal-5-3.local"),
]

NODES=[]

for (gpio, url) in node_descriptors:
    try:
        gpio_node = machine.Pin(gpio)
        wled_node = WLEDNode(url)
        NODES.append(Node(gpio_node, wled=wled_node))
        log.info(f"Building {(gpio, url)}.")
    except OSError:
        log.error(f"Building {(gpio, url)} failed.")
        pass
