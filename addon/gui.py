import wx
import gui
import gui.settingsDialogs as settings
from . import addonConfig


class StackspotSettingsPanel(settings.SettingsPanel):
    title = "StackSpot AI"

    def makeSettings(self, sizer):
        self.clientIdCtrl = wx.TextCtrl(self, value=addonConfig.getPref("client_id"))
        sizer.Add(wx.StaticText(self, label=_("Client ID:")))
        sizer.Add(self.clientIdCtrl, flag=wx.EXPAND)

        self.clientSecretCtrl = wx.TextCtrl(self, value=addonConfig.getPref("client_secret"), style=wx.TE_PASSWORD)
        sizer.Add(wx.StaticText(self, label=_("Client Secret:")))
        sizer.Add(self.clientSecretCtrl, flag=wx.EXPAND)

        self.realmCtrl = wx.TextCtrl(self, value=addonConfig.getPref("realm"))
        sizer.Add(wx.StaticText(self, label=_("Realm:")))
        sizer.Add(self.realmCtrl, flag=wx.EXPAND)

        self.slugCtrl = wx.TextCtrl(self, value=addonConfig.getPref("slug"))
        sizer.Add(wx.StaticText(self, label=_("Slug do Quick Command:")))
        sizer.Add(self.slugCtrl, flag=wx.EXPAND)

    def onSave(self):
        addonConfig.setPref("client_id", self.clientIdCtrl.GetValue())
        addonConfig.setPref("client_secret", self.clientSecretCtrl.GetValue())
        addonConfig.setPref("realm", self.realmCtrl.GetValue())
        addonConfig.setPref("slug", self.slugCtrl.GetValue())


def onSettingsDialog():
    if StackspotSettingsPanel not in gui.settingsDialogs.NVDASettingsDialog.categoryClasses:
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(StackspotSettingsPanel)


onSettingsDialog()
