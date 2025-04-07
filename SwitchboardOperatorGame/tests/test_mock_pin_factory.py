import unittest

from tests.mock_pin_factory import MockPinFactory


class TestMockPinFactory(unittest.TestCase):
    def setUp(self):
        self.mpf = MockPinFactory()

    def test_mockpinfactory_pins_with_the_same_id_are_the_same_object(self):
        assert self.mpf.Pin(0) == self.mpf.Pin(0)
        assert self.mpf.Pin(1) == self.mpf.Pin(1)

    def test_mockpinfactory_pins_with_the_different_ids_are_different_objects(self):
        assert self.mpf.Pin(0) != self.mpf.Pin(1)
        assert self.mpf.Pin(1) != self.mpf.Pin(0)
