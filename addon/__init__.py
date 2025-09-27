import addonHandler
from .stackspot_gui import StackspotSettingsPanel

try:
    addonHandler.initTranslation()
except addonHandler.AddonError:
    pass

if StackspotSettingsPanel not in stackspot_gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
    stackspot_gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)
