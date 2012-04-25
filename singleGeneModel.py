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

import simuOpt, random, math
simuOpt.setOptions(gui=False, alleleType='binary', optimized=True)
from simuPOP import *

import config

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



def penetrance(pop,DPL=["rs4491689"],GRR=1.0,wtr=0.05,numCases=1000,numControls=1000):
	"""
	Given a simuPOP population, the relative risk (additive), the wild-type risk, and the number and cases and controls, build a case-control dataset in simuPOP format.
	DPL must be a list, even if there is only one locus.
	"""
	
	print config.SELECTED_CASE
	#DPL=["rs4491689", "rs2619939"]
	reppop = pop.clone()
	loci = reppop.lociByNames(DPL)
	#Set risks
	het_risk = wtr*GRR
	if GRR > 1:
		hom_mut_risk = wtr*GRR*2
	else:
		hom_mut_risk = wtr
	
	config.risks = [wtr,het_risk,hom_mut_risk]
	config.numCases = numCases
	config.numControls = numControls
	
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
	print config.SELECTED_CASE
	config.SELECTED_CASE,config.SELECTED_CONTROL,config.DISCARDED_INDS,config.NUM_WT_CASES,config.NUM_MUT_CONTROLS = config.reset()
	return reppop

if __name__=='__main__':
	pop = loadPopulation('MAF_0.05_2.pop')
	print "Expanded population loaded!"
	pop_file_name = "rep_1.pop"
	
	for a in range(2):
		case_control_dataset = penetrance(pop)	
	
	case_control_dataset.save(pop_file_name)