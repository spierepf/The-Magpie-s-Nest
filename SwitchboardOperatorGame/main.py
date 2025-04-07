# This is a sample Python script.
from node import Node


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def wled_names():
    yield 'intrados'
    yield 'time-and-space'
    yield 'fruit-platter'
    for i in range(5):
        for j in range(5):
            if ((i == 0 or i == 4) and (j < 3)) or (i == 1 or i == 3) or ((i == 2) and (j < 2)):
                yield f'portal-{i+1}-{j+1}'


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'http://wled-{name}.local')  # Press Ctrl+F8 to toggle the breakpoint.


def build_node(pin_id, node_name):
    pass


nodes = [
    build_node(0,  'portal-1-1'),
    build_node(1,  'portal-1-2'),
    build_node(2,  'portal-1-3'),

    build_node(3,  'portal-2-1'),
    build_node(4,  'portal-2-2'),
    build_node(5,  'portal-2-3'),
    build_node(6,  'portal-2-4'),
    build_node(7,  'portal-2-5'),

    build_node(8,  'portal-3-5'),
    build_node(9,  'portal-3-4'),
    build_node(10, 'portal-3-3'),
    build_node(11, 'portal-3-2'),
    build_node(12, 'portal-3-1'),

    build_node(13, 'portal-4-3'),
    build_node(14, 'portal-4-2'),
    build_node(15, 'portal-4-1'),
]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for name in wled_names():
        print_hi(name)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
