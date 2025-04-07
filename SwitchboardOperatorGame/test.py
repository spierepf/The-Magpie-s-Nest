import os

import install

if 'unittest' not in os.listdir(install.libpath):
    import mip

    mip.install('unittest', target=install.libpath)

import unittest
# noinspection PyUnresolvedReferences
from tests.test_mock_pin import TestMockPin
# noinspection PyUnresolvedReferences
from tests.test_mock_pin_factory import TestMockPinFactory
# noinspection PyUnresolvedReferences
from tests.test_mock_pin_net import TestMockPinNet, TestMockPinNetWithOnePin, TestMockPinNetWithTwoPins
# noinspection PyUnresolvedReferences
from tests.test_observable import TestObservable
# noinspection PyUnresolvedReferences
from tests.test_node import TestNode

if __name__ == "__main__":
    unittest.main()
