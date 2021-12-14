# -*- coding: utf-8 -*- 
__doc__ = """
Check the consistency of the BIM Model and retrieves validation report of it's elighment to the EIR. 

Проверяет наполнение информационной модели, а также выдаёт отчёт о соответсвии информационным требованиям EIR заказчика.
"""

#import re
#import os

import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons

clr.AddReference('System')
clr.AddReference('RevitAPIUI')
import pyrevit
from pyrevit import forms
from pyrevit import script
from pyrevit.coreutils import charts
from collections import Counter, namedtuple

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application
t = Autodesk.Revit.DB.Transaction(doc)

# param = namedtuple('ParamAlias', ['name','guid','exists'])


def collect_current():
    #Collects all elements from current view
    allElementsInView = FilteredElementCollector(doc, doc.ActiveView.Id)\
                            .ToElements()
    return allElementsInView

def collect_current_ids():
    #Collects all elements from current view
    allElementsIdsInView = FilteredElementCollector(doc, doc.ActiveView.Id)\
                            .ToElementIds()
    return allElementsIdsInView

def check_param(param_guid):
    spe = FilteredElementCollector(doc).OfClass(SharedParameterElement)
    for s in spe:
        if s.GuidValue.ToString() == param_guid:
            return s
        else:
            pass

#Gather the categories of the selected elements and count them afterwards
cats_list = []
for elem in collect_current():
    try:
        data = elem.Category.Name
        if (elem.Category.CategoryType == Autodesk.Revit.DB.CategoryType.Model
            and elem.Category.AllowsBoundParameters == True 
            and elem.Category.Id.ToString() != '-2008043'):
            #print(elem.Category.Name, elem.Category.CategoryType,
            #       elem.Category.Id.ToString())
            cats_list.append(data)
        else:
            pass
    except:
        pass
        #print(elem.Name)
        #cats_list.append('Undefined')
cats_keys = Counter(cats_list).keys() # equals to list(set(words))
cats_values = Counter(cats_list).values() # counts the elements' frequency

#Gather the assembly code parameter of the selected elements
code_list = []
for elem in collect_current():
    try:
        if (elem.Category.CategoryType == Autodesk.Revit.DB.CategoryType.Model
            and elem.Category.AllowsBoundParameters == True 
            and elem.Category.Id.ToString() != '-2008043'):
            data = doc.GetElement(elem.GetTypeId()).get_Parameter(BuiltInParameter.UNIFORMAT_CODE).AsString()
            if data != '':
                code_list.append(data)
            else:
                #print(elem.Name)
                code_list.append('Undefined')
        else:
            pass
    except:
        pass
code_keys = Counter(code_list).keys() # equals to list(set(words))
code_values = Counter(code_list).values() # counts the elements' frequency

#Defy wbs parameter
wbs_param_guid = "8a35d485-8725-484a-9dc7-dd16a4727f3f"
wbs_param = check_param(wbs_param_guid)

#Gather the wbs parameter of the selected elements
if wbs_param != None:
    wbs_list = []
    for elem in collect_current():
        #print elem
        try:
            if (elem.Category.CategoryType == Autodesk.Revit.DB.CategoryType.Model 
                and elem.Category.AllowsBoundParameters == True 
                and elem.Category.Id.ToString() != '-2008043'):
                data = doc.GetElement(elem.Id).get_Parameter(wbs_param.GuidValue).AsString()
                if data != '':
                    wbs_list.append(data)
                else:
                    wbs_list.append('Undefined')
            else:
                pass
        except:
            pass
    wbs_keys = Counter(wbs_list).keys() # equals to list(set(words))
    wbs_values = Counter(wbs_list).values() # counts the elements' frequency
else:
    pass





def main():
    
    #check_parameter('0')

    #Print the number of all elements displayed in view
    print('Total number of elements in view: {}'.format(collect_current().Count))

    output1 = script.get_output()
    #Draw categories chart
    chr1 = charts.PyRevitOutputChart(output1, chart_type='doughnut', version=None)
    chr1.data.labels = cats_keys
    set_a = chr1.data.new_dataset('set_a')
    set_a.data = cats_values
    chr1.randomize_colors()
    print('Categories of elements in view chart:')
    chr1.draw()


    #Draw assembly code chart
    output2 = script.get_output()
    chr2 = charts.PyRevitOutputChart(output2, chart_type='doughnut', version=None)
    chr2.data.labels = code_keys
    set_b = chr2.data.new_dataset('set_b')
    set_b.data = code_values
    chr2.randomize_colors()  
    print('Assembly code chart:') 
    chr2.draw()


    if wbs_param != None:
        output3 = script.get_output()
        chr3 = charts.PyRevitOutputChart(output3, chart_type='doughnut', version=None)
        chr3.data.labels = wbs_keys
        set_c = chr3.data.new_dataset('set_c')
        set_c.data = wbs_values
        chr3.randomize_colors()
        print('WBS parameter summary for active view:') 
        chr3.draw()
    else:
        print("There is no 'RHI_GN_WBS код' parameter in a project")
        print("В проект не добавлен параметр 'RHI_GN_WBS код'")



if __name__ == '__main__':
    main()