import sys
import os
import globalPluginHandler

addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

from gui import StackspotSettingsPanel


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        # Registra o painel de configurações na NVDA
        import gui as nvda_gui  # módulo gui interno do NVDA
        nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)

    def terminate(self):
        super().terminate()
        import gui as nvda_gui
        # Remove o painel ao desativar o addon
        if StackspotSettingsPanel in nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
            nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(StackspotSettingsPanel)
