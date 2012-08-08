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
     'description': 'Names of analysis methods for which bash scripts will be created.'
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

def cliner(pars,logger=None):
	my_methods = pars.formatters
	infile = pars.inputfile
	inputfileroot = infile.split(".")[0]
	
	#Get a list of all directories beneath DPLSim/analysisMethods
	allAnalysisMethods,methodNames = DPLSim.analysisMethods.myModList()
	
	#Read in the binary simupop population
	#select the correct cline writing method for each analysis method chosen.  
	filenames = []
	for m in my_methods:
		if m.upper() in methodNames:
 			for a in allAnalysisMethods:
 				if a.name.upper() == m.upper(): 
					if a.hasClineFunction():
						cline_module = a.getClineFunction()
						cline_pars = simuOpt.Params(cline_module.options)
						if not cline_pars.getParam(checkArgs=False):
							sys.exit(1)
						cline_module.clineWriter(cline_pars)
						filenames.append(cline_pars.bashname)
						if logger:
							logger.info("Bash Script to type %s written!" % (a.name))
					else:
						logger.info("Command Line for method %s not supported!" % m)
	return filenames	

short_desc = """
Main function to setup the command line executable scripts for each program.
"""


if __name__ == "__main__":
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()

	pars = simuOpt.Params(options, short_desc)
	
	if not pars.getParam():
		sys.exit(1)
	filenames=cliner(pars,logger)
	print filenames			
	