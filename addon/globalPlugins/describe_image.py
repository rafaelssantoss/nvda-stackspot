import ctypes
import os
import struct
import tempfile
from ctypes import wintypes
import api
import globalPluginHandler
import speech

from stackspot import Stackspot
from . import addonConfig

client_id = addonConfig.getPref("client_id")
client_secret = addonConfig.getPref("client_secret")
realm = addonConfig.getPref("realm")
slug = addonConfig.getPref("slug")


def capture_screen(rect):
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    x, y, w, h = rect
    width = w
    height = h

    hdesktop = user32.GetDesktopWindow()
    desktop_dc = user32.GetWindowDC(hdesktop)
    img_dc = gdi32.CreateCompatibleDC(desktop_dc)
    bmp = gdi32.CreateCompatibleBitmap(desktop_dc, width, height)
    gdi32.SelectObject(img_dc, bmp)

    SRCCOPY = 0x00CC0020
    gdi32.BitBlt(img_dc, 0, 0, width, height, desktop_dc, x, y, SRCCOPY)

    class BITMAPFILEHEADER(ctypes.Structure):
        _fields_ = [("bfType", wintypes.WORD),
                    ("bfSize", wintypes.DWORD),
                    ("bfReserved1", wintypes.WORD),
                    ("bfReserved2", wintypes.WORD),
                    ("bfOffBits", wintypes.DWORD)]

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [("biSize", wintypes.DWORD),
                    ("biWidth", wintypes.LONG),
                    ("biHeight", wintypes.LONG),
                    ("biPlanes", wintypes.WORD),
                    ("biBitCount", wintypes.WORD),
                    ("biCompression", wintypes.DWORD),
                    ("biSizeImage", wintypes.DWORD),
                    ("biXPelsPerMeter", wintypes.LONG),
                    ("biYPelsPerMeter", wintypes.LONG),
                    ("biClrUsed", wintypes.DWORD),
                    ("biClrImportant", wintypes.DWORD)]

    class BITMAP(ctypes.Structure):
        _fields_ = [("bmType", wintypes.LONG),
                    ("bmWidth", wintypes.LONG),
                    ("bmHeight", wintypes.LONG),
                    ("bmWidthBytes", wintypes.LONG),
                    ("bmPlanes", wintypes.WORD),
                    ("bmBitsPixel", wintypes.WORD),
                    ("bmBits", ctypes.c_void_p)]

    bmp_struct = BITMAP()
    gdi32.GetObjectW(bmp, ctypes.sizeof(bmp_struct), ctypes.byref(bmp_struct))

    total_bytes = bmp_struct.bmHeight * bmp_struct.bmWidthBytes
    buffer = ctypes.create_string_buffer(total_bytes)
    gdi32.GetBitmapBits(bmp, total_bytes, buffer)

    tmp_file = os.path.join(tempfile.gettempdir(), "focused_image.bmp")
    with open(tmp_file, "wb") as f:
        f.write(b'BM')
        f.write(struct.pack('<IHHI', 14 + 40 + total_bytes, 0, 0, 14 + 40))
        f.write(struct.pack('<IIIHHIIIIII',
                            40, width, height, 1, 24, 0,
                            total_bytes, 0, 0, 0, 0))
        f.write(buffer)

    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(img_dc)
    user32.ReleaseDC(hdesktop, desktop_dc)

    return tmp_file


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def script_descreverImagem(self, gesture):
        try:
            obj = api.getFocusObject()
            if obj.role != "graphic":
                speech.speakText("O foco atual não é uma imagem.")
                return

            rect = obj.location
            if not rect:
                speech.speakText("Não consegui obter a posição da imagem.")
                return

            tmp_file = capture_screen(rect)

            stackspot = Stackspot.instance().credential(
                client_id=client_id,
                client_secret=client_secret,
                realm=realm
            )
            result = stackspot.file(tmp_file, "CONTEXT", "").transcription(slug)

            speech.speakText(result)

        except Exception as e:
            speech.speakText(f"Erro: {e}")

    __gestures = {
        "kb:NVDA+i": "descreverImagem"
    }
