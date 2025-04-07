import unittest

from tests.mock_pin import MockPin
from tests.mock_pin_factory import MockPinFactory


class TestMockPin(unittest.TestCase):
    def setUp(self):
        self.mpf = MockPinFactory()

    def test_mockpin_has_mode(self):
        assert self.mpf.Pin(0, mode=MockPin.IN).mode() == MockPin.IN
        assert self.mpf.Pin(0, mode=MockPin.OUT).mode() == MockPin.OUT

    def test_mockpin_has_pull(self):
        assert self.mpf.Pin(0, pull=MockPin.PULL_UP).pull() == MockPin.PULL_UP
        assert self.mpf.Pin(0, pull=None).pull() is None

    def test_mockpin_has_value(self):
        assert self.mpf.Pin(0, value=True).value() == True
        assert self.mpf.Pin(0, value=False).value() == False

    def mockpin_notifies_observers(self, method, old_state, new_state):
        class Observer:
            def __init__(self):
                self.arg = None
                self.pin = None

            def update(self, observable, arg):
                self.pin = observable
                self.arg = arg

        observer = Observer()
        pin = self.mpf.Pin(0)

        method(pin, old_state)
        pin.attach_observer(observer)
        method(pin, old_state)
        assert observer.pin is None
        method(pin, new_state)
        assert observer.pin == pin

    def test_mockpin_notifies_observers_according_to_value(self):
        self.mockpin_notifies_observers(MockPin.value, True, False)

    def test_mockpin_notifies_observers_according_to_mode(self):
        self.mockpin_notifies_observers(MockPin.mode, MockPin.IN, MockPin.OUT)

    def test_mockpin_notifies_observers_according_to_pull(self):
        self.mockpin_notifies_observers(MockPin.pull, None, MockPin.PULL_UP)
