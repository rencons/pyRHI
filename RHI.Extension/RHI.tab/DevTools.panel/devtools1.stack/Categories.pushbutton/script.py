# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev


__doc__ = "test"
__author__ = 'Roman Golev'
__title__ = "Categories\n List + ID"


import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

clr.AddReference('System')
clr.AddReference('RevitAPIUI')
import pyrevit
from pyrevit import forms
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application
t = Autodesk.Revit.DB.Transaction(doc)


categories = doc.Settings.Categories
n = categories.Size
print(n)

for c in categories:
    #print (c.Name, c.Id.IntegerValue, c.SubCategories.Size, c.CategoryType, c.AllowsBoundParameters )
    if c.SubCategories.Size != 0:
        print(c.SubCategories, c.SubCategories.Size)
        for i in c.SubCategories:
            print i.SubCategories.ForwardIterator()
