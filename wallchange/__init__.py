import gettext
import locale
import os
import pathlib
import sys

from . import mainwindow, callbacks, setwallpaper

LOCALEDIR = "@LOCALEDIR@"
if LOCALEDIR == "@LOCALEDIR@":
    LOCALEDIR = pathlib.Path(__file__).parent / "po"


app_id = "me.lebao3105.wallchange"
locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain(app_id, LOCALEDIR)
gettext.textdomain(app_id)
gettext.install(app_id)
_ = gettext.gettext


def start_app():
    args = sys.argv
    argc = len(args) - 1
    root = mainwindow.App(0)

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
            root.frame.SetTitle(_("WallChange - {}".format(args[1])))
            root.frame.SetStatusText(args[1])

    root.MainLoop()
