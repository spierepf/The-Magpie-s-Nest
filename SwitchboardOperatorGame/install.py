import os
import sys

libpath = 'lib'
sys.path.insert(0, libpath)
if libpath not in os.listdir():
    os.mkdir(libpath)

if 'logging.mpy' not in os.listdir(libpath):
    import mip

    mip.install('logging', target=libpath)

if 'uwledclient.py' not in os.listdir(libpath):
    import mip

    mip.install('github:spierepf/uwledclient', target=libpath)

if 'mcp23s08.py' not in os.listdir(libpath):
    import mip

    mip.install('github:spierepf/mcp23s08', target=libpath)

if 'itertools.mpy' not in os.listdir(libpath):
    import mip

    mip.install('itertools', target=libpath)
