# callbacks.py
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

import os.path
import xml.etree.cElementTree as ET

from gi.repository import Gtk, Adw # type: ignore
from . import imports

class XMLParseError(Exception):

    def __init__(self, msg: str, dont_show_toast: bool = False):
        if not dont_show_toast:
            toast = Adw.Toast.new()
            toast.set_title(msg)
            toast.show()
            del toast
        super().__init__(msg)

class FileHandler(object):
    
    currfile: str = ""
    tree = ET.ElementTree()
    configs: dict = {}

    def OpenXML(self, parent):
        def OpenXML_(dialog_, response):
            if response == Gtk.ResponseType.ACCEPT:
                self.currfile = dialog_.get_file().get_path()
                print(self.currfile)

        filter_ = Gtk.FileFilter()
        filter_.set_name("WallChange manifest")
        filter_.add_mime_type("application/xml")

        dialog = Gtk.FileChooserNative(
            title=_("Open a file to continue"),
            transient_for=parent, # https://gitlab.gnome.org/GNOME/pygobject/-/issues/484
            action=Gtk.FileChooserAction.OPEN
        )

        dialog.connect("response", OpenXML_)
        dialog.add_filter(filter_)
        dialog.show()

    def OpenImg(self, parent, type: str):
        def OpenImg_(dialog_, response):
            if response == Gtk.ResponseType.ACCEPT:
                imports.__dict__["%sBg" % type] = dialog_.get_file().get_path()

        filter_ = Gtk.FileFilter()
        filter_.set_name("Image files")
        filter_.add_mime_type("image/jpeg")
        filter_.add_mime_type("image/png")

        dialog = Gtk.FileChooserNative(
            title=_("Open a file to continue"),
            transient_for=parent,
            action=Gtk.FileChooserAction.OPEN
        )

        dialog.connect("response", OpenImg_)
        dialog.add_filter(filter_)
        dialog.show()

    def ReadXML(self) -> bool:
        if self.currfile == "" or not os.path.isfile(self.currfile):
            raise XMLParseError(_("Code error: FileHandler.currfile is blank or invalid data"))

        if self.tree.getroot().tag != "data":
            raise XMLParseError("Invalid root element on file: %s instead of 'data'" % self.tree.getroot().tag)
        else:
            for child in self.tree.getroot():
                if child.tag not in ["light", "dark", "config"]:
                    raise XMLParseError(
                        "Required tags not found: light, dark"
                    ) # config is optional, but suggested
                
                if child.tag == "config":
                    for text in ["notif"]:
                        self.configs[text] = child.find(text).text

                elif child.tag == "light" or "dark":
                    img = child.find("image").text # type: ignore
                    if os.path.isfile(img):
                        arr = ["L", "D"]
                        for item in arr:
                            if child.tag.startswith(item.lower()):
                                child.tag = item + child.tag[1:]
                        imports.__dict__["%sBg" % child.tag] = img
                    else:
                        raise XMLParseError(
                            "Image for %s variant not found: %s"
                            % child.tag, img
                        )