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

from gi.repository import Gtk, Adw
from . import imports

class XMLParseError(Exception):

    def __init__(self, msg: str, dont_show_toast: bool = False, toastoverlay: Adw.ToastOverlay = None):
        if not dont_show_toast:
            if not toastoverlay:
                raise Exception("dont_show_toast parameter set to False but toast is None")
            toastoverlay.add_toast(Adw.Toast.new(msg))

        super().__init__(msg)

class FileHandler(object):
    
    currfile: str = ""
    tree = ET.ElementTree()
    configs: dict = {}

    # Global file filters
    xmlflt = Gtk.FileFilter()
    xmlflt.set_name("WallChange manifest")
    xmlflt.add_mime_type("application/xml")

    imagesflt = Gtk.FileFilter()
    imagesflt.set_name("Image files")
    imagesflt.add_mime_type("image/jpeg")
    imagesflt.add_mime_type("image/png")

    def __init__(self, parent, toastoverlay: Adw.ToastOverlay):
        self.parent = parent
        self.toaster = toastoverlay

    def OpenXML(self):
        def OpenXML_(dialog_, response):
            if response == Gtk.ResponseType.ACCEPT:
                self.currfile = dialog_.get_file().get_path()
                # print(self.currfile)

        dialog = Gtk.FileChooserNative(
            title=_("Open a file to continue"),
            transient_for=self.parent, # https://gitlab.gnome.org/GNOME/pygobject/-/issues/484
            action=Gtk.FileChooserAction.OPEN
        )

        dialog.connect("response", OpenXML_)
        dialog.add_filter(self.xmlflt)
        dialog.show()

    def OpenImg(self, imgtype: str):
        def OpenImg_(dialog_, response):
            if response == Gtk.ResponseType.ACCEPT:
                imports.__dict__["%sBg" % imgtype] = dialog_.get_file().get_path()

        dialog = Gtk.FileChooserNative(
            title=_("Open a file to continue"),
            transient_for=self.parent,
            action=Gtk.FileChooserAction.OPEN
        )

        dialog.connect("response", OpenImg_)
        dialog.add_filter(self.imagesflt)
        dialog.show()

    def ReadXML(self) -> bool:
        if self.currfile == "" or not os.path.isfile(self.currfile):
            raise XMLParseError(
                _("Code error: FileHandler.currfile is blank or invalid data"),
                self.toaster
            )

        if self.tree.getroot().tag != "data":
            raise XMLParseError(
                _("Invalid root element on file: %s instead of 'data'" % self.tree.getroot().tag),
                self.toaster
            )
        else:
            for child in self.tree.getroot():
                if child.tag not in ["light", "dark", "config"]:
                    raise XMLParseError(
                        _("Required tags not found: light, dark"),
                        self.toaster
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
                            _("Image for background %s variant not found: %s"
                            % child.tag, img), self.toaster
                        )
    
    def WriteNew(self, showtoast:bool = True, show_save_dialog:bool = True):
        ready: bool = False

        def dialog_response(dlg, response):
            nonlocal ready
            if response == Gtk.ResponseType.ACCEPT:
                self.currfile = dlg.get_file().get_path()
                ready = True
            else:
                ready = False
            
        def MakeTree():
            tree = ET.Element("data")
            config = ET.Element(tree, "config")
            light = ET.SubElement(tree, "light")
            dark = ET.SubElement(tree, "dark")

            ET.SubElement(light, "image").text = imports.LightBg
            ET.SubElement(dark, "image").text = imports.DarkBg
            ET.SubElement(config, "notif").text = str(imports.NOTIF)

            return tree
        
        if not os.path.isfile(imports.DarkBg):
            raise XMLParseError(_("Dark wallpaper not found in PC or not selected"), False, self.toaster)
        
        if not os.path.isfile(imports.LightBg):
            raise XMLParseError(_("Light wallpaper not found in PC or not selected"), False, self.toaster)
        
        if show_save_dialog:
            dialog = Gtk.FileChooserNative(
                title=_("File save"),
                transient_for=self.parent,
                action=Gtk.FileChooserAction.SAVE
            )
            dialog.add_filter(self.xmlflt)
            dialog.connect('response', dialog_response)
            dialog.show()

        if ready:
            tree = MakeTree()
            with open(self.currfile, "wb") as f:
                f.write('<?xml version="1.0" encoding="UTF-8">\n'.encode("utf-8"))
                f.write(ET.tostring(tree, "utf-8"))
        else:
            return
        
        if showtoast:
            self.toaster.add_toast(Adw.Toast.new(_("Wrote file %s - please check if the operation is really completed." % self.currfile)))