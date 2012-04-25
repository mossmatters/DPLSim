"""
Generate a bash script for running Margarita from the command line with various options.

The options are stored as a simuPOP.simuOpt option class, and uses its verification system.

"""
import sys
import simuOpt
from types import *

options = [
	{'name': 'inputfiles',
     'default': 'Margarita_rep_1.pop',
     'label': 'Name of input file in Margarita format.',
     'type': 'filenames',
     'description': 'Text file in Margarita format.'
    },
    {'name': 'memory',
     'default': 1024,
     'label': 'How many MB of RAM?',
     'description': '''Sets the -Xmx parameter in java for Margarita''',
     'type': 'integer'
    },
	{'name': 'permutations',
     'default': 1000,
     'label': 'Number of Permutations',
     'type': 'integer',
     'description': 'Permutation tests in Margarita'
    },
    {'name': 'numArgs',
     'default': 30,
     'label': 'Number of ARGs to infer.',
     'type': 'integer',
     'description': 'How many Ancestral Recombination Graphs to infer in Margarita'
    },
    {'name': 'smartPerm',
    'default':True,
    'label': "Perform Smart Permutations?",
    'type': BooleanType
    },
    {'name': 'numSmart',
     'default': 100,
     'label': 'Give up after how many permutations?',
     'type': 'integer',
     'description': 'Smart Permutations will give up if the first N permutations exceed observed.'
    },
    {'name': 'bashname',
    'default': 'rep1.bash',
    'type':'string',
    'label': "Name for the bash script.",
	'description': "Name of a file to save the bash script to run Margarita."
    },
    {'name':"betaLoc",
    'default':'~/bin/margarita.jar',
    'type':'filename',
    'label': 'Path to BETA_RUN.r'
    }
	]
	
def clineWriter(pars):
	bashfile = open(pars.bashname,'w')
	bashfile.write("#/bin/bash\n")
	if pars.smartPerm:
		bashfile.write("java -Xmx%d -jar %s %s %d %d --smart %d" % (pars.memory,pars.margaritaLoc,pars.inputfile,pars.numArgs,pars.permutations,pars.numSmart))
		bashfile.close()
		return
	else:
		bashfile.write("java -Xmx%d -jar %s %s %d %d" % (pars.memory,pars.margaritaLoc,pars.inputfile,pars.numArgs,pars.permutations))
		bashfile.close()
		return

short_desc = "This script sets up a command line for TreeDT"
	
if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()
	
	pars = simuOpt.Params(options,short_desc)
	if not pars.getParam():
		sys.exit(1)
	clineWriter(pars)
	