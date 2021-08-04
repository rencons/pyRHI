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

def make_active(a):
    uidoc.ActiveView = doc.GetElement(a.Id)
    print("make active 2")
    pass

class nw:  
    def __init__(self, Document):
        self.doc = Document
        self.navis3ds = []


    def find_ex(self):
        get3D_viewtype()
        navis3ds=[]
        elems = Autodesk.Revit.DB.FilteredElementCollector(doc).OfCategory(Autodesk.Revit.DB.BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
        for elem in elems:
            if elem.ViewType == ViewType.ThreeD :
                if "Navis" in elem.Name:
                    navis3ds.append(elem)
                    #print(elem.Name)
                    print(elem.ViewTemplateId)
                    #print(elem.AreAnnotationCategoriesHidden)
                elif "navis" in elem.Name:
                    navis3ds.append(elem)
                    #print(elem.Name)
                    print(elem.ViewTemplateId)
            else:
                pass
        return navis3ds

    def create3D(self):
        view3d = Autodesk.Revit.DB.View3D.CreateIsometric(doc, get3D_viewtype())
        try:
            view3d.Name = "Navis"
            #print(view3d.HasDetailLevel())
            #print(view3d.Id)
            
            #Change Detail Level to "Fine" of new Navis view
            view3d.DetailLevel = ViewDetailLevel.Fine
        
            #Changes Display Style to "FlatColors" of new Navis view
            view3d.DisplayStyle = DisplayStyle.FlatColors
            
            #Hide all annotations categories on view
            view3d.AreAnnotationCategoriesHidden = True



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
            return 'Error in creating 3D View'

    def collect_links(self):
        #Autodesk.Revit.DB.View.HideElements()
        #Collects links from model in format
        #{ LinkType: [LinkInstance, LinkInstance, ... ] }
        #:return:
        links = {}
        cl = FilteredElementCollector(doc).OfCategory(
            BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElementIds()
        #cll = FilteredElementCollector(doc).OfCategory(
        #    BuiltInCategory.OST_RvtLinks).OfClass(typeof(RevitLinkInstance)).ToElementIds()
        #print(i for i in cl)#,cll)
        for e_id in cl:
            e = doc.GetElement(e_id)
            type_id = e.GetTypeId()
            if type_id not in links:
                links[type_id] = []
            links[type_id].append(e_id)
        return links


msg = """Existing Navisworks view detected. Do you want to delete existing and create new one?"""
ops = ['Delete all and create new View','Keep existing']
cfgs = {'option1': { 'background': '0xFF55FF'}}
nwex = nw(doc).find_ex()
#print(nw(doc).collect_links())

#(https://forums.autodesk.com/t5/revit-api-forum/hide-unhide-revitlinkinstance-in-visibility-settings/td-p/8194955)

if nwex == []:
    #create3D View here with built-in setup
    with db.Transaction('Create Navis View'):
        nwnew = nw(doc).create3D()
    make_active(nwnew)
    with db.Transaction('Create Navis View1'):
        #Collect links with method
        for i in nw(doc).collect_links():
            print(i)
            #Autodesk.Revit.DB.View.HideElements(i)
            doc.ActiveView.HideElements(FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElementIds())
        
elif nwex != []:
    #options = pyrevit.forms.alert(msg, ok=False, yes=True, no=True, exitscript=True)
    options = forms.CommandSwitchWindow.show(ops, 
                                             message='Existing Navisworks view/views detected. What Would you like to do?',
                                             config=cfgs,)
    #print(options)
    if options == "Delete all and create new View":
        print(1)
        #Delete all existing Navis views
        #Create new 3D View
        #Make new 3D Active  
    elif options == "Keep existing":
        print("make active 0")
        make_active(nwex[0])
        print("make active 1")

    print(options)






"""

#views3d = []
#with db.Transaction('Create Navis View'):
#    print(create3D())
with db.Transaction('Create Navis View'):
    try:
        new3D = create3D()
    except:
        forms.alert("Error occured")

if new3D != None:
    uidoc.ActiveView = doc.GetElement(new3D.Id)


"""