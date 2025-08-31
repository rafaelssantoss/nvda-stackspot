import addonHandler
from .gui import StackspotSettingsPanel

try:
    addonHandler.initTranslation()
except addonHandler.AddonError:
    pass

if StackspotSettingsPanel not in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)
