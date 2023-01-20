import os
import platform
import xml.etree.cElementTree as ET
import wx
import wx.adv
from . import callbacks, setwallpaper

TRAY_TOOLTIP = "WallChange"
TRAY_ICON = "C:\\Users\\Dell\\Pictures\\vanilla-night.png"


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super(wx.adv.TaskBarIcon, self).__init__()
        self.frame = frame
        self.SetIcon(wx.Icon(wx.Bitmap(TRAY_ICON, wx.BITMAP_TYPE_ANY)), TRAY_TOOLTIP)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, lambda evt: self.frame.Show())

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(
            menu,
            _("Toggle the auto-wallpaper service"),
            lambda evt: self.frame.ToggleMode(),
        )
        menu.AppendSeparator()
        create_menu_item(menu, _("About this app"), lambda evt: self.frame.About())
        create_menu_item(
            menu,
            _("Quit"),
            lambda evt: (wx.CallAfter(self.Destroy), self.frame.Close(), exit(0)),
        )
        return menu


class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        kw["style"] = kw.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kw)

        self.statusbar = self.CreateStatusBar()
        self.SetStatusText(_("No open file."))

        self.isthreadon: bool = False
        self.isclosed: bool = False

        self.SetTitle("WallChange")
        self.SetSize(700, 600)

        self.BuildUI()
        self.AddMenu()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

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
        self.SetTitle("WallChange - {}".format(filepath))
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

        if hasattr(self, "lightbg" and "darkbg"):
            lightbg = self.lightbg
            darkbg = self.darkbg
        else:
            for item in self.buttons:
                if not os.path.isfile(item.GetLabel()):
                    return showdialog()
                else:
                    lightbg = self.buttons[0].GetLabel()
                    darkbg = self.buttons[1].GetLabel()

        if hasattr(self, "filepath"):
            for item in self.tree:
                if item.tag == "dark":
                    item.find("image").text = darkbg
                elif item.tag == "light":
                    item.find("image").text = lightbg

            with open(self.filepath, "wb") as f:
                ET.ElementTree(self.tree).write(f, "utf-8")
        else:
            callbacks.WriteNewFile(
                self, self.buttons[0].GetLabel(), self.buttons[1].GetLabel()
            )

        if self.isclosed == False:
            dlg = wx.MessageDialog(
                self,
                _("Start the wallpaper-set process now?"),
                _("Infomation"),
                style=wx.YES_NO,
            )
            if dlg.ShowModal() == wx.ID_YES:
                pass
            else:
                return
        self.thread = setwallpaper.AutoSet(self.filepath)
        self.isthreadon = True

    def OnClose(self, evt):
        if os.path.isfile(self.buttons[0].GetLabel()):
            self.lightbg = self.buttons[0].GetLabel()

        if os.path.isfile(self.buttons[1].GetLabel()):
            self.darkbg = self.buttons[1].GetLabel()
        self.isclosed = True
        evt.Skip()

    def IsShown(self):
        try:
            return super().IsShown()
        except RuntimeError:  # Window killed
            return False

    def ToggleMode(self):
        if self.isthreadon == True:
            del self.thread
            return

        if self.IsShown() == True:
            self.Save()
        elif hasattr(self, "isclosed") or not self.IsShown():
            if not hasattr(self, "lightbg" or "darkbg"):
                wx.MessageDialog(
                    None,
                    _(
                        "Get all required images first, then click the 'Save' button to start."
                    ),
                    _("Error"),
                    wx.OK | wx.ICON_ERROR,
                ).ShowModal()
                self.Show()
            else:
                self.Save()


class App(wx.App):
    def OnInit(self):
        self.frame = MainWindow(None)
        TaskBarIcon(self.frame)
        self.SetTopWindow(self.frame)
        self.SetExitOnFrameDelete(False)
        self.SetAppDisplayName("WallChange")
        self.frame.Show()
        return True
