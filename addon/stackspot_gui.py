import wx
from gui.settingsDialogs import SettingsPanel
import addonConfig


class StackspotSettingsPanel(SettingsPanel):
    title = _("StackSpot AI")

    def makeSettings(self, sizer):
        sHelper = self.makeSettingsHelper(sizer)

        self.clientIdCtrl = sHelper.addLabeledControl(
            _("Client ID:"), wx.TextCtrl,
            value=addonConfig.getPref("client_id")
        )
        self.clientSecretCtrl = sHelper.addLabeledControl(
            _("Client Secret:"), wx.TextCtrl,
            value=addonConfig.getPref("client_secret")
        )
        self.targetIdCtrl = sHelper.addLabeledControl(
            _("Target ID:"), wx.TextCtrl,
            value=addonConfig.getPref("target_id")
        )

    def onSave(self):
        addonConfig.setPref("client_id", self.clientIdCtrl.GetValue())
        addonConfig.setPref("client_secret", self.clientSecretCtrl.GetValue())
        addonConfig.setPref("target_id", self.targetIdCtrl.GetValue())
