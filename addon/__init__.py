import sys
import os

addonPath = os.path.dirname(__file__)
libPath = os.path.join(addonPath, '..', '..', 'lib')
sys.path.insert(0, libPath)