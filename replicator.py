"""
This script will let the user choose the level of replication in the simulation.
The directory structure produced by DPLSim depends on this.

For example, the default setting sets up replication at the level of Genotype Relative Risk.
Five levels are chosen, evenly spaced between GRR = 1.00 and GRR = 2.00

MAF_0.05_1 		#Minor Allele Frequency of 0.05, replicate 1
	GRR_1.00		#Genotype Relative Risk
		rep_1			#First Replicate
			program_1		#First analysis Program
				program_1.bash		#bash script to run program 1
				inputfiles_rep_1	#input files for program 1
				
			program_2		#Second Analysis Program
				program_2.bash
				inputfiles_rep_1
			
			program_3		#Third Analysis Program
				program_3.bash
				inputfiles_rep_1
		rep_2
			program_1
			program_2
			program_3
		.
		.
		.
		rep_n
			program_1
			program_2
			program_3

If the level of replication were at the level of wild type risk instead, the heirarchy
would be adjusted accordingly.

Multiple levels of replication are allowed: for example, testing several levels of GRR 
within a few replicates at the same Minor Allele Frequency.

Replicatior options include:

'MAF'
	minor allele frequency
'GRR'
	genotype relative risk (for the heterozygote)
'WTR'
	wild type risk

Other options will be added as necessary.

"""
import os, errno
import simuOpt
import DPLSim
from DPLSim.analysisMethods import my_import


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise
        
def path_maker(outer,*args):
	"""Takes two levels and creates a directory hierarchy.
	outer
		highest directory name
	arglist
		list of lower directory names."""
	dirpath = "%s/%s" %(outer,"/".join(args))
	mkdir_p(dirpath)
	return dirpath

replicators = [
	{'name':'MAF',
	'label':'Minor Allele Frequency.',
	'default':True,
	'type': bool,
	},
	{'name':'GRR',
	'label':'Genotype Relative Risk.',
	'default':True,
	'type': bool,
	} ,	
# 	{'name':'WTR',
# 	'label':'Wild Type Risk.',
# 	'default':False,
# 	'type': bool,
# 	}
    {'name': 'formatters',
     'default': ['PLINK'],
     'chooseFrom' : [x.split('.')[2].upper() for x in DPLSim.analysisMethods.getAnalysisMethods()],
     'label': 'Formatters\nHold Control to select multiple.',
     'description': 'Names of analysis methods for which input files will be created.'
    }
	]

### A simuOpt options list, one for each type of replicator level.
MAF_options =[
		{'name':'range_hi',
		'default':0.05,
		'label':'Maximum MAF',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'range_lo',
		'default':0.05,
		'label':'Minimum MAF',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'num_steps',
		'default':1,
		'label':'Number of different MAFs',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		{'name':'replicates',
		'default':5,
		'label':'Number of Replicates within each MAF',
		'type':int,
		'validate':simuOpt.valueGE(1)
		}

	]
GRR_options =[
		{'name':'range_hi',
		'default':1,
		'label':'Maximum GRR',
		'type':'number'
		},
		{'name':'range_lo',
		'default':2,
		'label':'Minimum GRR',
		'type':'number',
		'validate':simuOpt.valueGT(0)
		},
		{'name':'num_steps',
		'default':5,
		'label':'Number of different GTRs',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		{'name':'replicates',
		'default':100,
		'label':'Number of Replicates within each GRR',
		'type':int,
		'validate':simuOpt.valueGE(1)
		}
	]
WTR_options=	[
		{'name':'range_hi',
		'default':0.05,
		'label':'Maximum WTR',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'range_lo',
		'default':0.05,
		'label':'Minimum WTR',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'num_steps',
		'default':1,
		'label':'Number of different WTRs',
		'type':int,
		'validate':simuOpt.valueGT(1)
		}
	]


def float_range(low,high,leng):
	"""
	Return a list of evenly spaced floating point numbers, similar to the R function "seq." 
	
	low
		The minimum value
	high
		The maximum value
	leng
		The length of the final list
	"""
	low = float(low)
	high = float(high)
	step = ((high-low) * 1.0 / (leng-1))
	return [low+i*step for i in xrange(leng)]

def dir_setup(logger=None):
	replicator_choice = simuOpt.Params(replicators)
	if not replicator_choice.getParam():
		sys.exit(1)
	
	if replicator_choice.MAF:
		MAF_opt = simuOpt.Params(MAF_options)
		if not MAF_opt.getParam():
			sys.exit(1)
		if MAF_opt.num_steps == 1:
			MAFs = [MAF_opt.range_hi]
		else:
			MAFs = float_range(MAF_opt.range_hi,MAF_opt.range_lo,MAF_opt.num_steps)
		print MAFs
	
	if replicator_choice.GRR:
		GRR_opt = simuOpt.Params(GRR_options)
		if not GRR_opt.getParam():
			sys.exit(1)
		GRRs = float_range(GRR_opt.range_hi,GRR_opt.range_lo,GRR_opt.num_steps)
		print GRRs
	
	dirpaths=[]
	
	if replicator_choice.MAF:
		if replicator_choice.GRR:
			for maf in xrange(len(MAFs)):
				for maf_r in xrange(MAF_opt.replicates):
					maf_dir = "MAF_%.2f_%d" %(MAFs[maf],maf_r+1)
					print maf_dir
					for grr in xrange(len(GRRs)):
						grr_dir = "GRR_%.2f" % GRRs[grr]
						for grr_r in xrange(GRR_opt.replicates):
							rep_dir = "rep_%d" % (grr_r + 1)
							for prog in replicator_choice.formatters:
								prog_dir = prog
								dirpaths.append(path_maker(maf_dir,grr_dir,rep_dir,prog_dir))
	return dirpaths

if __name__ == '__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()
	dirpaths = dir_setup(logger)		
	print dirpaths
	
# 	if replicator_choice.WTR:
# 		WTR_opt = simuOpt.Params(WTR_options)
# 		if not WTR_opt.getParam():
# 			sys.exit(1)
# 		WTRs = float_range(WTR_opt.range_hi,WTR_opt.range_lo,WTR_opt.num_steps)
# 		print WTRs
