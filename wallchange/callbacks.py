import os.path
import xml.etree.cElementTree as ET
import wx


class XMLParseError(Exception):
    pass


def OpenImg(parent, obj):
    dlg = wx.FileDialog(
        parent,
        _("Select your preferred background"),
        wildcard="Image file (*.png;*.jpg)|*.png;*.jpg",
        style=wx.FD_FILE_MUST_EXIST,
    )
    if dlg.ShowModal() != wx.ID_CANCEL:
        obj.SetLabel(dlg.GetPath())


def OpenXML(parent):
    dlg = wx.FileDialog(
        parent, _("Open WallChange manifest"), wildcard="XML File (*.xml)|*.xml",
        style=wx.FD_FILE_MUST_EXIST
    )
    if dlg.ShowModal() != wx.ID_CANCEL:
        return dlg.GetPath()
    else:
        return False


def ReadXML(path: str):
    def check_tag(tag: str):
        tags = ["light", "dark"]
        if not tag in tags:
            raise XMLParseError("Required tags not found: light, dark")

    all_childs = {}
    tree = ET.parse(path)

    if tree.getroot().tag != "data":
        raise XMLParseError(
            "Invalid root object tag: %s instead of 'data'" % tree.getroot().tag
        )
    else:
        for child in tree.getroot():
            try:
                check_tag(child.tag)
            except XMLParseError:
                break
            
            img = child.find("image").text
            if os.path.isfile(img):
                all_childs[child.tag] = img
            else:
                ImageNotFound(child.tag, img)
                raise XMLParseError

        return all_childs, tree.getroot()


def WriteNewFile(parent, light_bg: str, dark_bg: str):
    dlg = wx.FileDialog(
        parent,
        _("Save"),
        wildcard="XML File (*.xml)|*.xml",
        style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
    )
    if dlg.ShowModal() != wx.ID_CANCEL:
        tree = ET.Element("data")
        lightbg = ET.SubElement(tree, "light")
        darkbg = ET.SubElement(tree, "dark")
        ET.SubElement(lightbg, "image").text = light_bg
        ET.SubElement(darkbg, "image").text = dark_bg
        with open(dlg.GetPath(), "wb") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode("utf-8"))
            f.write(ET.tostring(tree, 'utf-8'))
        parent.filepath = dlg.GetPath()


def ImageNotFound(element, img):
    return wx.MessageDialog(
        wx.Frame(),
        _("Image not found for background variant {}: {}".format(element, img)),
    ).ShowModal()