class MockPinNet:
    def __init__(self):
        self._pins = set()
        self.__update = self._update

    def verify_max_one_output_pin(self):
        output_pins = [pin for pin in self._pins if pin.mode() == pin.OUT]
        if len(output_pins) > 1:
            raise RuntimeError(f"Multiple connected output pins: {output_pins}")

    def _update(self):
        self.verify_max_one_output_pin()

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
        pin.observers.attach(self.__update)

    def detach_pin(self, pin):
        if pin not in self._pins:
            raise RuntimeError()
        self._pins.remove(pin)
        pin._net = None
        pin.observers.detach(self.__update)
