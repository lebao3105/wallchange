import os
import pathlib
import platform
import xml.etree.cElementTree as ET
import wx
import wx.adv

from . import callbacks, setwallpaper, imports

TRAY_TOOLTIP = "WallChange"
ICON = "{}.svg".format("me.lebao3105.wallchange")
TRAY_ICON = str(pathlib.Path(__file__).parent / ".." / "icons" / ICON)


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        super(wx.adv.TaskBarIcon, self).__init__()
        self.frame = frame
        self.SetIcon(wx.Icon(TRAY_ICON), TRAY_TOOLTIP)
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
            lambda evt: (wx.CallAfter(exit), self.frame.Close(), self.Destroy()),
        )
        return menu


class MainWindow(wx.Frame):
    def __init__(self, *args, **kw):
        kw["style"] = kw.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kw)

        self.statusbar = self.CreateStatusBar()
        self.SetStatusText(_("No open file."))
        # self.SetIcon(wx.Icon(TRAY_ICON, wx.BITMAP_TYPE_ANY))

        self.isthreadon: bool = False
        self.isclosed: bool = False
        self.reader = callbacks.XmlReader(self, skip_file_read=True)

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
        filemenu.AppendSeparator()
        cmds["notif"] = wx.MenuItem(filemenu, wx.ID_ANY, _("Don't notify me on wallpaper changes"))
        filemenu.Append(cmds["notif"])
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
            cmds["exit"]: lambda evt: self.Close(),
            cmds["notif"]: lambda evt: self.ToggleNotify(cmds["notif"])
        }

        for item in allcmds:
            self.Bind(wx.EVT_MENU, allcmds[item], item)

        self.timer = wx.Timer()
        self.timer.Start()
        self.Bind(wx.EVT_TIMER, lambda evt: self.ToggleNotify(cmds["notif"], True))

        self.SetMenuBar(menu)

    def BuildUI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Light background
        label1 = wx.StaticText(panel, -1, _("Light background"))
        sizer.Add(label1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        button_1 = wx.Button(panel, -1, _("Select an image"))
        button_1.Bind(wx.EVT_BUTTON, lambda evt: callbacks.OpenImg(self, button_1))
        sizer.Add(button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Dark background
        label2 = wx.StaticText(panel, -1, _("Dark background"))
        sizer.Add(label2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        button_2 = wx.Button(panel, -1, _("Select an image"))
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
        Dynamically theme your desktop (background)!
        wxPython version: {wxver}
        Python version: {pyver}
        OS type: {ostype}
        """
        )
        aboutinf = wx.adv.AboutDialogInfo()
        # aboutinf.SetIcon(wx.Icon(TRAY_ICON))
        aboutinf.SetName("WallChange")
        aboutinf.SetDescription(msg)
        aboutinf.SetCopyright("(C) 2022-2023 Le Bao Nguyen")
        aboutinf.AddDeveloper("Le Bao Nguyen")
        return wx.adv.AboutBox(aboutinf)

    def OpenFile(self) -> bool:
        filepath = callbacks.OpenXML(self)
        if filepath is False:
            return False
        else:
            # try:
            #     self.reader.read(filepath)
            # except callbacks.XMLParseError:
            #     return False
            self.reader.read(filepath)
            
            self.buttons[0].SetLabel(self.reader.images["light"])
            self.buttons[1].SetLabel(self.reader.images["dark"])
            imports.NOTIF = bool(self.reader.configs["notif"])

            self.SetTitle("WallChange - {}".format(filepath))
            self.SetStatusText(filepath)
            self.Refresh()

    def CloseFile(self):
        for item in self.buttons:
            item.SetLabel(_("Select an image"))

    def Save(self):
        def showdialog():
            return wx.MessageDialog(
                self,
                _("Image not found, or you have not filled this section yet."),
                _("Error"),
                style=wx.OK | wx.ICON_ERROR,
            ).ShowModal()

        for button in self.buttons:
            if not os.path.isfile(button.GetLabel()):
                return showdialog()
            
        self.reader.images["light"] = self.buttons[0].GetLabel()
        self.reader.images["dark"] = self.buttons[1].GetLabel()

        self.reader.writenew(True if not os.path.isfile(self.GetStatusBar().GetStatusText()) else False)

        if self.isclosed == False:
            dlg = wx.MessageDialog(
                self,
                _("Start the wallpaper-set process now?"),
                _("Infomation"),
                style=wx.YES_NO,
            )
            if dlg.ShowModal() == wx.ID_YES:
                self.thread = setwallpaper.AutoSet(self.reader.images)
                self.isthreadon = True
            else:
                return
            

    def OnClose(self, evt):
        if os.path.isfile(self.buttons[0].GetLabel()):
            self.reader.images["light"] = self.buttons[0].GetLabel()

        if os.path.isfile(self.buttons[1].GetLabel()):
            self.reader.images["drak"] = self.buttons[1].GetLabel()

        self.isclosed = True
        self.Hide()

    def ToggleMode(self):
        if self.isthreadon == True:
            del self.thread
            setwallpaper.SendNotification(
                _("Infomation"), _("Turned off auto wallpaper-set service.")
            )
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
                self.Show(True)
            else:
                self.Save()

    def ToggleNotify(self, menuitem:wx.MenuItem, skip_replace:bool=False) -> bool:
        arr = {True: False, False:True}
        if not skip_replace:
            imports.NOTIF = arr[imports.NOTIF]
        menuitem.SetItemLabel(_("Notify me on wallpaper changes") if not imports.NOTIF else _("Don't notify me on wallpaper changes"))
        return imports.NOTIF