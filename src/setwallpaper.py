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
import shutil

gi.require_version('Adw', '1')
from gi.repository import Adw, Notify
from . import imports

def SetWallpaper(path: str, mode: str):
    uri = "'file://%s'" % path
    if not shutil.which(path):
        ShowNotification('Image path not found: %s' % path)
        return False
    imports.ShellSchemas.set_string('picture-uri-%s' % mode, uri)
    imports.ShellSchemas.apply()
    if imports.NOTIF:
        Notify.init('me.lebao3105.wallchange')
        Notify.Notification.new('Successfully set wallpaper %s' % path).Show()
        Notify.uninit()
    ShowNotification('Successfully set wallpaper %s' % path)
    return True

def getPreferedColor():
    return darkdetect.theme().lower()

def ShowNotification(message, btn_label:str = "", action: str = ""):
    toast = Adw.Toast.new()
    if btn_label and action != "":
        toast.set_button_label(btn_label)
        toast.set_action_name(action)
    toast.set_title(message)

    return toast.notify()

def AutoSet(childs: dict):
    def setwall(theme):
        themes = {
            Adw.ColorScheme.DEFAULT: "light",
            Adw.ColorScheme.FORCE_DARK: "dark",
            Adw.ColorScheme.FORCE_LIGHT: "light",
            Adw.ColorScheme.PREFER_DARK: getPreferedColor(),
            Adw.ColorScheme.PREFER_LIGHT: getPreferedColor()
        }
        return SetWallpaper(childs[f"{themes[theme]}"], theme)

    setwall(imports.StyleMgr.get_color_scheme())
