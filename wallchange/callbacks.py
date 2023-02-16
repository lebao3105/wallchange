import os.path
import xml.etree.cElementTree as ET
import wx

from . import imports

class XMLParseError(Exception):
    pass


def OpenXML(parent) -> str|bool:
    dlg = wx.FileDialog(
        parent,
        _("Open a WallChange manifest"),
        wildcard="XML File (*.xml)|*.xml",
        style=wx.FD_FILE_MUST_EXIST
    )
    if dlg.ShowModal() != wx.ID_CANCEL:
        return dlg.GetPath()
    else:
        return False


def OpenImg(parent, obj):
    dlg = wx.FileDialog(
        parent,
        _("Select your preferred background"),
        wildcard="Image file (*.png;*.jpg)|*.png;*.jpg",
        style=wx.FD_FILE_MUST_EXIST,
    )
    if dlg.ShowModal() != wx.ID_CANCEL:
        obj.SetLabel(dlg.GetPath())

def ImageNotFound(element, img):
    return wx.MessageDialog(
        wx.Frame(),
        _("Image not found for background variant {}: {}".format(element, img)),
    ).ShowModal()


class XmlReader(object):

    def __init__(self, parent, file:str="", skip_file_read:bool=False):
        """
        Constructor of the class.
        """
        self.parent = parent
        if skip_file_read:
            self.tree = ET.ElementTree()
            self.file = ""
        else:
            self.tree = ET.parse(file)
            self.file = file
        self.images = {}
        self.configs = {}
    
    def read(self, file:str=""):
        if file != "":
            self.tree.parse(file)
            self.file = file

        if self.tree.getroot().tag != "data":
            raise XMLParseError(
                "Invalid root object tag: %s instead of 'data'" % self.tree.getroot().tag
            )
        else:
            for child in self.tree.getroot():
                if child.tag not in ["light", "dark", "config"]:
                    raise XMLParseError(
                        "Required tags not found: light, dark"
                    )

                if child.tag == "config":
                    for text in ["notif"]:
                        self.configs[text] = child.find(text).text

                elif child.tag == "light" or "dark":
                    img = child.find("image").text
                    if os.path.isfile(img):
                        self.images[child.tag] = img
                    else:
                        ImageNotFound(child.tag, img)
                        raise XMLParseError

    def writenew(self, showdlg:bool=True):
        def _write(path:str):
            tree = ET.Element("data")
            config = ET.SubElement(tree, "config")
            light = ET.SubElement(tree, "light")
            dark = ET.SubElement(tree, "dark")
            
            ET.SubElement(light, "image").text = self.images["light"]
            ET.SubElement(dark, "image").text = self.images["dark"]
            ET.SubElement(config, "notif").text = str(imports.NOTIF)

            with open(path, "wb") as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode("utf-8"))
                f.write(ET.tostring(tree, 'utf-8'))

            self.file = path

        if showdlg:
            dlg = wx.FileDialog(
                self.parent,
                _("Save"),
                wildcard="XML File (*.xml)|*.xml",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )
            if dlg.ShowModal() != wx.ID_CANCEL:
                _write(dlg.GetPath())
                return True
            else:
                return False
        else:
            _write(self.file)
            return True

                    