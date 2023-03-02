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

@Gtk.Template(resource_path='/me/lebao3105/wallchange/views/window.ui')
class WallchangeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'WallchangeWindow'

    open_btn = Gtk.Template.Child()
    lightbg_btn = Gtk.Template.Child()
    darkbg_btn = Gtk.Template.Child()

    lightbg = Gtk.Template.Child()
    darkbg = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.filehandler = FileHandler()
        self.open_btn.connect('clicked', self.openfile_dlg)
        self.lightbg_btn.connect('clicked', self.lightbg_dlg)

    def openfile_dlg(self, button):
        return self.filehandler.OpenXML(self)
    
    def lightbg_dlg(self, button):
        self.filehandler.OpenImg(self, "Light")
        self.lightbg.set_label(imports.LightBg)
    
    def dark_dlg(self, button):
        self.filehandler.OpenImg(self, "Dark")
        self.darkbg.set_label(imports.DarkBg)

@Gtk.Template(resource_path='/me/lebao3105/wallchange/views/prefs.ui')
class PreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
    
