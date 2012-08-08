"""
Generate a bash script for running Blossoc from the command line with various options.

The options are stored as a simuPOP.simuOpt option class, and uses its verification system.

"""
import sys,os
import simuOpt
from types import *

options = [
	{'name': 'genotypefile',
     'default': 'Blossoc_genotypes_2_rep_1.txt',
     'label': 'Name of genotypes file in Blossoc format.',
     'type': 'filename',
     'description': 'Text file for Blossoc: One haplotype per line, disease status in first column, followed by SNPs.'
    },
    {'name': 'positionsfile',
     'default': 'Blossoc_positions_2_rep_1.txt',
     'label': 'Name of positions file in Blossoc format.',
     'type': 'filename',
     'description': 'Text file for Blossoc: List of positions in floating point format (trailing .0) on a single line.'
    },
    {'name': 'scoreFunction',
     'default': 'H',
     'label': 'Blossoc score function',
     'description': '''
     H = HQC
     B = BIC
     A = AIC
     G = Gini
     S = SMA
     P = Probability
     X = eXperimental genotype likelihood score
     In Blossoc the default is H if haplotypes > 400, otherwise P     
     ''',
     'type': ('chooseOneOf',['H','B','A','G','S','P','X'])
    },
	{'name': 'permutations',
	 'default': 0,
     'label': 'Number of Permutations',
     'type': 'integer',
     'description': 'Permutation tests in Blossoc'
    },
    {'name': 'unphased',
     'default': False,
     'label': 'Unphased?',
     'type': BooleanType,
     'description': 'Blossoc accepts unphased data (-u1) by default. Data from simuPOP is phased.'
    },
    {'name': 'outputfilename',
    'default':'scores.txt',
    'label': "Output file name from Blossoc",
    'type': 'string',
    'description': "Blossoc outputs one file with the scores on a single line."
    },
    {'name':"cleanup",
    'default':True,
    'type':BooleanType,
    "description":"""If true, will delete the input files upon completion. Saves only the scores."""
    },
    {'name': 'bashname',
    'default': 'rep_1_blossoc.bash',
    'type':'string',
    'label': "Name for the bash script.",
	'description': "Name of a file to save the bash script to run Blossoc."
    } ,
    {'name':'dirname',
    "default": "."
    "description":"Path where bash script will be created"
    }
	]
	
def clineWriter(pars):
	bashfile = open(os.path.join(pars.dirname,pars.bashname,'w')
	bashfile.write("#/bin/bash\n")
	if pars.unphased:
		bashfile.write("blossoc %s %s -o %s\n" % (pars.positionsfile,pars.genotypefile,pars.outputfilename))
	else:
		bashfile.write("blossoc -u0 %s %s -o %s\n" % (pars.positionsfile,pars.genotypefile,pars.outputfilename))
	
	if pars.cleanup:
		bashfile.write("rm %s\n" % pars.positionsfile)
		bashfile.write("rm %s\n" % pars.genotypefile)

	bashfile.close()
	os.chmod(pars.bashname,0755)
	return
	
short_desc = "This script sets up a command line bash script for Blossoc"
	
if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()
	
	pars = simuOpt.Params(options,short_desc)
	if not pars.getParam():
		sys.exit(1)
	clineWriter(pars)
	