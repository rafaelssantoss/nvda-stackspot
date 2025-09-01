import os
import sys
import ctypes
import tempfile
import api
import globalPluginHandler
import speech
import logHandler

addon_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(addon_dir, '..', 'lib')
addon_root = os.path.abspath(os.path.join(addon_dir, '..'))

for path in (lib_dir, addon_root):
    if path not in sys.path:
        sys.path.insert(0, path)

from stackspot.stackspot import Stackspot
import addonConfig

from PIL import Image

client_id = addonConfig.getPref("client_id")
client_secret = addonConfig.getPref("client_secret")
realm = addonConfig.getPref("realm")
slug = addonConfig.getPref("slug")


def capture_screen(rect):
    x, y, w, h = rect
    width = w
    height = h

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    hdesktop = user32.GetDesktopWindow()
    desktop_dc = user32.GetWindowDC(hdesktop)
    img_dc = gdi32.CreateCompatibleDC(desktop_dc)
    bmp = gdi32.CreateCompatibleBitmap(desktop_dc, width, height)
    gdi32.SelectObject(img_dc, bmp)

    SRCCOPY = 0x00CC0020
    gdi32.BitBlt(img_dc, 0, 0, width, height, desktop_dc, x, y, SRCCOPY)

    class BITMAP(ctypes.Structure):
        _fields_ = [("bmType", ctypes.c_int),
                    ("bmWidth", ctypes.c_int),
                    ("bmHeight", ctypes.c_int),
                    ("bmWidthBytes", ctypes.c_int),
                    ("bmPlanes", ctypes.c_ushort),
                    ("bmBitsPixel", ctypes.c_ushort),
                    ("bmBits", ctypes.c_void_p)]

    bmp_struct = BITMAP()
    gdi32.GetObjectW(bmp, ctypes.sizeof(bmp_struct), ctypes.byref(bmp_struct))

    # Calcular tamanho do buffer
    if bmp_struct.bmBitsPixel == 32:
        # 32 bits por pixel (ARGB)
        buffer_size = bmp_struct.bmHeight * bmp_struct.bmWidth * 4
    else:
        # 24 bits por pixel (RGB)
        buffer_size = bmp_struct.bmHeight * bmp_struct.bmWidth * 3

    buffer = ctypes.create_string_buffer(buffer_size)
    gdi32.GetBitmapBits(bmp, buffer_size, buffer)

    # Criar imagem PIL a partir do buffer
    if bmp_struct.bmBitsPixel == 32:
        # Converter ARGB para RGB
        image = Image.frombuffer(
            'RGBA',
            (width, height),
            buffer,
            'raw',
            'BGRA',  # Windows usa BGR
            0, 1
        )
        image = image.convert('RGB')
    else:
        # RGB direto
        image = Image.frombuffer(
            'RGB',
            (width, height),
            buffer,
            'raw',
            'BGR',  # Windows usa BGR
            0, 1
        )

    tmp_file = os.path.join(tempfile.gettempdir(), "focused_image.png")
    image.save(tmp_file, format='PNG', optimize=True)

    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(img_dc)
    user32.ReleaseDC(hdesktop, desktop_dc)

    return tmp_file


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def script_descreverImagem(self, gesture):
        try:
            obj = api.getFocusObject()
            rect = obj.location if obj and obj.location else None

            if not rect:
                x, y = api.getMousePosition()
                rect = (x - 100, y - 100, 200, 200)
                speech.speakText("Não foi detectado objeto acessível, capturando área do cursor.")

            tmp_file = capture_screen(rect)

            stackspot = Stackspot.instance().credential(
                client_id=client_id,
                client_secret=client_secret,
                realm=realm
            )
            result = stackspot.send_file_stackspot(tmp_file, "CONTEXT", "").transcription(slug)

            speech.speakText(result)

        except Exception as e:
            logHandler.log.error(f'Error: {e}')
            speech.speakText(f"Erro ao processar imagem: {str(e)}")

    __gestures = {
        "kb:NVDA+i": "descreverImagem"
    }