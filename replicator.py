"""
This script will let the user choose the level of replication in the simulation.
Although the directory structure is set, the user may choose the level of gridding
At each of the levels: Minor Allele Frequency, Number of Controls, Wild Type Risk,
and Genotype Relative Risk.

For example, the default setting sets up replication only at the level of Genotype Relative Risk.
Five levels are chosen, evenly spaced between GRR = 1.00 and GRR = 2.00

MAF_0.05_1 		#Minor Allele Frequency of 0.05, replicate 1
	CC_1000_1	#1000 Controls in each dataset, replicate 1
		WTR_0.05_1		#Wild Type Risk = 0.05, replicate 1
		GRR_1.00_1		#Genotype Relative Risk, first replicate
			
			program_1		#First analysis Program
			program_2		#Second Analysis Program
			program_3		#Third Analysis Program

		GRR_1.00_2
			program_1
			program_2
			program_3
		.
		.
		.
		GRR_1.00_100
			program_1
			program_2
			program_3

		GRR_1.25_1			# Next level of GRR
			program_1
			program_2
			program_3
			

Multiple levels of replication are allowed: for example, testing several levels of GRR 
within a few replicates at the same Minor Allele Frequency.

Replicatior options include:

'MAF'
	final minor allele frequency
'CC'
	Number of Control individuals in sample datasets
'WTR'
	wild type risk

'GRR'
	genotype relative risk (for the heterozygote)

"""
import os, errno,sys
import simuOpt
import DPLSim
from DPLSim.analysisMethods import my_import
from DPLSim import singleGeneModel


def mkdir_p(path):
	try:
		os.makedirs(path)
		return 1
	except OSError as exc: # Python >2.5
		if exc.errno == errno.EEXIST:
			pass
			return 0
		else: raise
		
def path_maker(outer,*args):
	"""Takes multiple levels and creates a directory hierarchy.
	outer
		highest directory name
	arglist
		list of lower directory names."""
	dirpath = "%s/%s" %(outer,"/".join(args))
	return dirpath

replicator_options = [
		{'separator':'Minor Allele Frequency'},
		{'name':'MAF_range_hi',
		'default':0.05,
		'label':'Maximum MAF',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'MAF_range_lo',
		'default':0.05,
		'label':'Minimum MAF',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'MAF_num_steps',
		'default':1,
		'label':'Number of MAF levels',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		{'name':'MAF_replicates',
		'default':1,
		'label':'Replicates within each MAF',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		
		{'separator':"Number of Controls"},
		{'name':'CC_range_hi',
		'default':1000,
		'label':'Max # Controls',
		'type':int,
		'validate':simuOpt.valueGE(100)
		},
		{'name':'CC_range_lo',
		'default':1000,
		'label':'Min # Controls',
		'type':int,
		'validate':simuOpt.valueGE(100)
		},
		{'name':'CC_num_steps',
		'default':1,
		'label':'Number Control Levels',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		{'name':'CC_replicates',
		'default':1,
		'label':'Replicates within each # Control',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		
		{'separator':"Wild Type Risk"},
		{'name':'WTR_range_hi',
		'default':0.05,
		'label':'Maximum WTR',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'WTR_range_lo',
		'default':0.05,
		'label':'Minimum WTR',
		'type':'number',
		'validate':simuOpt.valueBetween(0,1)
		},
		{'name':'WTR_num_steps',
		'default':1,
		'label':'Number WTR levels',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		{'name':'WTR_replicates',
		'default':1,
		'label':'Replicates within each WTR',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},

		{'separator':"Genotype Relative Risk"},
		{'name':'GRR_range_hi',
		'default':2,
		'label':'Maximum GRR',
		'type':'number'
		},
		{'name':'GRR_range_lo',
		'default':1,
		'label':'Minimum GRR',
		'type':'number',
		'validate':simuOpt.valueGT(0)
		},
		{'name':'GRR_num_steps',
		'default':5,
		'label':'Number of GRR levels',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},
		{'name':'GRR_replicates',
		'default':100,
		'label':'Replicates within each GRR',
		'type':int,
		'validate':simuOpt.valueGE(1)
		},

	{'name': 'formatters',
	 'default': ['PLINK'],
	 'chooseFrom' : [x.split('.')[2].upper() for x in DPLSim.analysisMethods.getAnalysisMethods()],
	 'label': 'Formatters\nHold Control to select multiple.',
	 'description': 'Names of analysis methods for which input files will be created.'
	},
	{'name':'createDirs',
	'default':True,
	'type':bool,
	'label':"Create Directories Here and Now?"
	}
	]

short_desc = """
Set up the directory hierarchy for replication and gridding of parameters.
"""

### A simuOpt options list, one for each type of replicator level.
def float_range(low,high,leng, logger=None):
	"""
	Return a list of evenly spaced floating point numbers, similar to the R function "seq." 
	
	low
		The minimum value
	high
		The maximum value
	leng
		The length of the final list
	"""
	if leng == 1:
		if low != high:
			if logger:	
				logger.info("Steps = 1, but low not equal to high. Using high value!")
		return [float(high)]
	
	else:
		low = float(low)
		high = float(high)
		step = ((high-low) * 1.0 / (leng-1))
		return [low+i*step for i in xrange(leng)]

def dir_path_gen(rep_opt,logger=None):
	"""Iterate through the gridding levels to create directory paths"""
	dirpaths = []
	for maf in xrange(len(rep_opt.MAFs)):
		for maf_rep in xrange(rep_opt.MAF_replicates):
			maf_dir = "MAF_%.2f_%d" %(rep_opt.MAFs[maf],maf_rep+1)
			for cc in xrange(len(rep_opt.CCs)):
				for cc_rep in xrange(rep_opt.CC_replicates):
					cc_dir = "cc_%d_%d" % (rep_opt.CCs[cc],cc_rep+1)
					for wtr in xrange(len(rep_opt.WTRs)):
						for wtr_rep in xrange(rep_opt.WTR_replicates):
							wtr_dir = "WTR_%.2f_%d" % (rep_opt.WTRs[wtr],wtr_rep+1)
							for grr in xrange(len(rep_opt.GRRs)):
								for grr_rep in xrange(rep_opt.GRR_replicates):
									grr_dir = "GRR_%.2f_%d" % (rep_opt.GRRs[grr],grr_rep+1)
									for prog in rep_opt.formatters:
										prog_dir = prog
										dirpaths.append(path_maker(maf_dir,cc_dir,wtr_dir,grr_dir,prog_dir))
	return dirpaths

def dir_setup(rep_opt,logger=None):
	"""
	Set up the Directory hierarchy with the gridding and replication specified in rep_opt.
	"""

	
	rep_opt.MAFs = float_range(rep_opt.MAF_range_hi,rep_opt.MAF_range_lo,rep_opt.MAF_num_steps,logger)
	rep_opt.CCs  = float_range(rep_opt.CC_range_hi,rep_opt.CC_range_lo,rep_opt.CC_num_steps,logger)
	rep_opt.GRRs = float_range(rep_opt.GRR_range_hi,rep_opt.GRR_range_lo,rep_opt.GRR_num_steps,logger)
	rep_opt.WTRs = float_range(rep_opt.WTR_range_hi,rep_opt.WTR_range_lo,rep_opt.WTR_num_steps,logger)
	
	if logger:
		logger.info("Creating directories with the following parameters:")
		for key in sorted(rep_opt.asDict().iterkeys()):
			logger.info("%s = %s" %(key,rep_opt.asDict()[key]))		
		logger.info("Minor Allele Frequencies: " + ",".join(repr(x) for x in rep_opt.MAFs))
		logger.info("Controls: " + ",".join(repr(x) for x in rep_opt.CCs))
		logger.info("Wild Type Risks: " + ",".join(repr(x) for x in rep_opt.WTRs))
		logger.info("Genotype Relative Risks: " + ",".join(repr(x) for x in rep_opt.GRRs))

	dirpaths = dir_path_gen(rep_opt,logger)	
	num_created = 0
	for d in dirpaths:
		num_created += mkdir_p(d)	
	logger.info("Created %d new directories" % num_created)									
	return dirpaths

def rep_bash(dirpaths,logger=None,**kwargs):
	"""
	Given the list of dirpaths in the replicates, parse out the program name and send
	the parameters along to cline_writer.py.
	"""
	for d in dirpaths:
		program = os.split.path(d)[0]
		kwargs['dirpath'] = d
		kwargs['formatters'] = program
		cline_filenames = get_cline(logger,**kwargs)
	
def rep_case_control(rep_opt,logger=None):
	"""Given the gridding scheme options, create simuPOP files in the given subdirectories."""	
	simuOpt.setOptions(alleleType='binary', optimized=True)
	from simuPOP import *

	cc_opt = simuOpt.Params(singleGeneModel.options)
	
	for maf in xrange(len(rep_opt.MAFs)):
		for maf_rep in xrange(rep_opt.MAF_replicates):
			
			maf_dir = "MAF_%.2f_%d" %(rep_opt.MAFs[maf],maf_rep+1)
			cc_opt.expandPop = "%s/%s.pop" % (maf_dir,maf_dir)
			cc_opt.pop = 	loadPopulation(cc_opt.expandPop)
			logger.info("Expanded population %s loaded!" %cc_opt.expandPop)

			for cc in xrange(len(rep_opt.CCs)):
				for cc_rep in xrange(rep_opt.CC_replicates):
					cc_dir = "cc_%d_%d" % (rep_opt.CCs[cc],cc_rep+1)
					for wtr in xrange(len(rep_opt.WTRs)):
						for wtr_rep in xrange(rep_opt.WTR_replicates):
							wtr_dir = "WTR_%.2f_%d" % (rep_opt.WTRs[wtr],wtr_rep+1)
							for grr in xrange(len(rep_opt.GRRs)):
								for grr_rep in xrange(rep_opt.GRR_replicates):
									grr_dir = "GRR_%.2f_%d" % (rep_opt.GRRs[grr],grr_rep+1)
									
									dirpath = path_maker(maf_dir,cc_dir,wtr_dir,grr_dir)
									
									cc_opt.wtr = rep_opt.WTRs[wtr]
									cc_opt.GRR = rep_opt.GRRs[grr]
									cc_opt.numControls= rep_opt.CCs[cc]
									cc_opt.sampledPop = os.path.join(dirpath,"sample.pop")
									pop = singleGeneModel.penetrance(cc_opt,logger)
									case_control_dataset.save(pars.sampledPop)
									logger.info("Sampled population saved at %s" %pars.sampledPop)
									
										

if __name__ == '__main__':
	import logging
	logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.DEBUG)
	logger = logging.getLogger()
	
	rep_opt = simuOpt.Params(replicator_options)
	if not rep_opt.getParam():
		sys.exit(1)
	
	dirpaths = dir_setup(logger)#,formatters=['PLINK',"BLOSSOC","TREEDT","MARGARITA","BETA"])		
	#print dirpaths
	