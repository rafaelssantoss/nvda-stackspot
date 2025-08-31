import wx
from gui.settingsDialogs import SettingsPanel
import addonConfig


class StackspotSettingsPanel(SettingsPanel):
    title = _("StackSpot AI")

    def makeSettings(self, sizer):
        sizer.Add(wx.StaticText(self, label=_("Client ID:")))
        self.clientIdCtrl = wx.TextCtrl(self, value=addonConfig.getPref("client_id") or "")
        sizer.Add(self.clientIdCtrl, flag=wx.EXPAND | wx.ALL, border=5)

        sizer.Add(wx.StaticText(self, label=_("Client Secret:")))
        self.clientSecretCtrl = wx.TextCtrl(self, value=addonConfig.getPref("client_secret") or "")
        sizer.Add(self.clientSecretCtrl, flag=wx.EXPAND | wx.ALL, border=5)

        sizer.Add(wx.StaticText(self, label=_("Realm:")))
        self.realmCtrl = wx.TextCtrl(self, value=addonConfig.getPref("realm") or "")
        sizer.Add(self.realmCtrl, flag=wx.EXPAND | wx.ALL, border=5)

        sizer.Add(wx.StaticText(self, label=_("Slug:")))
        self.slugCtrl = wx.TextCtrl(self, value=addonConfig.getPref("slug") or "")
        sizer.Add(self.slugCtrl, flag=wx.EXPAND | wx.ALL, border=5)

    def onSave(self):
        addonConfig.setPref("client_id", self.clientIdCtrl.GetValue())
        addonConfig.setPref("client_secret", self.clientSecretCtrl.GetValue())
        addonConfig.setPref("realm", self.realmCtrl.GetValue())
        addonConfig.setPref("slug", self.slugCtrl.GetValue())
