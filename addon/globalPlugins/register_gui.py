from ..gui import StackspotSettingsPanel
import gui as nvda_gui
import globalPluginHandler


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)

    def terminate(self):
        super().terminate()
        if StackspotSettingsPanel in nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
            nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(StackspotSettingsPanel)
