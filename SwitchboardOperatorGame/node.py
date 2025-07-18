class Node:
    def __init__(self, pin, show_colour=None, clear_colour=None):
        self._pin = pin
        self.show_colour = show_colour
        self.clear_colour = clear_colour

    def pin(self):
        return self._pin

    def is_connected_to(self, other_node):
        pin = self._pin
        other_pin = other_node._pin
        pin.init(mode=pin.IN, pull=pin.PULL_UP)
        try:
            for _ in range(5):
                other_pin.init(mode=other_pin.OUT, value=False)
                if pin.value():
                    return False
                other_pin.init(mode=other_pin.OUT, value=True)
                if not pin():
                    return False
            return True
        finally:
            pin.init(mode=pin.IN, pull=None)
            other_pin.init(mode=other_pin.IN, pull=None)

    def __repr__(self):
        return f"<Node: {self._pin}>"
