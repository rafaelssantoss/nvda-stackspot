import globalPluginHandler
import speech
import api
import os
import tempfile
from PIL import ImageGrab
from stackspot import Stackspot
from . import addonConfig

client_id = addonConfig.getPref("client_id")
client_secret = addonConfig.getPref("client_secret")
realm = addonConfig.getPref("realm")
slug = addonConfig.getPref("slug")


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

            x, y, w, h = rect
            bbox = (x, y, x + w, y + h)

            tmp_file = os.path.join(tempfile.gettempdir(), "focused_image.png")
            img = ImageGrab.grab(bbox=bbox)
            img.save(tmp_file, "PNG")

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

with open('81292.jpg', 'rb') as file:
    result = Stackspot.instance().credential('client_id',
                                             'client_secret',
                                             'realm').file(file, 'CONTEXT', '').transcription('quick-commando-slug')

    print(result)