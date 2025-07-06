import os
import sys

libpath = 'lib'
sys.path.insert(0, libpath)
if libpath not in os.listdir():
    os.mkdir(libpath)

if 'ulogging.py' not in os.listdir(libpath):
    import mip

    mip.install('github:pfalcon/pycopy-lib/ulogging/ulogging.py', target=libpath)

if 'uwledclient.py' not in os.listdir(libpath):
    import mip

    mip.install('github:spierepf/uwledclient', target=libpath)

if 'mcp23s08.py' not in os.listdir(libpath):
    import mip

    mip.install('github:spierepf/mcp23s08', target=libpath)

if 'upatterns' not in os.listdir(libpath):
    import mip

    mip.install('github:spierepf/mip_packages/upatterns', target=libpath)
