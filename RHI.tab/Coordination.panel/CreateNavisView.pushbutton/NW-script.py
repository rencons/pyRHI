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
        #print(view3d.HasDetailLevel())
        print(view3d.Id)
        
        #Changes Detail Level to "Fine" of new Navis view
        view3d.DetailLevel = ViewDetailLevel.Fine
    
        #Changes Display Style to "FlatColors" of new Navis view
        view3d.DisplayStyle = DisplayStyle.FlatColors
        

        #TODO: Hide all anotation categories
        #TODO: Set Medium Detail Level for Structural Framing, Structural Columns, etc..
        #print(view3d.DetailLevel)
        #uidoc.ShowElements(view3d.Id)
        #print(uidoc.ActiveView.Title)
        #print(uidoc.ActiveView)
        #print(doc.GetElement(view3d.Id))
        #uidoc.ActiveView = doc.GetElement(view3d.Id)
        #print(view3d.Title)
        return view3d

        
    except:
        doc.Delete(view3d.Id)

    #for  view3d in views3d:
        #pass



def collect_links():
    """
    Collects links from model in format
    { LinkType: [LinkInstance, LinkInstance, ... ] }

    :return:
    dict
    """

    links = {}

    cl = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElementIds()
    for e_id in cl:
        e = doc.GetElement(e_id)
        type_id = e.GetTypeId()
        if type_id not in links:
            links[type_id] = []
        links[type_id].append(e)

    return links


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
            if "Navis" in elem.Name:
                navis3ds.append(elem)
                #print(elem.Name)
            elif "navis" in elem.Name:
                navis3ds.append(elem)
                #print(elem.Name)
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
        print('alert')




with db.Transaction('Create Navis View'):
    try:
        new3D = create3D()
    except:
        forms.alert("Error occured")


if new3D != "":
    uidoc.ActiveView = doc.GetElement(new3D.Id)
