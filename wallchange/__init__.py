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
        try:
            childs, tree = callbacks.ReadXML(args[1])
        except callbacks.XMLParseError:
            pass
        else:
            lightbg = childs["light"]
            darkbg = childs["dark"]
            root.frame.buttons[0].SetLabel(lightbg)
            root.frame.buttons[1].SetLabel(darkbg)
            root.frame.filepath = args[1]
            root.frame.tree = tree
            root.frame.SetTitle("WallChange - {}".format(args[1]))
            root.frame.SetStatusText(args[1])

    root.MainLoop()
