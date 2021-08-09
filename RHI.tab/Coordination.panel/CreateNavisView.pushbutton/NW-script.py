# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev 
# Reference information:
#(https://forums.autodesk.com/t5/revit-api-forum/hide-unhide-revitlinkinstance-in-visibility-settings/td-p/8194955)

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

def make_active(a):
    uidoc.ActiveView = doc.GetElement(a.Id)
    pass

class nw:  
    def __init__(self, Document):
        self.doc = Document

    def find_ex(self):
        navis3ds=[]
        elems = Autodesk.Revit.DB.FilteredElementCollector(doc).OfCategory(Autodesk.Revit.DB.BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
        for elem in elems:
            if elem.ViewType == ViewType.ThreeD :
                if "Navis" in elem.Name:
                    navis3ds.append(elem)
                elif "navis" in elem.Name:
                    navis3ds.append(elem)
            else:
                pass
        return navis3ds

    def create3D(self,option1):
        view3d = Autodesk.Revit.DB.View3D.CreateIsometric(doc, get3D_viewtype())
        try:
            view3d.Name = "Navis"
            #print(view3d.HasDetailLevel())
            #print(view3d.Id)
            
            #Change Detail Level to "Fine" of new Navis view
            view3d.DetailLevel = ViewDetailLevel.Fine
        
            #Changes Display Style to "FlatColors" of new Navis view
            view3d.DisplayStyle = DisplayStyle.FlatColors
            
            #Hide all annotations, import, point clouds on view
            view3d.AreAnnotationCategoriesHidden = True
            view3d.AreImportCategoriesHidden = True
            view3d.ArePointCloudsHidden = True
            
            if option1 == 1:
                view3d.HideElements(nw(doc).collect_links())
            else:
                pass

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
            return 'Error in creating 3D View'

    def create_default3D(self):
        view3d = Autodesk.Revit.DB.View3D.CreateIsometric(doc, get3D_viewtype())
        return view3d

    def collect_links(self):
        #links = []
        cl = FilteredElementCollector(doc) \
                .OfCategory(BuiltInCategory.OST_RvtLinks) \
                .ToElementIds()
        return cl

    def define_file_name(self):
        print(doc.Title)
        pass


msg = """Existing Navisworks view detected. Do you want to delete existing and create new one?"""
ops = ['Delete all and create new View','Keep existing']
cfgs = {'option1': { 'background': '0xFF55FF'}}
nwex = nw(doc).find_ex()



if nwex == []:
    #create3D View here with built-in setup
    with db.Transaction('Create Navis View'):
        nwnew = nw(doc).create3D(1)
    make_active(nwnew)

elif nwex != []:
    options = forms.CommandSwitchWindow.show(ops, 
                                             message='Existing Navisworks view/views detected. What Would you like to do?',
                                             config=cfgs,)
    if options == "Delete all and create new View":
        #print("Delete all and create new View")
        #Create Default 3D
        with db.Transaction("Create dummy 3D view"):
            def3D = nw(doc).create_default3D()
        make_active(def3D)
        #Delete all existing Navis views
        nw(doc).define_file_name()
        with db.Transaction("Delete Existing 'Navis' views"):
            for el_nw in nwex:
                doc.Delete(el_nw.Id)  
            nwnew = nw(doc).create3D(1)
            #doc.Delete(def3D)               
        make_active(nwnew)
    elif options == "Keep existing":
        print("make active 0")
        make_active(nwex[0])

