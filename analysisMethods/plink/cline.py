"""
Generate a bash script for running PLINK from the command line with various options.

The options are stored as a simuPOP.simuOpt option class, and uses its verification system.

"""
import sys
import simuOpt
from types import *

options = [
	{'name': 'filestem',
     'default': 'rep_1',
     'label': 'Input file stem for .ped and .map files.',
     'type': 'string',
     'description': 'The base name of the two files required by PLINK: a pedigree file (.ped) and a map file (.map).',
     'validate': simuOpt.valueNotEqual('')
    },
    {'name': 'outfilestem',
     'default': 'rep_1',
     'label': 'Output filestem name for .assoc file.',
     'type': 'string',
     'description': 'An initial population created using script selectedMarkers.py',
     'validate': simuOpt.valueNotEqual('')
    },
	{'name': 'assoc',
     'default': True,
     'label': 'Find Association',
     'type': 'bool',
     'description': 'Use the --assoc flag in PLINK.'
    },
    {'name': 'noweb',
     'default': True,
     'label': 'Turn update check off',
     'type': 'bool',
     'description': 'Use --noweb flag in PLINK, suppressing the update check.'
    },
    {'name': 'bashname',
    'default': 'rep_1.bash',
    'type':'string',
    'label': "Name for the bash script.",
	'description': "Name of a file to save the bash script to run PLINK.",
	'validate': simuOpt.valueNotEqual('')
    }
	]
	
def clineWriter(pars):
	if pars.assoc:
		a = "--assoc"
	else:
		a = ""
	if pars.noweb:
		n = "--noweb"
	else:
		n = ""
	bashfile = open(pars.bashname,'w')
	bashfile.write("#/bin/bash\n")
	bashfile.write("plink --file %s --out %s %s %s\n" % (pars.filestem,pars.outfilestem,a,n))
	bashfile.close()

short_desc = "This script sets up a command line for PLINK"
	
if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()
	
	pars = simuOpt.Params(options,short_desc)
	if not pars.getParam():
		sys.exit(1)
	clineWriter(pars)
	