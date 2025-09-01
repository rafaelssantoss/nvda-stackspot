import os
import sys
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
from .capture_image import ScreenCapture

client_id = addonConfig.getPref("client_id")
client_secret = addonConfig.getPref("client_secret")
realm = addonConfig.getPref("realm")
slug = addonConfig.getPref("slug")


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    def script_runStackSpot(self, gesture):
        speech.speakText("Processando imagem")

        binary_png = ScreenCapture.capture_region_around_mouse(300)
        stackspot = Stackspot.instance().credential(
            client_id=client_id,
            client_secret=client_secret,
            realm=realm
        )

        result = stackspot.send_file_stackspot(binary_png, "CONTEXT", "").transcription(slug)
        speech.speakText(result)

    __gestures = {
        "kb:NVDA+i": "descreverImagem"
    }