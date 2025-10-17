# noinspection PyUnresolvedReferences
import install

# This is a sample Python script.
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

import random
import time

from config import NODES, MIN_HINT_DELAY, MAX_HINT_DELAY, HINT_DURATION, CONFIRM_DURATION, WLED_ADDRESSES

from game_controller import GameController
from node_pair import NodePair
from sequencer import Sequencer, SECOND
from uwled.udp_client import udp_message, broadcast_message, send_message_to, get_addr_from_hostname_and_port, EFFECTS, PALETTES


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


sequencer = Sequencer()


def reset_to_pride():
    broadcast_message(udp_message(effect_current=EFFECTS["Pride 2015"]))


colours = [
    [255,0,0,0],
    [255,69,0,0],
    [255,255,0,0],
    [0,255,0,0],
    [0,0,255,0],
    [75,0,130,0],
    [143,0,255,0],
]
messages = list(map(lambda c: udp_message(col=c, effect_current=EFFECTS["Solid"]), colours))


def build_node_pair(colour, node0, node1):
    log.info(f"Building node pair from {colour, node0} {node1}")
    def hint():
        msg = udp_message(col=colour, effect_current=EFFECTS["Solid"])
        send_message_to(msg, WLED_ADDRESSES[node0.aux['wled_name']])
        send_message_to(msg, WLED_ADDRESSES[node1.aux['wled_name']])

        def end_hint():
            reset_to_pride()
            queue_hint()
            
        sequencer.after(HINT_DURATION, end_hint)
            
        
    def confirm():
        msg = udp_message(col=colour, effect_current=EFFECTS["blink"], effect_speed=255)
        send_message_to(msg, WLED_ADDRESSES[node0.aux['wled_name']])
        send_message_to(msg, WLED_ADDRESSES[node1.aux['wled_name']])

        def end_confirm():
            reset_to_pride()
            
        sequencer.after(CONFIRM_DURATION, end_confirm)
        
    return NodePair(node0, node1, hint, confirm)


def hint_task():
    game_controller.give_hint()


def queue_hint():
    delay = random.randrange(MIN_HINT_DELAY, MAX_HINT_DELAY)
    log.info(f"Next hint in {delay/SECOND} seconds")
    sequencer.after(delay, hint_task)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    reset_to_pride()

    colours = [
        [255,0,0,0],
        [0,255,0,0],
        [0,0,255,0],
    ]
    nodes = list(NODES)
    shuffled_elements = []
    for _ in range(len(colours) * 2):
        node = random.choice(nodes)
        nodes.remove(node)
        shuffled_elements.append(node)
    pairs = list(map(lambda n: build_node_pair(*n), zip(colours, shuffled_elements[::2], shuffled_elements[1::2])))
    game_controller = GameController(pairs)

    queue_hint()

    while game_controller.poll():
        time.sleep(0.01)
        sequencer()

    # CELEBRATE

    broadcast_message(udp_message())
    time.sleep(3)

    addresses = list(WLED_ADDRESSES.values())
    for _ in range(100):
        address = random.choice(addresses)
        message = random.choice(messages)
        send_message_to(message, address)
        time.sleep(0.5)

    broadcast_message(udp_message())
    time.sleep(1)

    for _ in range(3):
        broadcast_message(udp_message(effect_current=EFFECTS["Pride 2015"]))
        time.sleep(0.1)
        

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

