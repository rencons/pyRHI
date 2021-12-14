# -*- coding: utf-8 -*- 
__doc__ = """
Check the consistency of Assembly Code for model elements \
and temporarily isolates the elements for which the assembly \
code should be filled.

Shift+Click — shows a list of elements that does not contain the parameter

---------------------------------------------------------------------
Проверяет наполнение информационной модели кодом по классификатору и \
временно изолирует элементы, для которых необходимо заполнить код.

Shift+Click — показывает список элементов, для которых не заполнен \
параметр
"""

__title__ = "Check\nWBS Code"

#import re
#import os

import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons


clr.AddReference('System')
from System.Collections.Generic import List
clr.AddReference('RevitAPIUI')
import pyrevit
from pyrevit import forms
from pyrevit import script
from pyrevit.coreutils import charts
#from pyrevit.coreutils import emoji
from collections import Counter, namedtuple

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application
t = Autodesk.Revit.DB.Transaction(doc)


def collect_current():
    #Collects all elements from current view
    allElementsInView = FilteredElementCollector(doc, doc.ActiveView.Id).ToElements()
    return allElementsInView

def collect_current_ids():
    #Collects all elements from current view
    allElementsIdsInView = FilteredElementCollector(doc, doc.ActiveView.Id).ToElementIds()
    return allElementsIdsInView

def check_param(param_guid):
    spe = FilteredElementCollector(doc).OfClass(SharedParameterElement)
    for s in spe:
        if s.GuidValue.ToString() == param_guid:
            return s
        else:
            pass

#Defy wbs parameter
wbs_param_guid = "8a35d485-8725-484a-9dc7-dd16a4727f3f"
wbs_param = check_param(wbs_param_guid)

#print wbs_param

#Gather the assembly code parameter of the selected elements
wbs_list = []
code_id_list_hide = []
count_code_id_filled = 0
if wbs_param != None:
    for elem in collect_current():
        try:
            if (elem.Category.CategoryType == Autodesk.Revit.DB.CategoryType.Model
                and elem.Category.AllowsBoundParameters == True 
                and elem.Category.Id.ToString() != '-2008043'):
                data = doc.GetElement(elem.Id).get_Parameter(wbs_param.GuidValue).AsString()
                #print (data, '0')
                if data != '' and data != None:
                    # 
                    code_id_list_hide.append(elem.Id)
                elif data == '' or data == None or data == 'None':
                    count_code_id_filled += 1
                    wbs_list.append(elem)
                    # code_list.append('Undefined')
                else:
                    pass
            else:
                pass
        except:
            pass
else:
    pass


def main():
    if __shiftclick__:
        if count_code_id_filled == 0:
            pyrevit.forms.alert("Great! Everything is filled.")
        else:        
            for wbs in wbs_list:
                print(wbs.Name, wbs.Id.ToString(), wbs.Category.Name)


    else:
        hide_list = List[ElementId](code_id_list_hide)
        #print(hide_list, count_code_id_filled)
        if count_code_id_filled == 0:
            pyrevit.forms.alert("Great! Everything is filled.")
        else:
            t.Start("Temp hide")
            doc.ActiveView.HideElementsTemporary(hide_list)
            t.Commit()


if __name__ == '__main__':
    main()