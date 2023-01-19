import os
import platform
import xml.etree.cElementTree as ET
import wx
import wx.adv
from . import callbacks, setwallpaper

class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        kw["style"] = kw.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kw)
        
        self.statusbar = self.CreateStatusBar()
        self.SetStatusText(_("No open file."))

        self.SetTitle(_("WallChange"))
        self.SetSize(700, 600)

        self.BuildUI()
        self.AddMenu()

    def AddMenu(self):
        menu = wx.MenuBar()
        cmds = {}

        # File
        filemenu = wx.Menu()
        cmds["open"] = filemenu.Append(wx.ID_OPEN)
        cmds["close"] = filemenu.Append(wx.ID_CLOSE)
        cmds["save"] = filemenu.Append(wx.ID_SAVE)
        cmds["exit"] = filemenu.Append(wx.ID_EXIT)
        menu.Append(filemenu, _("&File"))

        # Help
        helpmenu = wx.Menu()
        cmds["about"] = helpmenu.Append(wx.ID_ABOUT)
        menu.Append(helpmenu, _("&Help"))

        # Menu commands
        allcmds = {
            cmds["open"]: lambda evt: self.OpenFile(),
            cmds["close"]: lambda evt: self.CloseFile(),
            cmds["save"]: lambda evt: self.Save(),
            cmds["about"]: lambda evt: self.About(),
        }

        for item in allcmds:
            self.Bind(wx.EVT_MENU, allcmds[item], item)

        self.SetMenuBar(menu)

    def BuildUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Light background
        label1 = wx.StaticText(panel, -1, _("Light background"))
        sizer.Add(label1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        button_1 = wx.Button(panel, -1, _("Select a image"))
        button_1.Bind(wx.EVT_BUTTON, lambda evt: callbacks.OpenImg(self, button_1))
        sizer.Add(button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Dark background
        label2 = wx.StaticText(panel, -1, _("Dark background"))
        sizer.Add(label2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        button_2 = wx.Button(panel, -1, _("Select a image"))
        button_2.Bind(wx.EVT_BUTTON, lambda evt: callbacks.OpenImg(self, button_2))
        sizer.Add(button_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Save button
        button_3 = wx.Button(panel, -1, _("Save"))
        button_3.Bind(wx.EVT_BUTTON, lambda evt: self.Save())
        sizer.Add(button_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.buttons = [button_1, button_2]

        panel.SetSizer(sizer)
        self.Layout()
        self.Refresh()

    def About(self):
        wxver = wx.__version__
        pyver = platform.python_version()
        ostype = platform.system() if platform.system() != "" else _("Unknown")
        msg = _(
            f"""\
    Dynamically changes your desktop theme!
    wxPython version: {wxver}
    Python version: {pyver}
    OS type: {ostype}
        """
        )
        aboutinf = wx.adv.AboutDialogInfo()
        aboutinf.SetName("WallChange")
        aboutinf.SetDescription(msg)
        aboutinf.SetCopyright("(C) 2023 Le Bao Nguyen")
        aboutinf.AddDeveloper("Le Bao Nguyen")
        return wx.adv.AboutBox(aboutinf)

    def OpenFile(self):
        filepath = callbacks.OpenXML(self)
        if filepath is False:
            return
        else:
            try:
                childs, tree = callbacks.ReadXML(filepath)
            except callbacks.XMLParseError:
                return
        lightbg = childs["light"]
        darkbg = childs["dark"]
        self.buttons[0].SetLabel(lightbg)
        self.buttons[1].SetLabel(darkbg)
        self.filepath = filepath
        self.tree = tree
        self.SetTitle(_("WallChange - {}".format(filepath)))
        self.SetStatusText(filepath)
        self.Refresh()

    def CloseFile(self):
        for item in self.buttons:
            item.SetLabel(_("Choose"))

    def Save(self):
        def showdialog():
            return wx.MessageDialog(
                self,
                _("Please select all required images before you continue."),
                _("Missing component(s)"),
                style=wx.OK | wx.ICON_ERROR,
            ).ShowModal()

        for item in self.buttons:
            if not os.path.isfile(item.GetLabel()):
                return showdialog()

        if hasattr(self, "filepath"):
            for item in self.tree:
                if item.tag == "dark":
                    item.text = self.buttons[1].GetLabel()
                elif item.tag == "light":
                    item.text = self.buttons[0].GetLabel()

            with open(self.filepath, "wb") as f:
                ET.ElementTree(self.tree).write(f, "utf-8")
        else:
            callbacks.WriteNewFile(
                self, self.buttons[0].GetLabel(), self.buttons[1].GetLabel()
            )

        dlg = wx.MessageDialog(
            self, _("Start the wallpaper-set process now?"), _("Infomation"), style=wx.YES_NO
        )
        if dlg.ShowModal() == wx.ID_YES:
            self.thread = setwallpaper.AutoSet(self.filepath)


class App(wx.App):
    def OnInit(self):
        self.frame = MainWindow(None)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
