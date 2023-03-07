# window.py
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

import threading
from gi.repository import Adw
from gi.repository import Gtk
from .callbacks import FileHandler
from .setwallpaper import AutoWallpaper
from . import imports


@Gtk.Template(resource_path="/me/lebao3105/wallchange/views/main.ui")
class WallchangeWindow(Adw.ApplicationWindow):
    __gtype_name__ = "MainWindow"

    lightbg = Gtk.Template.Child()
    darkbg = Gtk.Template.Child()
    toastoverlay = Gtk.Template.Child()
    thread = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filehandler = FileHandler(self, self.toastoverlay)
        self.autowall = AutoWallpaper(self.toastoverlay)

    @Gtk.Template.Callback()
    def openfile_dlg(self, button):
        return self.filehandler.OpenXML()

    @Gtk.Template.Callback()
    def lightbg_dlg(self, button):
        if self.filehandler.OpenImg("light"):
            self.lightbg.set_text(imports.lightBg)

    @Gtk.Template.Callback()
    def darkbg_dlg(self, button):
        if self.filehandler.OpenImg("dark"):
            self.darkbg.set_text(imports.darkBg)

    @Gtk.Template.Callback()
    def save_toggled(self, button):
        return self.filehandler.WriteNew()

    @Gtk.Template.Callback()
    def timing_toggled(self, button):
        if self.thread.get_text() == _("Start now"):
            self.autowall.StartThread()
            self.thread.set_text(_("Stop"))
        elif self.thread.get_text() == _("Stop"):
            self.autowall.StopThread()


@Gtk.Template(resource_path="/me/lebao3105/wallchange/views/prefs.ui")
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "PreferencesWindow"

    @Gtk.Template.Callback()
    def on_switch_button(self, switch, GParamBoolean):
        if switch.get_active():
            # print('activated')
            imports.NOTIF = True
        else:
            # print('turned off')
            imports.NOTIF = False

        imports.AppSchemas.set_boolean("notify-me", imports.NOTIF)
        imports.AppSchemas.apply()
