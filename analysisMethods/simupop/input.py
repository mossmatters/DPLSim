"""Requires the simuPOP module be installed in the python path. Imports the results of a sampled population using the simuPOP methods."""


import simuOpt as inputsimuOpt
inputsimuOpt.setOptions(quiet=True)
import simuPOP as inputsimuPop

def inRead(filename):
	"""
	Reads a binary file containing a population in simuPOP format.
	Returns the population as a simuPOP object.
	"""
	pop = inputsimuPop.loadPopulation(filename)
	return pop
	