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

def get3D_viewtype():
    collector3d = FilteredElementCollector(doc).OfClass(Autodesk.Revit.DB.ViewFamilyType).ToElements()
    for el in collector3d:
        if el.ViewFamily == ViewFamily.ThreeDimensional:
            viewFamTypeId = el.Id
            return viewFamTypeId
        else:
            0


def create3D():
    view3d = View3D.CreateIsometric(doc, get3D_viewtype())
    try:
        view3d.Name = "Navis"
        print(view3d.DetailLevel)
        #uidoc.ShowElements(view3d.Id)
        print(uidoc.ActiveView.Title)
        print(view3d.Title)
    except:
        doc.Delete(view3d.Id)

    #for  view3d in views3d:
        #pass

def make_nwview_active():
    
    # = view3d
    #print(uidoc.ActiveView.GetOpenUIViews())
    #uidoc.ActiveView.Set(view3d)
    #uidoc.ActiveView.Set()
    pass

def find_nw_view():
    navis3ds=[]
    elems = Autodesk.Revit.DB.FilteredElementCollector(doc).OfCategory(Autodesk.Revit.DB.BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    for elem in elems:
        if elem.ViewType == ViewType.ThreeD :
            if "Navis" or "navis" in elem.Name:
                navis3ds.append(elem)
                #print(elem)
        else:
            pass
    return navis3ds


#views3d = []
#with db.Transaction('Create Navis View'):
#    print(create3D())


#print find_nw_view()
def check_views():
    if find_nw_view() != []:
        pyrevit.forms.alert_ifnot('Are you sure?',ok=False, yes=True, no=True, exitscript=True)
        print 'alert'



"""
with db.Transaction('Create Navis View'):
    try:
        create3D()
    except:
        forms.alert("Error occured")
"""
