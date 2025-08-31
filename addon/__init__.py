from .gui import StackspotSettingsPanel
import gui.settingsDialogs

if StackspotSettingsPanel not in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)
