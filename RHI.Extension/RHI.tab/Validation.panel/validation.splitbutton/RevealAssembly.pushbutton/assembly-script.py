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

__title__ = "Check\nAssembly Code"

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

#Gather the assembly code parameter of the selected elements
code_list = []
code_id_list_hide = []
count_code_id_filled = 0
for elem in collect_current():
    try:
        if (elem.Category.CategoryType == Autodesk.Revit.DB.CategoryType.Model
            and elem.Category.AllowsBoundParameters == True 
            and elem.Category.Id.ToString() != '-2008043'):
            data = doc.GetElement(elem.GetTypeId()).get_Parameter(BuiltInParameter.UNIFORMAT_CODE).AsString()
            if data != '':
                # 
                code_id_list_hide.append(elem.Id)
            elif data == '':
                count_code_id_filled += 1
                code_list.append(elem)
                # code_list.append('Undefined')
            else:
                pass
        else:
            pass
    except:
        pass


def main():
    if __shiftclick__:
        if count_code_id_filled == 0:
            pyrevit.forms.alert("Great! Everything is filled.")
        else:        
            for code in code_list:
                print(code.Name, code.Id.ToString(), code.Category.Name)


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