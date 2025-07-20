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

    def test_game_controller_can_give_hints(self):
        node_pair = Mock()
        game_controller = GameController([node_pair])
        game_controller.give_hint()

        node_pair.give_hint.assert_called_once()

    def test_game_controller_rotates_hints(self):
        node_pair1 = Mock()
        node_pair2 = Mock()
        game_controller = GameController([node_pair1, node_pair2])

        game_controller.give_hint()
        node_pair1.give_hint.assert_called_once()

        game_controller.give_hint()
        node_pair2.give_hint.assert_called_once()

    def test_game_controller_skips_connected_node_pairs_when_giving_hints(self):
        node_pair1 = Mock()
        node_pair2 = Mock()
        game_controller = GameController([node_pair1, node_pair2])

        node_pair1.is_connected.return_value = True

        game_controller.give_hint()
        node_pair1.give_hint.assert_not_called()
        node_pair2.give_hint.assert_called_once()

    def test_give_hint_does_nothing_if_all_node_pairs_are_connected(self):
        node_pair = Mock()
        node_pair.is_connected.return_value = True
        game_controller = GameController([node_pair])
        game_controller.give_hint()

        node_pair.give_hint.assert_not_called()


if __name__ == '__main__':
    unittest.main()
