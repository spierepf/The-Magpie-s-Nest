try:
    from upatterns.observable import Observable
except:
    from lib.upatterns.observable import Observable


class NodePair:
    def __init__(self, node1, node2):
        assert node1.pin() != node2.pin()
        self.observers = Observable()
        self._node1 = node1
        self._node2 = node2
        self._connection_state = self._get_connection_state()

    def _get_connection_state(self):
        return self._node1.is_connected_to(self._node2)

    def poll(self):
        current_connection_state = self._get_connection_state()
        if self._connection_state == current_connection_state:
            return
        self._connection_state = current_connection_state
        self.observers.notify(self, self._connection_state)
