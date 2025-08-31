import os
import sys
import tempfile
import api
import globalPluginHandler
import speech
import logHandler
import win32gui
import win32ui
import win32con

addon_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(addon_dir, '..', 'lib')
addon_root = os.path.abspath(os.path.join(addon_dir, '..'))

for path in (lib_dir, addon_root):
    if path not in sys.path:
        sys.path.insert(0, path)

from stackspot.stackspot import Stackspot
import addonConfig

client_id = addonConfig.getPref("client_id")
client_secret = addonConfig.getPref("client_secret")
realm = addonConfig.getPref("realm")
slug = addonConfig.getPref("slug")


def capture_screen(rect):
    x, y, w, h = rect

    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, w, h)
    mem_dc.SelectObject(screenshot)

    mem_dc.BitBlt((0, 0), (w, h), img_dc, (x, y), win32con.SRCCOPY)

    tmp_file = os.path.join(tempfile.gettempdir(), "focused_image.png")
    screenshot.SaveBitmapFile(mem_dc, tmp_file)

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
    img_dc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, desktop_dc)

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