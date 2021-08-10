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
            #Hide all annotations, import, point clouds on view
            view3d.AreAnnotationCategoriesHidden = True
            view3d.AreImportCategoriesHidden = True
            view3d.ArePointCloudsHidden = True

            if nw(doc).define_file_name() == 0:
                #Change Detail Level to "Fine" of new Navis view
                view3d.DetailLevel = ViewDetailLevel.Fine
            elif nw(doc).define_file_name() == 1:   
                view3d.DetailLevel = ViewDetailLevel.Medium
            else:
                view3d.DetailLevel = ViewDetailLevel.Fine
            #Changes Display Style to "FlatColors" of new Navis view
            view3d.DisplayStyle = DisplayStyle.FlatColors
            
            if option1 == 1:
                view3d.HideElements(nw(doc).collect_links())
            else:
                pass

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
        #print(doc.Title)
        if "KM" or "КМ" or "EKM" in doc.Title:
            return 1
        else:
            return 0


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
                                             message="""Existing Navisworks view/views detected. What would you like to do? 
                                             Обнаружен существующий вид/виды 'Navisworks'. Что выполнить далее? """,
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
                #print(el_nw.Id)
                doc.Delete(el_nw.Id)  
            nwnew = nw(doc).create3D(1)
            #print(def3D,def3D.Id.ToString())
            #doc.Delete(def3D.Id)  
        make_active(nwnew)
        with db.Transaction("Delete dummy 3D view"):   
           doc.Delete(def3D.Id)
    elif options == "Keep existing":
        try:
            make_active(nwex[0])
        except:
            pass
        pass