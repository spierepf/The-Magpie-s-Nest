import logging

log = logging.getLogger(__name__)


class GameController:
    def __init__(self, node_pairs):
        self._node_pairs = set(node_pairs)
        for node_pair in self._node_pairs:
            log.info(f'Configured pair: {node_pair}')

    def poll(self):
        incomplete = False
        for node_pair in self._node_pairs:
            incomplete |= node_pair.poll()
        return incomplete
