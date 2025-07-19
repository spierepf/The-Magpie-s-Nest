import logging

log = logging.getLogger(__name__)


class GameController:
    def __init__(self, node_pairs):
        self._node_pairs = set(node_pairs)
        self._connected_node_pairs = set()
        for node_pair in self._node_pairs:
            log.info(f'Configured pair: {node_pair}')
            node_pair.observers.attach(self._pair_connection_state_change)

    def poll(self):
        for node_pair in self._node_pairs:
            node_pair.poll()
        return self._node_pairs != self._connected_node_pairs

    def _pair_connection_state_change(self, pair, are_connected):
        log.info(f'{pair} connection state change: {are_connected}')
        if are_connected:
            self._connected_node_pairs.add(pair)
        else:
            self._connected_node_pairs.remove(pair)
