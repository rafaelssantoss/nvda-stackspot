import os
import sys
sys.path.insert(0, os.path.split(os.path.split(__file__)[0])[0] + "\\lib")

import api, globalPluginHandler, ui, speech, tempfile
from .stackspot import Stackspot
from PIL import ImageGrab

""" Um exemplo de execução de integração com stackspot com entrada de estimulo NVDA"""

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	stackspot = Stackspot()
	def script_runStackSpot(self, gesture):
		obj = api.getNavigatorObject()
		location = obj.location
		bounding_box = (location.left, location.top, location.left + location.width, location.top + location.height)
		snap = ImageGrab.grab(bounding_box)
		file = tempfile.mktemp(suffix=".png")
		snap.save(file)

		try:
			response = self.stackspot.describe_image(file)
			log.info(response)
			ui.message(response)
		finally:
			os.remove(file)

	__gestures = {
		"kb:NVDA+alt+S": "runStackSpot"
	}
