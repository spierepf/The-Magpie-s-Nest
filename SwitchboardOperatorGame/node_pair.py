class NodePair:
    def __init__(self, node1, node2):
        assert node1.pin() != node2.pin()
        self._node1 = node1
        self._node2 = node2
        self._connection_state = self._get_connection_state()

    def _get_connection_state(self):
        return self._node1.is_connected_to(self._node2)

    def poll(self):
        current_connection_state = self._get_connection_state()
        if self._connection_state != current_connection_state:
            self._connection_state = current_connection_state
        return not current_connection_state

    def __repr__(self):
        return f"<NodePair: {self._node1}, {self._node2}>"
