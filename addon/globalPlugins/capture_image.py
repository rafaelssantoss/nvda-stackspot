import os
import sys

addon_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(addon_dir, '..', 'lib')
addon_root = os.path.abspath(os.path.join(addon_dir, '..'))
for path in (lib_dir, addon_root):
    if path not in sys.path:
        sys.path.insert(0, path)

import ctypes
import ctypes.wintypes
from PIL import Image
import io


class ScreenCapture:
    @staticmethod
    def get_mouse_position():
        """Obtém a posição do cursor do mouse (x, y)."""
        pt = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    @staticmethod
    def capture_region_around_mouse(size=300):
        """
        Captura uma região quadrada em torno do mouse e retorna os bytes PNG.
        size = largura/altura em pixels (ex: 300 → 300x300).
        """
        x, y = ScreenCapture.get_mouse_position()
        half = size // 2
        left, top = x - half, y - half
        width, height = size, size

        hdc_screen = ctypes.windll.user32.GetDC(0)
        hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_screen)
        hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_screen, width, height)
        ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)

        SRCCOPY = 0x00CC0020
        ctypes.windll.gdi32.BitBlt(
            hdc_mem, 0, 0, width, height,
            hdc_screen, left, top, SRCCOPY
        )

        bmp_header = ctypes.wintypes.BITMAPFILEHEADER()
        bmp_info = ctypes.wintypes.BITMAPINFOHEADER()
        bmp_info.biSize = ctypes.sizeof(ctypes.wintypes.BITMAPINFOHEADER)
        bmp_info.biWidth = width
        bmp_info.biHeight = -height
        bmp_info.biPlanes = 1
        bmp_info.biBitCount = 24
        bmp_info.biCompression = 0
        bmp_info.biSizeImage = ((width * 3 + 3) & -4) * height

        buf = ctypes.create_string_buffer(bmp_info.biSizeImage)
        ctypes.windll.gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, buf, ctypes.byref(bmp_info), 0)

        ctypes.windll.gdi32.DeleteObject(hbitmap)
        ctypes.windll.gdi32.DeleteDC(hdc_mem)
        ctypes.windll.user32.ReleaseDC(0, hdc_screen)

        try:
            img = Image.frombuffer("RGB", (width, height), buf, "raw", "BGR", 0, 1)
            output = io.BytesIO()
            img.save(output, format="PNG")
            return output.getvalue()
        except ImportError:
            return buf.raw
