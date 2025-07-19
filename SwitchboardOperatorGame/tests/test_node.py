import unittest

from node import Node

try:
    from umockpin.mock_pin_factory import MockPinFactory
    from umockpin.mock_pin_net import MockPinNet
except:
    from lib.umockpin.mock_pin_factory import MockPinFactory
    from lib.umockpin.mock_pin_net import MockPinNet


class TestNode(unittest.TestCase):
    def setUp(self):
        self.mpf = MockPinFactory()
        self.node_pin = self.mpf.Pin(0)
        self.node = Node(self.node_pin)
        self.other_node_pin = self.mpf.Pin(1)
        self.other_node = Node(self.other_node_pin)

    def test_disconnected_nodes_read_as_disconnected(self):
        assert not self.node.is_connected_to(self.other_node)

    def test_nodes_whose_pins_are_attached_to_the_same_net_read_as_connected(self):
        net = MockPinNet()
        net.attach_pin(self.node_pin)
        net.attach_pin(self.other_node_pin)
        assert self.node.is_connected_to(self.other_node)

    def test_pins_returned_to_input_with_no_pull_up_after_connection_check(self):
        self.node.is_connected_to(self.other_node)
        assert self.node_pin.mode() == self.node_pin.IN
        assert self.node_pin.pull() is None
        assert self.other_node_pin.mode() == self.other_node_pin.IN
        assert self.other_node_pin.pull() is None
