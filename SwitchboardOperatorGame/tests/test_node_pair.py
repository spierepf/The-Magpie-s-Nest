import unittest

from node import Node
from node_pair import NodePair

try:
    from umockpin.mock_pin_factory import MockPinFactory
    from umockpin.mock_pin_net import MockPinNet
except:
    from lib.umockpin.mock_pin_factory import MockPinFactory
    from lib.umockpin.mock_pin_net import MockPinNet


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

    def test_node_pair_does_not_accept_nodes_with_the_same_pin(self):
        self.assertRaises(AssertionError, lambda: NodePair(Node(self.pin0), Node(self.pin0)))

    def test_node_pair_poll_returns_true_when_pins_disconnected(self):
        assert self.node_pair.poll() == True

    def test_node_pair_poll_returns_false_when_pins_connected(self):
        self.connect_pins()
        assert self.node_pair.poll() == False


if __name__ == '__main__':
    unittest.main()
