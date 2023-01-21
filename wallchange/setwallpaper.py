import darkdetect
import subprocess
import sys
import threading
import wx
import wx.adv

from . import callbacks


def SetWallpaper(path: str, mode):
    """
    Set wallpaper for supported platform(s):
    * Windows (of course) - 10 (1607+)
    * *NIX (Linux, BSD, and macOS)
    """
    if sys.platform == "win32":
        from ctypes import windll

        windll.user32.SystemParametersInfoW(20, 0, path, 0)
    elif sys.platform == "linux":
        uri = "'file://%s'" % path
        if mode == "dark":
            schema = "picture-uri-dark"
        else:
            schema = "picture-uri"
        args = ["gsettings", "set", "org.gnome.desktop.background", schema, uri]
        subprocess.Popen(args)
    elif sys.platform == "darwin":
        args = ["wallpaper", path]
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
        return SetWallpaper(childs[theme], theme)

    thread = threading.Thread(target=darkdetect.listener, args=(setwall,))
    thread.daemon = True
    thread.start()
    setwall(str(darkdetect.theme()))
    SendNotification(_("Infomation"), _("The auto-wallpaper service has been started."))
    return thread


def SendNotification(title, message, flags=wx.ICON_INFORMATION):
    return wx.adv.NotificationMessage(title, message, flags=flags).Show(50)
