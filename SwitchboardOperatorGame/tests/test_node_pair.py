import unittest
from unittest.mock import Mock

from node import Node
from node_pair import NodePair
from umockpin.mock_pin_factory import MockPinFactory
from umockpin.mock_pin_net import MockPinNet


class NodePairTestCase(unittest.TestCase):
    def setUp(self):
        self.mpf = MockPinFactory()
        self.pin0 = self.mpf.Pin(0)
        self.pin1 = self.mpf.Pin(1)
        self.node0 = Node(self.pin0)
        self.node1 = Node(self.pin1)
        self.node_pair = NodePair(self.node0, self.node1)
        self.net = MockPinNet()

    def connect_pins(self):
        self.net.attach_pin(self.pin0)
        self.net.attach_pin(self.pin1)

    def disconnect_pins(self):
        self.net.detach_pin(self.pin0)
        self.net.detach_pin(self.pin1)

    def test_disconnected_node_pair_does_not_accept_nodes_with_the_same_pin(self):
        self.assertRaises(AssertionError, lambda: NodePair(Node(self.pin0), Node(self.pin0)))

    def test_node_pair_notifies_observers_when_pins_become_connected(self):
        spy = Mock()
        self.node_pair.observers.attach(spy)

        self.connect_pins()

        self.node_pair.poll()

        spy.assert_called_once_with(self.node_pair, True)

    def test_connected_node_pair_notifies_observers_when_pins_become_disconnected(self):
        self.connect_pins()

        self.node_pair.poll()
        spy = Mock()
        self.node_pair.observers.attach(spy)

        self.disconnect_pins()

        self.node_pair.poll()

        spy.assert_called_once_with(self.node_pair, False)

    def test_disconnected_node_pair_does_not_notify_observers_when_connection_state_does_not_change(self):
        self.node_pair.poll()
        spy = Mock()
        self.node_pair.observers.attach(spy)

        self.node_pair.poll()

        spy.assert_not_called()

    def test_connected_node_pair_does_not_notify_observers_when_connection_state_does_not_change(self):
        self.connect_pins()

        self.node_pair.poll()
        spy = Mock()
        self.node_pair.observers.attach(spy)

        self.node_pair.poll()

        spy.assert_not_called()


if __name__ == '__main__':
    unittest.main()
