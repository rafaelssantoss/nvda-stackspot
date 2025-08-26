import api, globalPluginHandler, ui, speech, screenBitmap
from .stackspot import Stackspot

""" Um exemplo de execução de integração com stackspot com entrada de estimulo NVDA"""

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	stackspot = Stackspot()
	def script_runStackSpot(self, gesture):
		obj = api.getNavigatorObject()
		location = obj.location
		sb = screenBitmap.ScreenBitmap(location.width, location.height)

		pixels = sb.captureImage(
			location.left,
			location.top,
			location.width,
			location.height
		)

		response = self.stackspot.describe_image(pixels)
		ui.message(response)

	__gestures = {
		"kb:NVDA+alt+S": "runStackSpot"
	}
