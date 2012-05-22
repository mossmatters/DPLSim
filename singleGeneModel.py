""" 
This script takes an expanded population from simupop and selects cases and controls
based on a disease model set in _selectInds. Individuals are chosen based on a rejection-sampling
approach noted in Peng and Amos 2010-- essentially, random matings among the expanded population
are attempted until a given number of cases has successfully been reached.
 
The penetrance method expects a population object in simupop format.
It will return a reduced population of case and control individuals.

The user will need to specify:

1) The locus used for the disease model, by name.
2) The Genotype Relative Risk.
3) The wild-type risk.
4) The number of cases and controls. 
"""

import simuOpt, random, math,sys
simuOpt.setOptions(quiet=True, alleleType='binary', optimized=True)
from simuPOP import *

import config

options = [
	{'name':'DPL',
	'default':["rs4491689"],
	'type':'strings',
	'label':"Disease Locus ID"
	},
	{'name':'GRR',
	'default':1.0,
	'type':'number',
	'label':"Genotype Relative Risk",
	'validate':simuOpt.valueGE(1.0)
	},
	{'name':'wtr',
	'default':0.05,
	'type':'number',
	'label':'Wild Type Risk',
	'validate':simuOpt.valueBetween(0,1)
	},
	{'name':'numCases',
	'default':1000,
	'type':int,
	'label':"Number of Cases"
	},
	{'name':'numControls',
	'default':1000,
	'type':int,
	'label':"Number of Controls"
	},
	{'name':'expandPop',
	'default':'MAF_0.05_2.pop',
	'type':'filename',
	'label':'Expanded Population to Sample',
	'validate':simuOpt.valueValidFile()
	},
	{'name':'sampledPop',
	'default':'rep_1.pop',
	'type':str,
	'label':"Name of sampled population file"
	},
	{'name':'pop',
	'default':'',
	'description':'simuPOP population object from expandPop'
	}
	]


def _selectInds(off, param):
	'Deterimine if the offspring can be kept'
	g1 = off.allele(param[0], 0) + off.allele(param[0], 1)
	affected = random.random() < config.risks[g1]
	if affected:
		if config.SELECTED_CASE < config.numCases:
			off.setAffected(True)
			config.SELECTED_CASE += 1
			if g1 == 0:
				config.NUM_WT_CASES += 1
			return True
	else:
		if config.SELECTED_CONTROL < config.numControls:
			config.SELECTED_CONTROL += 1
			off.setAffected(False)
			if g1 > 0:
				config.NUM_MUT_CONTROLS +=1
			return True
			
	config.DISCARDED_INDS += 1
	return False



def penetrance(pars,logger=None):
	"""
	Given a simuPOP population, the relative risk (additive), the wild-type risk, and the number and cases and controls, build a case-control dataset in simuPOP format.
	DPL must be a list, even if there is only one locus.
	"""
	#DPL=["rs4491689", "rs2619939"]
	reppop = pars.pop.clone()
	loci = reppop.lociByNames(pars.DPL)
	#Set risks
	het_risk = pars.wtr*pars.GRR
	if pars.GRR > 1:
		hom_mut_risk = pars.wtr*pars.GRR*2
	else:
		hom_mut_risk = pars.wtr
	
	config.risks = [pars.wtr,het_risk,hom_mut_risk]
	config.numCases = pars.numCases
	config.numControls = pars.numControls
	
	reppop.evolve(
		matingScheme=RandomMating(
			ops=[
				MendelianGenoTransmitter(),
				# an individual will be discarded if _selectInds returns False
				PyOperator(func=_selectInds, param=loci)
			], 
			subPopSize=config.numCases + config.numControls
		),
		gen = 1
	)
	
	if logger:
		logger.info("Number of Wild Type Cases: %d" %config.NUM_WT_CASES)
		logger.info("Number of Mutant Controls: %d" %config.NUM_MUT_CONTROLS)
	
	config.SELECTED_CASE,config.SELECTED_CONTROL,config.DISCARDED_INDS,config.NUM_WT_CASES,config.NUM_MUT_CONTROLS = config.reset()
	return reppop

if __name__=='__main__':
	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()

	pars = simuOpt.Params(options)
	if not pars.getParam():
		sys.exit(1)
	pars.pop = loadPopulation(pars.expandPop)
	logger.info("Expanded population %s loaded!" %pars.expandPop)
	
	case_control_dataset = penetrance(pars,logger)	
	
	case_control_dataset.save(pars.sampledPop)
	logger.info("Sampled population saved at %s" %pars.sampledPop)