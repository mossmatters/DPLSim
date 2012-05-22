import os
import sys
from types import *
import DPLSim
import simuOpt
from DPLSim.analysisMethods import my_import

options = [
    {'name': 'formatters',
     'default': ['PLINK'],
     'chooseFrom' : [x.split('.')[2].upper() for x in DPLSim.analysisMethods.getAnalysisMethods()],
     'label': 'Formatters\nHold Control to select multiple.',
     'description': 'Names of analysis methods for which input files will be created.'
    },
    {'name': 'inputfile',
     'default': 'rep_1.pop',
     'useDefault' : True,
     'label': 'simuPOP Population',
     'allowedTypes': StringType,
     'validate': simuOpt.valueValidFile(),
     'description': 'A simupop population file to parse and format.'
    }
    ]

def format(pars,logger=None):
	my_methods = pars.formatters
	infile = pars.inputfile
	inputfileroot = infile.split(".")[0]
	
	#Get a list of all directories beneath DPLSim/analysisMethods
	allAnalysisMethods,methodNames = DPLSim.analysisMethods.myModList()
	
	#Read in the binary simupop population
	inputMethodName=	'DPLSim.analysisMethods.simupop.input'
	inputmethod = my_import(inputMethodName)
	pop = inputmethod.inRead(infile)
	if logger:
		logger.info("Loading %s file %s successful!" %(inputMethodName.split('.')[2],infile))
	
	
	#select the correct parsing method for each analysis method chosen.  
	filenames = []
	for m in my_methods:
		if m.upper() in methodNames:
 			for a in allAnalysisMethods:
 				if a.name.upper() == m.upper(): 
					if a.hasFormatFunction():
					
						filenames.append(a.formatter.createFiles(pop,inputfileroot))
						if logger:
							logger.info("Formatting to type %s done!" % a.name)
					else:
						logger.info("Parsing for method %s not supported!" % m)
	return filenames	

short_desc = """
Main formatting function to parse simuPOP population file and output the files necessary
To run one or more analysis methods.
"""


if __name__ == "__main__":
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()

	pars = simuOpt.Params(options, short_desc)
	
	if not pars.getParam():
		sys.exit(1)
	filenames=format(pars,logger)
	print filenames			
	