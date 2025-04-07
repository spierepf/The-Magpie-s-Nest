from tests.mock_pin import MockPin


class MockPinFactory:
    def __init__(self):
        self._pins = dict()

    def Pin(self, id, mode=-1, pull=-1, value=None):
        if id not in self._pins:
            self._pins[id] = MockPin(id)

        pin = self._pins[id]
        pin.init(mode=mode, pull=pull, value=value)
        return pin
