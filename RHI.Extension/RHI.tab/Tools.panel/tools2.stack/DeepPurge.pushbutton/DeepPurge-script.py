# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev

__doc__ = """Purges all unused elements from project
-----------------------------------
Удаляет все неиспользуемые элементы модели
"""
__author__ = 'Roman Golev'
__title__ = "Quad\nPurge"

#https://forums.autodesk.com/t5/revit-api-forum/purge-unused-via-the-api/td-p/6431564
#https://forums.autodesk.com/t5/revit-api-forum/how-to-call-revit-purge-button-from-the-api/td-p/7522679
#https://forums.autodesk.com/t5/revit-ideas/purge-unused-revit-api/idi-p/7556266

import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit import DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import System
clr.AddReference('RevitAPIUI')
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application
t = Autodesk.Revit.DB.Transaction(doc)

def get_unused():
    purgeGuid = 'e8c63650-70b7-435a-9010-ec97660c1bda'
    purgableElementIds = []
    performanceAdviser = DB.PerformanceAdviser.GetPerformanceAdviser()
    guid = System.Guid(purgeGuid)
    ruleId = None
    allRuleIds = performanceAdviser.GetAllRuleIds()
    for rule in allRuleIds:
        # Finds the PerformanceAdviserRuleId for the purge command
        if str(rule.Guid) == purgeGuid:
            ruleId = rule
    ruleIds = List[DB.PerformanceAdviserRuleId]([ruleId])
    print(ruleId)
    for i in range(4):
        # Executes the purge
        failureMessages = performanceAdviser.ExecuteRules(doc, ruleIds)
        if failureMessages.Count > 0:
            # Retreives the elements
            purgableElementIds = failureMessages[0].GetFailingElements()
    return purgableElementIds

# Deletes the elements
elems1 = get_unused()
t.Start("Purge unused")
try:
    doc.Delete(elems1)
except:
    for e in elems1:
        try:
            doc.Delete(e)
        except:
            t.RollBack()
            print('error')
            pass
elems2 = get_unused()
try:
    doc.Delete(elems2)
except:
    for e in elems2:
        try:
            doc.Delete(e)
        except:
            t.RollBack()
            print('error')
            pass
t.Commit()
