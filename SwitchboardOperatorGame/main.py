# noinspection PyUnresolvedReferences
import install

# This is a sample Python script.
import logging
import random
import time

from config import NODES, MIN_HINT_DELAY, MAX_HINT_DELAY, HINT_DURATION, CONFIRM_DURATION

from game_controller import GameController
from node_pair import NodePair
from sequencer import Sequencer, SECOND

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


sequencer = Sequencer()


def reset_to_pride():
    for node in NODES:
        log.info(f"Resetting {node}")
        node.aux["wled"].update().fx("Pride 2015").sx(16).next().done()


def build_node_pair(colour, node0, node1):
    log.info(f"Building node pair from {node0} {node1}")
    def hint():
        node0.aux['wled'].update().fx("Solid").col([colour]).next().done()
        node1.aux['wled'].update().fx("Solid").col([colour]).next().done()

        def end_hint():
            node0.aux['wled'].update().fx("Pride 2015").sx(16).next().done()
            node1.aux['wled'].update().fx("Pride 2015").sx(16).next().done()
            queue_hint()
            
        sequencer.after(HINT_DURATION, end_hint)
            
        
    def confirm():
        node0.aux['wled'].update().fx("Blink").sx(255).col([colour]).next().done()
        node1.aux['wled'].update().fx("Blink").sx(255).col([colour]).next().done()

        def end_confirm():
            node0.aux['wled'].update().fx("Pride 2015").sx(16).next().done()
            node1.aux['wled'].update().fx("Pride 2015").sx(16).next().done()
            
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
        [255,0,0],
        [0,255,0],
        [0,0,255],
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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
