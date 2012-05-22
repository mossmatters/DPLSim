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
import simuOpt

replicators = [
	{'name':'MAF',
	'label':'Minor Allele Frequency.',
	'default':False,
	'type': bool,
	},
	{'name':'GRR',
	'label':'Genotype Relative Risk.',
	'default':True,
	'type': bool,
	},	
	{'name':'WTR',
	'label':'Wild Type Risk.',
	'default':False,
	'type': bool,
	},
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
		'validate':simuOpt.valueGT(1)
		}
	]
GRR_options =[
		{'name':'range_hi',
		'default':1,
		'label':'Maximum GTR',
		'type':'number'
		},
		{'name':'range_lo',
		'default':2,
		'label':'Minimum GTR',
		'type':'number',
		'validate':simuOpt.valueGT(0)
		},
		{'name':'num_steps',
		'default':5,
		'label':'Number of different GTRs',
		'type':int,
		'validate':simuOpt.valueGT(1)
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


if __name__ == '__main__':
	replicator_choice = simuOpt.Params(replicators)
	if not replicator_choice.getParam():
		sys.exit(1)
	
	if replicator_choice.MAF:
		MAF_opt = simuOpt.Params(MAF_options)
		if not MAF_opt.getParam():
			sys.exit(1)
		MAFs = float_range(MAF_opt.range_hi,MAF_opt.range_lo,MAF_opt.num_steps)
		print MAFs
	
	if replicator_choice.GRR:
		GRR_opt = simuOpt.Params(GRR_options)
		if not GRR_opt.getParam():
			sys.exit(1)
		GRRs = float_range(GRR_opt.range_hi,GRR_opt.range_lo,GRR_opt.num_steps)
		print GRRs
	
	if replicator_choice.WTR:
		WTR_opt = simuOpt.Params(WTR_options)
		if not WTR_opt.getParam():
			sys.exit(1)
		WTRs = float_range(WTR_opt.range_hi,WTR_opt.range_lo,WTR_opt.num_steps)
		print WTRs
