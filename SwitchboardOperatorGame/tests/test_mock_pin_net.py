import unittest

from tests.mock_pin import MockPin
from tests.mock_pin_factory import MockPinFactory
from tests.mock_pin_net import MockPinNet


class TestMockPinNet(unittest.TestCase):
    def test_net_with_no_pins_has_no_value(self):
        assert MockPinNet().value() is None


class TestMockPinNetWithOnePin(unittest.TestCase):
    def setUp(self):
        self.mpf = MockPinFactory()
        self.net = MockPinNet()
        self.pin = self.mpf.Pin(0)
        self.net.attach_pin(self.pin)

    def test_pin_may_not_be_detached_from_net_it_is_not_attached_to(self):
        self.assertRaises(RuntimeError, lambda: MockPinNet().detach_pin(self.mpf.Pin(0)))

    def test_pin_may_be_detached_from_net_it_is_attached_to(self):
        self.net.detach_pin(self.pin)

    def test_detached_pin_may_be_reattached_to_net_it_was_detached_from(self):
        self.net.detach_pin(self.pin)
        self.net.attach_pin(self.pin)

    def test_detached_pin_may_be_attached_to_new_net(self):
        self.net.detach_pin(self.pin)
        MockPinNet().attach_pin(self.pin)

    def test_detaching_net_from_pin_manually_fails(self):
        self.assertRaises(KeyError, lambda: self.pin.detach_observer(self.net))

    def test_net_with_single_output_pin_takes_its_value_from_that_pin(self):
        self.pin.init(mode=MockPin.OUT)
        self.pin.high()
        assert self.net.value() == True
        self.pin.low()
        assert self.net.value() == False

    def test_net_with_single_input_pin_with_pull_up_has_value_true(self):
        self.pin.init(mode=MockPin.IN, pull=MockPin.PULL_UP)
        assert self.net.value() == True

    def test_net_with_single_input_pin_without_pull_up_has_no_value(self):
        self.pin.init(mode=MockPin.IN, pull=None)
        assert self.net.value() is None

    def test_attaching_second_output_pin_raises_exception(self):
        self.pin.init(mode=MockPin.OUT)
        self.assertRaises(RuntimeError, lambda: self.net.attach_pin(self.mpf.Pin(1, mode=MockPin.OUT)))

    def test_pin_may_not_be_attached_to_two_nets_at_the_same_time(self):
        self.assertRaises(RuntimeError, lambda: MockPinNet().attach_pin(self.pin))

    def test_pin_may_be_attached_to_a_new_net_after_being_removed_from_an_old_net(self):
        self.net.detach_pin(self.pin)
        MockPinNet().attach_pin(self.pin)

    def test_detaching_pin_removes_observer(self):
        self.net.detach_pin(self.pin)
        assert len(self.pin.observers) == 0


class TestMockPinNetWithTwoPins(unittest.TestCase):
    def setUp(self):
        self.mpf = MockPinFactory()
        self.net = MockPinNet()
        self.pin0 = self.mpf.Pin(0)
        self.net.attach_pin(self.pin0)
        self.pin1 = self.mpf.Pin(1)
        self.net.attach_pin(self.pin1)

    def test_net_with_input_pins_without_pull_up_has_no_value(self):
        self.pin0.init(mode=MockPin.IN, pull=None)
        self.pin0.init(mode=MockPin.IN, pull=None)
        for i in [self.net, self.pin0, self.pin1]:
            assert i.value() is None

    def test_net_with_an_input_pin_with_pull_up_has_value_true(self):
        self.pin0.init(mode=MockPin.IN, pull=MockPin.PULL_UP)
        self.pin1.init(mode=MockPin.IN, pull=None)
        for i in [self.net, self.pin0, self.pin1]:
            assert i.value() == True

    def test_net_with_an_output_pin_and_an_input_pin_takes_its_value_from_the_output_pin(self):
        self.pin0.init(mode=MockPin.OUT)
        self.pin1.init(mode=MockPin.IN, pull=None)
        self.pin0.high()
        for i in [self.net, self.pin0, self.pin1]:
            assert i.value() == True
        self.pin0.low()
        for i in [self.net, self.pin0, self.pin1]:
            assert i.value() == False

    def test_net_with_an_output_pin_and_an_input_pin_with_pull_up_takes_its_value_from_the_output_pin(self):
        self.pin0.init(mode=MockPin.OUT)
        self.pin1.init(mode=MockPin.IN, pull=MockPin.PULL_UP)
        self.pin0.high()
        for i in [self.net, self.pin0, self.pin1]:
            assert i.value() == True
        self.pin0.low()
        for i in [self.net, self.pin0, self.pin1]:
            assert i.value() == False

    def test_setting_second_pin_to_output_raises_exception(self):
        self.pin0.init(mode=MockPin.OUT)
        self.pin1.init(mode=MockPin.IN)
        self.assertRaises(RuntimeError, lambda: self.pin1.mode(MockPin.OUT))

    def test_detaching_output_pin_removes_its_influence_on_net(self):
        self.pin0.init(mode=MockPin.OUT, value=False)
        self.pin1.init(mode=MockPin.IN, pull=MockPin.PULL_UP)
        self.net.detach_pin(self.pin0)
        for i in [self.net, self.pin1]:
            assert i.value() == True
