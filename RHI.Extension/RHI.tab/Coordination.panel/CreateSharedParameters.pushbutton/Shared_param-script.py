# -*- coding: utf-8 -*-
# pylint: skip-file
# by Roman Golev 

__doc__ = """
Добавить общие параметры проекта /
Add shared parameters
------------------------------------
Инструмент автоматически добавляет
общие параметры проекта."""

__author__ = "Roman Golev"
__title__ = "Общие\nПараметры"


# Import RevitAPI
import clr
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import System
clr.AddReference('RevitAPIUI')
from Autodesk.Revit import Creation

# Import WPF
clr.AddReference('IronPython.Wpf')
import wpf
from System import Windows
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
import sys

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
uiapp = __revit__
app = uiapp.Application
t = Autodesk.Revit.DB.Transaction(doc)

import os.path as op
from rpw import  DB, UI, db, ui
import pyrevit
from pyrevit import forms
from pyrevit import UI
from pyrevit.forms import WPFWindow
from collections import namedtuple


runtype = []

class MyWindow(WPFWindow):
    def __init__(self,xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
    @property
    def checkbox1(self):
		return self.checkbox1_value.IsChecked
    @property
    def checkbox2(self):
		return self.checkbox2_value.IsChecked
    def click(self, sender, args):
		if self.checkbox1 == True:
			runtype.append(1)
			self.Close()
		elif self.checkbox2 == True:
			runtype.append(2)	
		else:
			forms.alert("You need to select at least one Parameter group")
			sys.exit()
		self.Close()


#def create_shared_param(m_param_option, m_catset, m_parameters, m_group):



	
def run(m_set):
	t.Start("Add RHI Shared parameters")
	#Determining whether the parameters are type or instance
	if m_set.t_param_option:
		bind = app.Create.NewInstanceBinding(m_set.t_catset)
	else : 
		bind = app.Create.NewTypeBinding(m_set.t_catset)
	#Adding the parameters to the project
	bindmap = doc.ParameterBindings
	try:
		for p in m_set.t_parameters:
			#print(p,bind,m_set.t_group)
			bindmap.Insert(p, bind, m_set.t_group)
			t.Commit()
	except:
		t.RollBack()
		#pyrevit.forms.alert("Error")
		return "error"


		


# let's show the window (modal)
MyWindow('ui.xaml').ShowDialog()

#Read shared parameters file
file_location = op.dirname(__file__) + r"\ФОП_RHI.txt"
app.SharedParametersFilename  = file_location
spfile = app.OpenSharedParameterFile()
gr = spfile.Groups

#Categories applied for shared params/ different sets for spicified params
cats1 = [Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DuctTerminal),
	#Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StairsSupports),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_RailingHandRail),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_RailingSupport),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_RailingTermination),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_RailingTopRail),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_RoofSoffit),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_EdgeSlab),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Assemblies),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_CableTrayFitting),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_CableTrayRun),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_CableTray),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Casework),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Ceilings),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Columns),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_ConduitFitting),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_CommunicationDevices),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_ConduitRun),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Conduit),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_CurtaSystem),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_CurtainWallPanels),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_CurtainWallMullions),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DataDevices),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DetailComponents),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Doors),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DuctAccessory),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DuctFitting),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DuctInsulations),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DuctLinings),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DuctSystem),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_ElectricalCircuit),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PlaceHolderDucts),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_DuctCurves),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_ElectricalEquipment),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_ElectricalFixtures),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Entourage),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Fascia),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FireAlarmDevices),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FlexDuctCurves),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FlexPipeCurves),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Floors),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Furniture),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FurnitureSystems),	
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_GenericModel),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_HVAC_Zones),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Gutter),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StairsLandings),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_LightingDevices),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_LightingFixtures),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FabricationContainment),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FabricationDuctwork),	
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FabricationHangers),	
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FabricationPipework),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Mass),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_MechanicalEquipment),
	#Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_MechanicalEquipmentSets),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_NurseCallDevices),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Parts),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Parking),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PipeAccessory),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PipeFitting),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PipeInsulations),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PlaceHolderPipes),
	#Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PipingSystem),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PipeCurves),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Planting),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PlumbingFixtures),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StairsRailing),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Ramps),
	#Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_RebarCover),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_ShaftOpening),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_RebarShape),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Roofs),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Rooms),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Site),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StairsRuns),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_SecurityDevices),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_SpecialityEquipment),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Stairs),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralColumns),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructConnections),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralFoundation),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_AreaRein),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FabricAreas),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_PathRein),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Rebar),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Coupler),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralFraming),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralFramingSystem),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_FabricReinforcement),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralStiffener),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Sprinklers),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_MEPSpaces),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_SwitchSystem),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_TelephoneDevices),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Topography),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralTruss),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Wire),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralTruss),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_StructuralTruss),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Walls),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Windows),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Roads)]
catset1 = app.Create.NewCategorySet()
[catset1.Insert(j) for j in cats1]

cats2 = [Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Walls),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Floors),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Ceilings),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Roofs),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Rooms)]
catset2 = app.Create.NewCategorySet()
[catset2.Insert(i) for i in cats2]

cats3 = [Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Rooms)]
catset3 = app.Create.NewCategorySet()
[catset3.Insert(i) for i in cats3]

cats4 = [Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Walls),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Floors),
	Autodesk.Revit.DB.Category.GetCategory(doc,Autodesk.Revit.DB.BuiltInCategory.OST_Roofs)]
catset4 = app.Create.NewCategorySet()
[catset4.Insert(i) for i in cats4]



defp = [g.Definitions for g in gr]
param = [x for l in defp for x in l]
defflatname = [x.Name for x in param]
grpname = [l.OwnerGroup.Name for l in param]
param_name = [pp.Name for pp in param]

param1 = [param[param_name.index('RHI_GN_WBS код')]]
# param2 = [param[param_name.index('')]]
# param3 = [param[param_name.index('')], \
# 		  param[param_name.index('')], \
# 		  param[param_name.index('')], \
# 		  param[param_name.index('')], \
# 		  param[param_name.index('')], \
# 		  param[param_name.index('')]]
# param4 = [param[param_name.index('')]]
#print(param1[0].GUID)

# №96 — PG_TEXT Group
#Parameter groups
f = System.Enum.GetValues(BuiltInParameterGroup)[97]
try:
	group = [a for a in System.Enum.GetValues(BuiltInParameterGroup) if a == f][0]
except:
	group = [a for a in System.Enum.GetValues(BuiltInParameterGroup) if str(a) == f][0]

param_option = True



#print(param_option, catset, parameters, group)
Set = namedtuple('Param_settings', ['t_param_option','t_catset','t_parameters','t_group'])
param_set1 = Set(t_param_option = param_option, t_catset = catset1, t_parameters = param1, t_group = group)
# param_set2 = Set(t_param_option = param_option, t_catset = catset2, t_parameters = param2, t_group = group)
# param_set3 = Set(t_param_option = param_option, t_catset = catset3, t_parameters = param3, t_group = group)
# param_set4 = Set(t_param_option = False, t_catset = catset4, t_parameters = param4, t_group = group)

if 1 in runtype:
	#print(param_set1)
	run(param_set1)
	#print(1)
# elif 2 in runtype:
# 	run(param_set2)
# elif 3 in runtype:
# 	run(param_set3)
else:
	sys.exit()
	pass