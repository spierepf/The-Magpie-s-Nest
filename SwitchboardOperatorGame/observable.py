class Observable:
    def __init__(self):
        self.observers = set()

    def attach_observer(self, observer):
        self.observers.add(observer)

    def detach_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, arg=None):
        for observer in list(self.observers):
            observer.update(self, arg)
