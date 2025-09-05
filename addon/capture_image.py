import api
import os
import sys
import ctypes
import ui

addon_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(addon_dir, '', 'lib')
addon_root = os.path.abspath(os.path.join(addon_dir, ''))
for path in (lib_dir, addon_root):
    if path not in sys.path:
        sys.path.insert(0, path)

from PIL import ImageGrab
import io


class ScreenCapture:
    @staticmethod
    def capture_region_around_navigation():
        """
        Captura uma região do objeto de navegação e retorna PNG binário.
        """
        nav = api.getNavigationObject()
        try:
            left, top, width, height = nav.location
        except TypeError:
            ui.message("Objeto não está visível")
            return None

        img = ImageGrab.grab(bbox=(left, top, left + width, top + height))

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
