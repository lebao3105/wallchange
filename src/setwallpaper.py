# setwallpaper.py
#
# Copyright 2023 Le Bao Nguyen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import darkdetect
import gi
import os.path
import threading

gi.require_version("Notify", "0.7")
from gi.repository import Adw, Notify
from . import imports


class AutoWallpaper(object):
    def __init__(self, toastoverlay: Adw.ToastOverlay):
        self.toaster = toastoverlay

    def applySchemas(self):
        if not imports.DarkBg or imports.LightBg:
            return False
        imports.AppSchemas.set_string("dark-wallpaper", imports.DarkBg)
        imports.AppSchemas.set_string("light-wallpaper", imports.LightBg)
        imports.AppSchemas.apply()

    def SetWallpaper(self, variant: str):
        path_ = imports.__dict__[variant + "Bg"]
        uri = "'file://%s'" % path_

        if not os.path.isfile(path_):
            self.ShowNotification(_("Image path not found: %s" % path_))
            return False
        imports.ShellSchemas.set_string("picture-uri-%s" % variant, uri)
        imports.ShellSchemas.apply()

        if imports.NOTIF:
            Notify.init("me.lebao3105.wallchange")
            Notify.Notification.new(_("Successfully set wallpaper %s" % path_)).Show()
            Notify.uninit()
        self.ShowNotification(_("Successfully set wallpaper %s" % path_))
        return True

    def ShowNotification(self, msg: str, action: str = "", action_label: str = ""):
        toast = Adw.Toast.new(msg)
        if action and action_label != "":
            toast.set_button_label(action_label)
            toast.set_action_name(action)

        return self.toaster.add_toast(toast)

    def AutoSet(self, theme: str):
        def setwall(_theme):
            themes = {
                Adw.ColorScheme.DEFAULT: "light",
                Adw.ColorScheme.FORCE_DARK: "dark",
                Adw.ColorScheme.FORCE_LIGHT: "light",
                Adw.ColorScheme.PREFER_DARK: theme.lower(),
                Adw.ColorScheme.PREFER_LIGHT: theme.lower(),
            }
            return self.SetWallpaper(themes[_theme])

        return setwall(imports.StyleMgr.get_color_scheme())

    def StartThread(self):
        self.thread = threading.Thread(
            target=darkdetect.listener, args=self.AutoSet, daemon=True
        )
        self.thread.start()
        self.ShowNotification(_("Thread started."))

    def StopThread(self):
        if hasattr(self, "thread"):
            del self.thread
        else:
            print("Code mistake: Thread not started or already killed")
