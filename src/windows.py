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

from gi.repository import Adw
from gi.repository import Gtk
from .callbacks import FileHandler
from . import imports

@Gtk.Template(resource_path='/me/lebao3105/wallchange/views/main.ui')
class WallchangeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'MainWindow'

    lightbg = Gtk.Template.Child()
    darkbg = Gtk.Template.Child()
    filehandler = FileHandler()

    @Gtk.Template.Callback()
    def openfile_dlg(self, button):
        return self.filehandler.OpenXML(self)
    
    @Gtk.Template.Callback()
    def lightbg_dlg(self, button):
        self.filehandler.OpenImg(self, "Light")
        self.lightbg.set_text(imports.LightBg)
    
    @Gtk.Template.Callback()
    def darkbg_dlg(self, button):
        self.filehandler.OpenImg(self, "Dark")
        self.darkbg.set_text(imports.DarkBg)

    @Gtk.Template.Callback()
    def save_toggled(self, switch, GParamBoolean):
        self.save = switch.get_active()
    
    @Gtk.Template.Callback()
    def timing_toggled(self, switch, GParamBoolean):
        self.timing = switch.get_active()

@Gtk.Template(resource_path='/me/lebao3105/wallchange/views/prefs.ui')
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesWindow'

    @Gtk.Template.Callback()
    def on_switch_button(self, switch, GParamBoolean):
        if switch.get_active():
            #print('activated')
            imports.NOTIF = True
        else:
            #print('turned off')
            imports.NOTIF = False
            
        imports.AppSchemas.set_boolean('notify-me', imports.NOTIF)
        imports.AppSchemas.apply()
    
