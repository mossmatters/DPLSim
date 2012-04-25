#!/usr/bin/env python

import sys, os, random, math, logging

import simuOpt
simuOpt.setOptions(quiet=True, alleleType='binary', optimized=True)
from simuPOP import *

import loadHapMap3, selectMarkers, simuGWAS

def downloadData(logger=None,chroms=[2,5,10],mypops=None):
	'''
	Download and create populations from the third phase of the HapMap3 data.
	By default it grabs all available populations.
	
	chroms -- a list of human chromosome numbers. (required)
	mypops -- a list of HapMap population names. (optional)
	
	If the directory "HapMap" does not exist in the current directory, it will create one.
	In the HapMap directory, if a HapMap population file already exists, it will not be overwritten.
	
	From Peng and Amos example_2.py
	This equivalent to command

	> loadHapMap3.py --chroms='[2, 5,10]' --dest=HapMap
	'''
	if mypops:
		for popName in mypops:
			if popName not in loadHapMap3.HapMap3_pops:
				logger.info("Population %s not a regognized HapMap population name!" %s)
				return
	else:
		mypops = loadHapMap3.HapMap3_pops				
	
	if not os.path.isdir('HapMap'):
		os.mkdir('HapMap')
		
	for chrom in chroms:
		for popName in loadHapMap3.HapMap3_pops:
			filename = 'HapMap/HapMap3_%s_chr%d.pop' % (popName, chrom)
			if not os.path.isfile(filename):
				print "Downloading %s" %filename
				pop = loadHapMap3.loadHapMapPop(chrom, popName)
				pop.save(filename)
			else:
				if logger:
					logger.info("File %s is already downloaded! Delete it to re-download." %filename)
				else:
					print "File %s is already downloaded! Delete it to re-download." %filename

def getInitPop(logger=None,chroms=[2,5,10],startPos=[25000000, 25000000, 40000000],
			numMarkers=[2000, 2000, 2000],
			nameFile='hh550v3_snptable.txt',
			savefiles=False,
			mypops=None):
	'''
	Get markers from a specified range in all HapMap populations, return this initialized population.
	
	logger -- report useful information during the run. (optional)
	chroms -- list of human chromosome numbers. (required)
	startPos -- list starting position (in bp) for each chromosome. If empty, start of chromosome used.
	numMarkers -- list of the number of markers for each chromosome. (required)
	nameFile -- A file containing the list of marker names to subset from the HapMap project, for example the Illumina 1M chipset.
	savefiles -- A list of two file names: [population_filename,marker_list_filename]. Nothing saved if False. (optional)
	mypops -- A list of HapMap3 population names, in the format such as 'HapMap_CEU'. (optional)
	
	Returns the initial population in simuPOP format, merged across all mypops for the selected markers.
	
	The default settings specify:
	Select 2000 markers on regions beginning at startPos on chromosomes 2, 5 and 10, using markers from the Illumina 1M chipset
	Savefiles may be specified as a list of two file names, one for the population and another for the marker list.
	
	Modified from Peng and Amos ex2.py
	From command line, you could prepare a marker list file from illumina annotation file
		 > cut -d, -f2 HumanHap550v3_A.csv  > HumanHap550v3_A.lst
	and then select markers
		 > selectMarkers.py --markerList='HumanHap550v3_A.lst' --chroms='[2, 5,10]' \
			--numMarkers='[2000,2000,2000]' --startPos='[20000000, 20000000,40000000]' \
			--filename=ex2_init.pop
	'''
	if mypops:
		for popName in mypops:
			if popName not in selectMarkers.HapMap3_pops:
				logger.info("Population %s not a regognized HapMap3 population name! Use the format: 'HapMap3_YRI'." %s)
				return
	else:
		mypops = selectMarkers.HapMap3_pops				

	names = []
	if nameFile:
		ann = open(nameFile)
		if logger:
			logger.info('Loading marker names from %s' %s)
		for line in ann:
			names.append(line.split('\t')[0])
 
	initpop = selectMarkers.getHapMapMarkers(
		names=names,
		HapMap_dir='HapMap',
		chroms=chroms,
		HapMap_pops=mypops,
		startPos=startPos,
		numMarkers=numMarkers,
		mergeSubPops=True,
		logger=logger)
	if savefiles:
		initpop.save(savefiles[0])
		selectMarkers.saveMarkerList(initpop, savefiles[1])
	return initpop

# rs4491689	2	26494285	A	G	0.2825
# rs2619939	5	25837347	C	T	0.2825
# DPL = ['rs4491689','rs2619939']
def expandPop(initpop,DPL=['rs4491689'],fitness=[1,0.996,0.994],curAlleleFreq=[0.05],scale=1):
	"""
	From the initial HapMap data, evolve the population with expansion and selection at one or more loci.
	
	initpop -- simuPOP population object containing a set of markers at one or more chromosomes.
	DPL -- List of disease locus names to be under selection during population expansion.
	fitness -- List of relative fitnesses, such as [AA, Aa, aa] for one locus. 
	curAlleleFreq -- List of final allele frequencies expected for the loci under expansion.	
	scale -- Determines whether the recombination/mutation is sped up during population expansion.
	
	Modified from example_2.py from Peng and Amos 2010.
	This is equivalent to
	
	  > simuGWAS.py --initPop=ex2_init.pop --DPL='["rs4491689","rs6869003"]' \
	  --filename=ex2_expanded.pop --curAlleleFreq='[0.05, 0.15]' --trajectory='forward'  --mlSelModel='multiplicative' \
	  --scale=1 --optimized --gui=False --fitness='[1, 0.996, 0.994, 1, 1.001, 1.005]'
	
	"""
	pars = simuOpt.Params(simuGWAS.options, DPL=DPL,
		curAlleleFreq=curAlleleFreq, 
		trajPlot='ex2_traj.pdf', mlSelModel='multiplicative',
		scale=scale, fitness=fitness)
	expandpop = simuGWAS.simuGWAS(pars,initpop)
	return expandpop		



#random.seed(235234)  # to keep result reproducible.
#getRNG().set(seed=12345)

if __name__ == '__main__':
	initPopName = 'ex2_init.pop'
	
	logging.basicConfig(level=logging.INFO)
	logger = logging.getLogger('DPLSimtest')
	downloadData(logger)
	if not os.path.isfile(initPopName): 
		getInitPop(logger)
	else:
		print "Initial population %s already exists! Delete it to regenerate" % initPopName
		initpop = loadPopulation(initPopName)
	expandpop = expandPop(initpop)
