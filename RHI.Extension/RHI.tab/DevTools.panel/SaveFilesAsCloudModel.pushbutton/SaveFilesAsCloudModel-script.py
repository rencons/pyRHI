# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev
#Reference (https://www.revitapidocs.com/2020/c72daf7a-43da-a480-d093-e3d6a96d9a76.htm)
# (https://thebuildingcoder.typepad.com/blog/2019/11/initiating-bim360-collaboration-and-linking.html)

__doc__ = """Загружает пакетно модели на Autodesk Docs и BIM360. \
    /Saves files in batch for Autodesk Docs и BIM360

.

Shift+Click — \
---------------------------------------------------------------------



Shift+Click — )
"""
__author__ = 'Roman Golev'
__title__ = "Batch Save\n As Cloud"
#__helpurl__ = ""

import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

clr.AddReference('System')
clr.AddReference('RevitAPIUI')
import pyrevit
from pyrevit import forms


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application
t = Autodesk.Revit.DB.Transaction(doc)

#TODO Pick Revit vesion and change algoryphm based on version running


def main():
    #Pick destination location
    #TODO search for folders
    #Pick files (Get)
    folderId = "urn:adsk.wipprod:fs.folder:co.q7BLwRsbQ8-E7jbIBwrhJQ"
    
    #TODO Enter Multitiple docs
    modelName = doc.Title.ToString()

    #TODO Iterate on Multiple docs
    Autodesk.Revit.DB.Document.SaveAsCloudModel(doc,folderId,modelName)






if __name__ == '__main__':
    main()
