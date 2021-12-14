# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev
#Reference (https://www.revitapidocs.com/2020/c72daf7a-43da-a480-d093-e3d6a96d9a76.htm)
# (https://www.revitapidocs.com/2019/cc284f13-a7a9-d37e-e46d-4769bf039a96.htm)
# (https://stackoverflow.com/questions/51370445/how-to-get-project-guid-and-model-guid-from-pathname)

__doc__ = """. \
    /Add more Revit links from Autodesk Docs и BIM360

.

Shift+Click — \
---------------------------------------------------------------------



Shift+Click — )
"""
__author__ = 'Roman Golev'
__title__ = "Link Cloud\n RVTs"
#__helpurl__ = ""

import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.ApplicationServices import Application
from Autodesk.Revit.DB import ModelPathUtils
from System import Guid

clr.AddReference('System')
clr.AddReference('RevitAPIUI')
import pyrevit
from pyrevit import forms


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application
t = Autodesk.Revit.DB.Transaction(doc)

versionNumber = uiapp.Application.VersionNumber
#print(uiapp.Application.VersionNumber)
#print(uiapp.Application.VersionName)
#print(uiapp.Application.Language)

projectId = Guid("ce62d13c-842f-4309-ba06-ffe7ff84a7a1")
modelId = Guid("adbd671b-e80a-4927-a1b6-aa5ec06ed934")

def main():
    #revitLinkTypeId = 0
    #placement = ImportPlacement.Site
    #Autodesk.Revit.DB.RevitLinkInstance.Create(doc,revitLinkTypeId,placement)
    t.Start("Link Cloud Model")
    mp = ModelPathUtils.ConvertCloudGUIDsToCloudPath(projectId,modelId)
    print(mp)
    o = RevitLinkOptions(False)
    linkType = RevitLinkType.Create(doc, mp, o)
    instance = RevitLinkInstance.Create(doc, linkType.ElementId)
    t.Commit()
    return instance



"""
    if versionNumber == 2020:
        123

    elif versionNumber == 2021 or 2021:
        123
"""




if __name__ == '__main__':
    main()
