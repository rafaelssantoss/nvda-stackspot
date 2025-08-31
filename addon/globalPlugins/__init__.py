import sys
import os

addon_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(addon_dir, '..', 'lib')
lib_dir = os.path.abspath(lib_dir)

if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)
