class MockPinNet:
    class PinObserver:
        def __init__(self, net):
            self._net = net

        def update(self, pin, arg=None):
            self._net.verify_max_one_output_pin()

    def __init__(self):
        self._pin_observer = self.PinObserver(self)
        self._pins = set()

    def verify_max_one_output_pin(self):
        output_pins = [pin for pin in self._pins if pin.mode() == pin.OUT]
        if len(output_pins) > 1:
            raise RuntimeError(f"Multiple connected output pins: {output_pins}")

    def value(self):
        for pin in self._pins:
            if pin.mode() == pin.OUT:
                return pin.value()
        for pin in self._pins:
            if pin.mode() == pin.IN and pin.pull() == pin.PULL_UP:
                return True
        return None

    def attach_pin(self, pin):
        if pin._net is not None:
            raise RuntimeError()
        self._pins.add(pin)
        self.verify_max_one_output_pin()
        pin._net = self
        pin.attach_observer(self._pin_observer)

    def detach_pin(self, pin):
        if pin not in self._pins:
            raise RuntimeError()
        self._pins.remove(pin)
        pin._net = None
        pin.detach_observer(self._pin_observer)
