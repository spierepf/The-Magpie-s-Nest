from observable import Observable


class MockPin(Observable):
    IN = 0
    OUT = 1

    PULL_UP = 1

    def __init__(self, id):
        super().__init__()
        self._id = id
        self._net = None
        self._mode = self.IN
        self._pull = None
        self._value = False

    def init(self, mode=-1, pull=-1, value=None):
        self.mode(mode)
        self.pull(pull)
        self.value(value)

    def value(self, x=None):
        if x is not None:
            if self._value != bool(x):
                self._value = bool(x)
                self.notify_observers()
        elif self._mode == self.OUT or self._net is None:
            return self._value
        else:
            return self._net.value()

    def __call__(self, x=None):
        return self.value(x)

    def on(self):
        self.value(True)

    def off(self):
        self.value(False)

    def low(self):
        self.value(False)

    def high(self):
        self.value(True)

    def mode(self, x=-1):
        if x in [self.IN, self.OUT]:
            if self._mode != x:
                self._mode = x
                self.notify_observers()
        else:
            return self._mode

    def pull(self, x=-1):
        if x in [None, self.PULL_UP]:
            if self._pull != x:
                self._pull = x
                self.notify_observers()
        else:
            return self._pull

    def toggle(self):
        self.value(not self.value())

    def __str__(self):
        return f"Pin({self._id}, {'IN' if self._mode == self.IN else 'OUT'})"