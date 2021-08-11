# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev 
# Reference information:
#(https://forums.autodesk.com/t5/revit-api-forum/hide-unhide-revitlinkinstance-in-visibility-settings/td-p/8194955)

__doc__ = """Создаёт 3D вид Navis. /Creates Navis 3D view.

Creates new 3D View for Navisworks export (Hides all annotations, imports, etc.) \
Searches for existing 3D Views, gives an option to delete existing view and \
create new one or preserve existed. 

Shift+Click — Keeps linked RVT files visible (for EFM coordination files) \
---------------------------------------------------------------------

Создаёт новый 3D вид Navisworks (скрывает аннотации, импорт DWG и т.д) \
Производит поиск существующих 3D видов и в случае наличия существуюего вида \
даёт возможность удалить и создать новый или оставить текущий. 

Shift+Click — Оставляет включенными связи RVT (для файлов промежуточной \
координации EFM) 
"""
__author__ = 'Roman Golev'
__title__ = "Create Navis\n View"
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
msg = """Existing Navisworks view detected. Do you want to delete existing and create new one?"""
ops = ['Delete all and create new View','Keep existing']
cfgs = {'option1': { 'background': '0xFF55FF'}}


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
            #Changes Display Style to "FlatColors" of new Navis view
            view3d.DisplayStyle = DisplayStyle.FlatColors

            if nw(doc).define_file_name() == 0:
                #Change Detail Level to "Fine" of new Navis view
                view3d.DetailLevel = ViewDetailLevel.Fine
            elif nw(doc).define_file_name() == 1:   
                view3d.DetailLevel = ViewDetailLevel.Medium
            else:
                view3d.DetailLevel = ViewDetailLevel.Fine

            if option1 == 1:
                try:
                    view3d.HideElements(nw(doc).collect_links())
                except:
                    pass
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


def main():
    nwex = nw(doc).find_ex()
    #links_on = 0
    if __shiftclick__:
        links_on = 0
    else :
        links_on = 1

    if nwex == []:
        t.Start("Create Navis View")
        try:
            nwnew = nw(doc).create3D(links_on)
            t.Commit()
            make_active(nwnew)
        except:
            t.RollBack()
            pyrevit.forms.alert("Error")


    elif nwex != []:
        options = forms.CommandSwitchWindow.show(ops, 
                                                message="""What would you like to do? / Что выполнить далее? """,
                                                config=cfgs,)
        if options == "Delete all and create new View":
            
            #Create Default 3D
            try:
                t.Start("Create dummy 3D view")
                def3D = nw(doc).create_default3D()
                t.Commit()
            except:
                t.RollBack()
                pyrevit.forms.alert("Error")                
            make_active(def3D)

            #Delete all existing Navis views and create new
            nw(doc).define_file_name()
            try:
                t.Start("Delete Existing 'Navis' views")
                for el_nw in nwex:
                    doc.Delete(el_nw.Id)
                nwnew = nw(doc).create3D(links_on)
                t.Commit()
            except:
                t.RollBack()
                pyrevit.forms.alert("Error")
            make_active(nwnew)

            #Delete dummy 3d view
            try:
                t.Start("Delete dummy 3D view")  
                doc.Delete(def3D.Id)
                t.Commit()
            except:
                t.RollBack()
                pyrevit.forms.alert("Error")
        elif options == "Keep existing":
            try:
                make_active(nwex[0])
            except:
                pass
            pass

if __name__ == '__main__':
    main()