"""
Generate a bash script for running TreeDT from the command line with various options.

The options are stored as a simuPOP.simuOpt option class, and uses its verification system.

"""
import sys
import simuOpt
from types import *

options = [
	{'name': 'inputfile',
     'default': 'TreeDT_rep_1.pop',
     'label': 'Name of input file in TreeDT format.',
     'type': 'filename',
     'description': 'Text file in TreeDT format.'
    },
    {'name': 'method',
     'default': 'p',
     'label': 'Which method to run TreeDT?',
     'description': '''TreeDT can run in five modes: 
     		s = file check mode
     		p = permutation test mode (default)
     		P = permutation test and correct location
     		k = permutation test with fixed number of subtrees
     		K = permutation test with fixed number of subtrees and correct location''',
     'type': ('chooseOneOf',['s','p','P','k','K'])
    },
	{'name': 'permutations',
     'default': 1000,
     'label': 'Number of Permutations',
     'type': 'int',
     'description': 'Permutation tests in TreeDT'
    },
    {'name': 'correctLoc',
     'default': 0,
     'label': 'Correct location (for P and K only)',
     'type': 'int',
     'description': 'Correct DPL for .'
    },
    {'name': 'fixedTrees',
    'default':0,
    'label': "Number of Fixed Subtrees (for k and K only)",
    'type': 'int'        },
    {'name': 'bashname',
    'default': 'rep1.bash',
    'type':'string',
    'label': "Name for the bash script.",
	'description': "Name of a file to save the bash script to run PLINK."
    }
	]
	
def clineWriter(pars):
	bashfile = open(pars.bashname,'w')
	bashfile.write("#/bin/bash\n")

	if pars.method == 's':
		bashfile.write("treedt s %s" % pars.inputfile)
		bashfile.close()
		return
	elif pars.method == 'p':
		bashfile.write("treedt p %s %d" % (pars.inputfile,pars.permutations))
		bashfile.close()
		return
	elif pars.method == 'P':
		bashfile.write("treedt p %s %d %d" % (pars.inputfile,pars.permutations,pars.correctLoc))
		bashfile.close()
		return
	elif pars.method == 'k':
		bashfile.write("treedt p %s %d %d" % (pars.inputfile,pars.permutations,pars.fixedTrees))
		bashfile.close()
		return
	elif pars.method == 'K':
		bashfile.write("treedt p %s %d %d %d" % (pars.inputfile,pars.permutations,pars.correctLoc,pars.fixedTrees))
		bashfile.close()
		return
	else:
		print "Method %s not supported!" % pars.method
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
	