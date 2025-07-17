from lib.upatterns.observable import Observable


class GameController:
    def __init__(self, node_pairs):
        self.observers = Observable()
        self._node_pairs = set(node_pairs)
        self._connected_node_pairs = set()
        for node_pair in self._node_pairs:
            node_pair.observers.attach(self._pair_connection_state_change)

    def poll(self):
        for node_pair in self._node_pairs:
            node_pair.poll()
        if self._node_pairs == self._connected_node_pairs:
            self.observers.notify()

    def _pair_connection_state_change(self, pair, are_connected):
        if are_connected:
            self._connected_node_pairs.add(pair)
        else:
            self._connected_node_pairs.remove(pair)
