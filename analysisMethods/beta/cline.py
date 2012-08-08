"""
Generate a bash script for running Margarita from the command line with various options.

The options are stored as a simuPOP.simuOpt option class, and uses its verification system.

"""
import sys,os
import simuOpt
from types import *

options = [
	{'name': 'haplofile',
     'default': 'Beta_haplotypes_2_rep_1.txt',
     'label': 'Phased Haplotype File.',
     'type': 'filename',
     'description': 'Text file in Beta format.'
    },
    {'name': 'posfile',
     'default': 'Beta_positions_2_rep_1.txt',
     'label': 'Positions File',
     'description': '''List of integers representing marker locations''',
     'type': 'filename'
    },
	{'name': 'statusfile',
     'default': 'Beta_status_2_rep_1.txt',
     'label': 'Disease Status File',
     'type': 'filename',
     'description': 'List of 0 and 1 for disease status in same order as haplofile.'
    },
    {'name': 'resultsfilename',
     'default': 'Beta_2_rep_1.scores',
     'label': 'Name of Results File.',
     'type': 'string',
     'description': 'Results file contains only the raw Bayes factor for each marker.'
    },
    {'name': 'logfile',
    'default':'Beta_2_rep_1.log',
    'label': "Log file with all output from BETA",
    'type': 'string'
    },
    {'name': 'rootpath',
     'default': "~/Desktop/Python/DPLSim_develop/",
     'label': 'Directory for temporary files.',
     'description': 'BETA creates many temporary files with genetree.'
    },
    {'name': 'bashname',
    'default': 'rep_1_beta.bash',
    'type':'string',
    'label': "Name for the bash script.",
	'description': "Name of a file to save the bash script to run BETA."
    },
    {'name':"betaLoc",
    'default':'~/bin/BETA_RUN.r',
    'type':'filename',
    'label': 'Path to BETA_RUN.r'
    },
    {'name':"cleanup",
    'default':True,
    'type':BooleanType,
    "description":"""If true, will delete the input files and most of the outputfiles upon completion. Saves only the Bayes factors."""
    },
    {'name':'dirname',
    "default": "."
    "description":"Path where bash script will be created"
    }
	]
	
def clineWriter(pars):
	bashfile = open(os.path.join(pars.dirname,pars.bashname,'w')
	bashfile.write("#/bin/bash\n")

	bashfile.write("Rscript %s %s %s %s %s %s >%s\n" %(pars.betaLoc,pars.haplofile,pars.posfile,pars.statusfile,pars.resultsfilename,pars.rootpath,pars.logfile))

	if pars.cleanup:
		bashfile.write("rm %s\n" %pars.haplofile)
		bashfile.write("rm %s\n" %pars.posfile)
		bashfile.write("rm %s\n" %pars.statusfile)
	
	bashfile.close()	
	os.chmod(pars.bashname,0755)
	return
	
short_desc = "This script sets up a command line bash script for BETA"
	
if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()
	
	pars = simuOpt.Params(options,short_desc)
	if not pars.getParam():
		sys.exit(1)
	clineWriter(pars)
	