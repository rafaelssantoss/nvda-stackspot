import wx
import gui.settingsDialogs as settings
import addonHandler
from . import addonConfig

addonHandler.initTranslation()


class StackspotSettingsPanel(settings.SettingsPanel):
    # Título exibido na aba de configurações
    title = "Stackspot AI"

    def makeSettings(self, sizer):
        sHelper = self.makeSettingsHelper(sizer)

        self.clientIdCtrl = sHelper.addLabeledControl(
            "Client ID:",
            wx.TextCtrl,
            value=addonConfig.getPref("client_id")
        )
        self.clientSecretCtrl = sHelper.addLabeledControl(
            "Client Secret:",
            wx.TextCtrl,
            value=addonConfig.getPref("client_secret"),
            style=wx.TE_PASSWORD
        )
        self.realmCtrl = sHelper.addLabeledControl(
            "Realm:",
            wx.TextCtrl,
            value=addonConfig.getPref("realm")
        )
        self.slugCtrl = sHelper.addLabeledControl(
            "Slug do Quick Command:",
            wx.TextCtrl,
            value=addonConfig.getPref("slug")
        )

    def onSave(self):
        addonConfig.setPref("client_id", self.clientIdCtrl.GetValue())
        addonConfig.setPref("client_secret", self.clientSecretCtrl.GetValue())
        addonConfig.setPref("realm", self.realmCtrl.GetValue())
        addonConfig.setPref("slug", self.slugCtrl.GetValue())


import gui.settingsDialogs

if StackspotSettingsPanel not in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)
