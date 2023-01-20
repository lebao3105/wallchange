import darkdetect
import sys
import threading
import wx
import wx.adv

from . import callbacks


def SetWallpaper(path: str):
    if sys.platform == "win32":
        from ctypes import windll

        windll.user32.SystemParametersInfoW(20, 0, path, 0)
    elif sys.platform == "linux":
        import subprocess

        uri = "'file://%s'" % path
        args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
        subprocess.Popen(args)
    else:
        return wx.MessageDialog(
            wx.Frame(),
            _("Your platform is not supported ({}).".format(sys.platform)),
            style=wx.OK | wx.ICON_INFORMATION,
        ).ShowModal()
    return SendNotification(
        "WallChange", _("Successfully changed your desktop wallpaper. Enjoy!")
    )


def AutoSet(filepath: str):
    childs = callbacks.ReadXML(filepath)[0]

    def setwall(theme: str):
        theme = (
            theme.lower()
        )  # darkdetect.theme() returns Dark/Light, so we need to lower the fn input to dark/light
        return SetWallpaper(childs[theme])

    thread = threading.Thread(target=darkdetect.listener, args=(setwall,))
    thread.daemon = True
    thread.start()
    setwall(str(darkdetect.theme()))
    SendNotification(_("Infomation"), _("The auto-wallpaper service has been started."))
    return thread


def SendNotification(title, message, flags=wx.ICON_INFORMATION):
    return wx.adv.NotificationMessage(title, message, flags=flags).Show(50)
