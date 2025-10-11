import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class NodePair:
    def __init__(self, node1, node2, give_hint=lambda: None, confirm=lambda: None):
        assert node1.pin() != node2.pin()
        self._node1 = node1
        self._node2 = node2
        self._connection_state = self._evaluate_connection_state()
        self.give_hint = give_hint
        self.confirm = confirm

    def _evaluate_connection_state(self):
        return self._node1.is_connected_to(self._node2)

    def poll(self):
        current_connection_state = self._evaluate_connection_state()
        if self._connection_state != current_connection_state:
            self._connection_state = current_connection_state
            log.info(f"{self} connection state changed to: {self._connection_state}")
            if self._connection_state:
                self.confirm()

        return not current_connection_state

    def __repr__(self):
        return f"<NodePair: {self._node1}, {self._node2}>"

    def is_connected(self):
        return self._connection_state
