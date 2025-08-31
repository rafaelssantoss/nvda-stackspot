import sys
import os
import importlib.util
import globalPluginHandler

addon_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if addon_root not in sys.path:
    sys.path.insert(0, addon_root)

gui_path = os.path.join(addon_root, "stackspot_gui.py")
spec = importlib.util.spec_from_file_location("addon_gui", gui_path)
addon_gui = importlib.util.module_from_spec(spec)
spec.loader.exec_module(addon_gui)

StackspotSettingsPanel = addon_gui.StackspotSettingsPanel


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        import gui as nvda_gui
        if StackspotSettingsPanel not in nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
            nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)

    def terminate(self):
        super().terminate()
        import gui as nvda_gui
        if StackspotSettingsPanel in nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
            nvda_gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(StackspotSettingsPanel)
