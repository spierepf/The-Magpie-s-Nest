# Getting Started

1. install [pyenv](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
1. `pyenv install micropython`
1. `cd SwitchboardOperatorGame/`
1. type `python` and verify MicroPython v1.x is displayed
1. execute `python test.py` to install dependencies and verify working env

# Terminology

Net - Any connected pins, used in mock testing
Node - Representation of input on foot ball and port hole
Node Pair - A pair of portholes the game wants connected
Pair Connect - When Node pair is connected, a small visual reward for user is displayed
Pair Disconnect - When a Node pair is disconnected, nothing or negative visual is displayed
Winning - All three (or n) node pairs are connected, a grand reward is displayed to user
