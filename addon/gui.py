import wx
import gui
import globalPluginHandler
import addonHandler
import addonConfig

addonHandler.initTranslation()


class StackspotSettingsPanel(gui.SettingsPanel):
    title = "Stackspot AI"

    def makeSettings(self, sizer):
        sHelper = self.makeSettingsHelper(sizer)

        self.clientIdCtrl = sHelper.addLabeledControl(
            "Client ID:", wx.TextCtrl,
            value=addonConfig.getPref("client_id")
        )
        self.clientSecretCtrl = sHelper.addLabeledControl(
            "Client Secret:", wx.TextCtrl,
            value=addonConfig.getPref("client_secret"),
            style=wx.TE_PASSWORD
        )
        self.realmCtrl = sHelper.addLabeledControl(
            "Realm:", wx.TextCtrl,
            value=addonConfig.getPref("realm")
        )
        self.slugCtrl = sHelper.addLabeledControl(
            "Slug do Quick Command:", wx.TextCtrl,
            value=addonConfig.getPref("slug")
        )

    def onSave(self):
        addonConfig.setPref("client_id", self.clientIdCtrl.GetValue())
        addonConfig.setPref("client_secret", self.clientSecretCtrl.GetValue())
        addonConfig.setPref("realm", self.realmCtrl.GetValue())
        addonConfig.setPref("slug", self.slugCtrl.GetValue())


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """
    Registra o painel StackspotSettingsPanel nas configurações do NVDA
    """

    def __init__(self):
        super().__init__()
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)

    def terminate(self):
        super().terminate()
        if StackspotSettingsPanel in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(StackspotSettingsPanel)
