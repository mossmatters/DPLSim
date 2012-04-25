"""
DPLSim: A Full Disease Gene Mapping Pipeline

1. Simupop simulation using human genome as starting point.
	a. initial population from Hapmap data
		loadHapMap3.py
		selectMarkers.py
		-select hapmap populations
		-select chromosomes (by name)
		-select markers (number of markers + start, range, list of SNPs)
	b. expand population under selection
		-names of markers under selection
		-selection regime
	c. generate case/control datasets using a penetrance model
		-penetrance.py
		single gene
			alleles additive or multiplicative?
		multiple Gene
			genes and alleles additive/multiplicative?
		wild type risk?
		relative risk?
		number of cases
		number of controls
	d. remove monomorphic markers (and DPL?) from datasets
		remove_rare_snps.py
		remove_DPL.py
		
2. Generation of input datafiles for various disease mapping programs.
	a. simupop_formatr.py
		- names of programs
	b. marg_split.py (makes sliding windows)
	
3. Generation of script files for running programs on SGE cluster.
	a. program-specific options (number of ARGs, number of permutations, etc)
	b. SGE options (memory, number of machines)
	c. is it to be run as an "array"?
		program-specific array intstructions

4. Generation of script files for collecting results.
	a. based on the programs run: need to stitch windows back together?
	
5. Generation of pipeline-run INSTRUCTIONS.
"""

import DPLSim
from DPLSim.analysisMethods import my_import

class AnalysisMethod(object):
	"""
	Initialize the AnalysisMethod class, with functions used by each analysis method.
	
	Each analysis method should have its own ProgramInfo class which inherits from AnalysisMethod.
	The ProgramInfo class will specify data members such as name and format as those functions become available for that analysis method.
	
	self.name -- The name of the analysis method. Used to load a ProgramInfo module dynamically.
	self.format -- If true, DPLSim can format into the input files for this analysis method. (a formatter is available)
	self.cline -- If true, DPLSim can create a bash script executing one or more runs of an analysis method.
	self.input -- If true, DPLSim can parse a file in this format into a simuPOP population object.
	
	getFormatter(self) -- Return a dynamically loaded ProgramInfo object for that analysis method.
	getName(self)-- Return the self.name of a ProgramInfo object.
	hasFormatFunction(self) -- Checks that self.format=True for a ProgramInfo object.
	hasInputFunction(self) -- Checks that self.input=True for a ProgramInfo object.
	"""
	
	def __init__(self):
		"""Initialize parameters for a base AnalysisMethod object"""
		self.name=None
		self.format=False
		self.cline=False
		self.cluster=False
		self.input=False
	
	def getFormatter(self):
		"""
		Get the formatting function for an analysis method, if available. 
		Uses the dynamic import function to return the formatter as a variable. 
		"""
		if self.format:
			print "importing formatter!"
			return my_import("DPLSim.analysisMethods.%s.formatter"%self.name.lower())
		else:
			print "not importing formatter!"
			
	def getName(self):
		"""Return the analysis method name of an AnalysisMethod object."""
		return self.name
	
	def hasFormatFunction(self):
		"""Determine whether DPL Sim supports parsing populations into input files of a specific analysis method."""
		try:
			return self.format
		except AttributeError:
			return False

	def hasInputFunction(self):
		"""Determine whether an analysis method can be imported into DPLSim."""
		try:
			return self.input
		except AttributeError:
			return False
	
	def hasClineFunction(self):
		"""Determine whether the creation of bash scripts is supported for this analysis method"""
		try:
			return self.cline
		except AttributeError:
			return False
	def getClineFunction(self):
		"""
		Get the cline function for an analysis method, if available.
		Uses the dynamic import function to return the cline function as a variable.
		"""
		if self.cline:
			return my_import("DPLSim.analysisMethods.%s.cline"%self.name.lower())