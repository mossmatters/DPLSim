"""
Upon importing, searches for all analysis programs and imports them too.
"""
import os
import DPLSim

am_path = os.path.join(DPLSim.__path__[0],'AnalysisMethods')

def getAnalysisMethods():
	"""Return a list of analysis methods that can be loaded."""
	return ["DPLSim.analysisMethods.%s"%(x) for x in os.listdir(am_path) if os.path.isdir(os.path.join(am_path,x)) and os.path.isfile(os.path.join(am_path,x,"formatter.py"))] 
	 
def getModuleList(methodNames):
	"""Given a list of analysis method names, return a list of loaded modules."""
	modList = [my_import(modName) for modName in methodNames]
	return modList

def my_import(name):
	"""Dynamically import a python module with multiple periods, such as DPLSim.AnalysisMethods.blossoc.formatter.
	Necessary because __import__(name) returns the highest level name (DPLSim)."""
	mod = __import__(name)
	components = name.split('.')
	for comp in components[1:]:
		mod = getattr(mod,comp)
	return mod

def myModList(returnNames = True,returnMethods = True):
	"""
	By Default, return two lists:
	1) list of ProgramInfo objects containing all available analysis methods
	2) list containing the names of all those methods
	"""
	modNames = getAnalysisMethods()
	modList = getModuleList(modNames)
	allAnalysisMethods = [mod.ProgramInfo() for mod in modList]
	methodNames = [a.getName() for a in allAnalysisMethods]
	if returnNames and returnMethods:
		return allAnalysisMethods,methodNames