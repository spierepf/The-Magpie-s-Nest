import unittest
from unittest.mock import Mock

try:
    from umockpin.mock_pin_factory import MockPinFactory
    from umockpin.mock_pin_net import MockPinNet
except:
    from lib.umockpin.mock_pin_factory import MockPinFactory
    from lib.umockpin.mock_pin_net import MockPinNet

from game_controller import GameController
from node import Node
from node_pair import NodePair


class GameControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.mpf = MockPinFactory()

    def connect_pins(self, i, j):
        net = MockPinNet()
        net.attach_pin(self.mpf.Pin(i))
        net.attach_pin(self.mpf.Pin(j))

    def test_polling_a_game_controller_will_poll_its_node_pairs(self):
        node_pair = Mock()
        node_pair.poll.return_value = False
        game_controller = GameController([node_pair])
        game_controller.poll()

        node_pair.poll.assert_called_once_with()

    def test_game_controller_poll_only_returns_false_when_all_node_pairs_connected(self):
        node_pairs = []
        for pin_id in range(0, 10, 2):
            node_pairs.append(NodePair(Node(self.mpf.Pin(pin_id)), Node(self.mpf.Pin(pin_id + 1))))
        game_controller = GameController(node_pairs)

        for pin_id in range(0, 8, 2):
            self.connect_pins(pin_id, pin_id + 1)
            assert game_controller.poll() == True

        self.connect_pins(8, 9)
        assert game_controller.poll() == False


if __name__ == '__main__':
    unittest.main()
