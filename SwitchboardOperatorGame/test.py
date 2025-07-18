import os

import install
import logging

logging.basicConfig(level=logging.ERROR)

if 'unittest' not in os.listdir(install.libpath):
    import mip

    mip.install('unittest', target=install.libpath)

if 'mock.py' not in os.listdir(install.libpath + "/unittest"):
    import mip

    mip.install('github:spierepf/umock', target=install.libpath)

if 'umockpin' not in os.listdir(install.libpath):
    import mip

    mip.install('github:spierepf/umockpin', target=install.libpath)

import unittest
# noinspection PyUnresolvedReferences
from tests.test_node import TestNode
# noinspection PyUnresolvedReferences
from tests.test_node_pair import NodePairTestCase
# noinspection PyUnresolvedReferences
from tests.test_game_controller import GameControllerTestCase

if __name__ == "__main__":
    unittest.main()
