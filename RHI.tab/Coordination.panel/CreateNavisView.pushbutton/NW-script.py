# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev 

__doc__ = 'Создаёт 3D вид Navis. /Creates Navis 3D view.'
__author__ = 'Roman Golev'
__title__ = "Navis\n3D View"

import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB import AssemblyViewUtils
from Autodesk.Revit.DB import FilteredWorksetCollector
import System
clr.AddReference('RevitAPIUI')
import pyrevit
from pyrevit import forms
from collections import namedtuple

import rpw
from rpw import db

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application

# worksets = []
# if doc.IsWorkshared == True:
#     wsCollector = FilteredWorksetCollector(doc).ToWorksets()
#     for workset in  wsCollector:
#         if workset.Kind == Autodesk.Revit.DB.WorksetKind.UserWorkset:
#             worksets.append(workset)
#         else:
#             pass
# else:
#     forms.alert("File is not workshared")

collector3d = FilteredElementCollector(doc).OfClass(Autodesk.Revit.DB.ViewFamilyType).ToElements()
for el in collector3d:
    if el.ViewFamily == ViewFamily.ThreeDimensional:
        viewFamTypeId = el.Id


#views3d = []
def create3D():
    view3d = View3D.CreateIsometric(doc, viewFamTypeId)
    #views3d.append(view3d)
    try:
        view3d.Name = "Navis"
        print(view3d.DetailLevel)
        #uidoc.ShowElements(view3d.Id)
        print(uidoc.ActiveView())# = view3d
    except:
            doc.Delete(view3d.Id)

    #for  view3d in views3d:
        #pass

with db.Transaction('Create Navis View'):
    try:
        create3D()
    except:
        forms.alert("Error occured")