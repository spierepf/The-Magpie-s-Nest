import unittest

from observable import Observable


class TestObservable(unittest.TestCase):
    class Observer:
        def __init__(self):
            self._observable = None
            self._arg = None


        def update(self, observable, arg):
            self._observable = observable
            self._arg = arg

    def test_observable_notifies_multiple_observers(self):
        observable = Observable()
        observers = [self.Observer() for _ in range(5)]
        for observer in observers:
            observable.attach_observer(observer)
        arg = object()
        observable.notify_observers(arg)
        for observer in observers:
            assert observer._observable == observable
            assert observer._arg == arg


    def test_observable_does_not_notify_removed_observer(self):
        observable = Observable()
        observers = [self.Observer() for _ in range(5)]
        for observer in observers:
            observable.attach_observer(observer)
        removed_observer = observers[2]
        observable.detach_observer(removed_observer)
        arg = object()
        observable.notify_observers(arg)
        assert removed_observer._observable is None
        assert removed_observer._arg is None

    def test_self_detaching_observers_do_not_affect_subsequent_observers(self):
        observable = Observable()
        class SelfDetachingObserver(self.Observer):
            def update(self, observable, arg):
                observable.detach_observer(self)
                super().update(observable, arg)
        observers = [SelfDetachingObserver() for _ in range(5)]
        for observer in observers:
            observable.attach_observer(observer)
        arg = object()
        observable.notify_observers(arg)
        for observer in observers:
            assert observer._observable == observable
            assert observer._arg == arg
        assert 0 == len(observable.observers)
