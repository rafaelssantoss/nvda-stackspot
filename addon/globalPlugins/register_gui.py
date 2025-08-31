from gui import StackspotSettingsPanel
import gui
import globalPluginHandler


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)

    def terminate(self):
        super().terminate()
        if StackspotSettingsPanel in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(StackspotSettingsPanel)
