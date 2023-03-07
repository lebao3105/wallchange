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

gi.require_version('Notify', '0.7')
from gi.repository import Adw, Notify
from . import imports

class AutoWallpaper(object):

    def __init__(self, toastoverlay: Adw.ToastOverlay):
        self.toaster = toastoverlay
    
    def getPreferedColor(self):
        return darkdetect.theme().lower() # This project depends on shell + application themes

    def SetWallpaper(self, variant: str):
        path = self.__dict__[variant + "bg"]
        uri = "'file://%s'" % path
        
        if not shutil.which(path):
            self.ShowNotification(_('Image path not found: %s' % path))
            return False
        imports.ShellSchemas.set_string('picture-uri-%s' % variant, uri)
        imports.ShellSchemas.apply()
        
        if imports.NOTIF:
            Notify.init('me.lebao3105.wallchange')
            Notify.Notification.new(_('Successfully set wallpaper %s' % path)).Show()
            Notify.uninit()
        self.ShowNotification(_('Successfully set wallpaper %s' % path))
        return True
    
    def ShowNotification(self, msg: str, action: str = "", action_label: str = ""):
        toast = Adw.Toast.new(msg)
        if action and action_label != "":
            toast.set_button_label(action_label)
            toast.set_action_name(action)
        
        return self.toaster.add_toast(toast)

    def AutoSet(self, childs: dict): # TODO: Fix this parameter
        def setwall(theme):
            themes = {
                Adw.ColorScheme.DEFAULT: "light",
                Adw.ColorScheme.FORCE_DARK: "dark",
                Adw.ColorScheme.FORCE_LIGHT: "light",
                Adw.ColorScheme.PREFER_DARK: self.getPreferedColor(),
                Adw.ColorScheme.PREFER_LIGHT: self.getPreferedColor()
            }
            self.__dict__[theme + "bg"] = childs[f"{themes[theme]}"]
            return self.SetWallpaper(theme)

        return setwall(imports.StyleMgr.get_color_scheme())
