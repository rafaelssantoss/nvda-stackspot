import os
import sys
import ctypes
import ctypes.wintypes

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
    def get_mouse_position():
        """Retorna a posição atual do cursor do mouse (x, y)."""
        pt = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    @staticmethod
    def capture_region_around_mouse(size=300):
        """
        Captura uma região quadrada ao redor do mouse e retorna PNG binário.
        """
        x, y = ScreenCapture.get_mouse_position()
        half = size // 2
        left, top = x - half, y - half
        right, bottom = x + half, y + half

        img = ImageGrab.grab(bbox=(left, top, right, bottom))

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
