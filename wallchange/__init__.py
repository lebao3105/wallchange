import gettext
import locale
import pathlib
import sys
import wx

from . import mainwindow, callbacks
LOCALEDIR = "@LOCALEDIR@"
IS_MESONTOUCHED = "@ISMESONTOUCHED@"  # Meson

if LOCALEDIR == "@LOCALEDIR@" and IS_MESONTOUCHED != "True":
    LOCALEDIR = pathlib.Path(__file__).parent / "po"

APP_ID = "me.lebao3105.wallchange"

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain(APP_ID, LOCALEDIR)
gettext.textdomain(APP_ID)
gettext.install(APP_ID)


def start_app():
    args = sys.argv[1:]
    argc = len(args)

    root = wx.App()
    mainwind = mainwindow.MainWindow(None, title="WallChange")
    mainwindow.TaskBarIcon(mainwind)
    root.SetTopWindow(mainwind)
    mainwind.Show()

    if argc > 0:
        mainwind.reader.read(args[0])
        mainwind.buttons[0].SetLabel(mainwind.reader.images["light"])
        mainwind.buttons[1].SetLabel(mainwind.reader.images["dark"])
        mainwind.filepath = args[0]
        mainwind.SetTitle("WallChange - {}".format(args[1]))
        mainwind.SetStatusText(args[0])
        mainwind.Refresh()

    root.MainLoop()
