import os,sys,logging
from simuOpt import *
from DPLSim import loadHapMap3,selectMarkers,singleGeneModel,simuGWAS,format,cline_writer,replicator
import simuPOP

pipeline_options = [
	{'name':'download',
	'type':bool,
	'default':False,
	'label':"Download HapMap Pops?"
	},
	{'name':'init',
	'type':bool,
	'default':False,
	'label':"Select Markers and Initialize Merged population?"
	},
	{'name':'expand',
	'type':bool,
	'default':False,
	'label':"Expand init pop using simuGWAS?"
	},
	{'name':'penetrance',
	'type':bool,
	'default':False,
	'label':"Get Case/Control Datasets using Single Gene Model?"
	},
	{'name':'format',
	'type':bool,
	'default':False,
	'label':"Create input files for analysis methods?"
	},
	{'name':'cline',
	'type':bool,
	'default':False,
	'label':"Write Bash Scripts for analysis methods?"
	},
	{'name':'pipeline_mode',
	'type':("chooseOneOf",["single","replicates"]),
	'default':"single",
	'label':"Run for one parameter setting or replicates?"
	}
	]


def downloadData(logger=None,**kwargs):
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
	options = loadHapMap3.options
	short_desc = """This script downloads the second release of the phase 3 of the HapMap datasets\n'
		'and saves them in simuPOP format. It also downloads the fine-scale\n'
		'recombination map and saves the genetic distance of each marker in\n'
		'a dictionary (geneticMap) in the population\'s local namespace."""
	
	if len(kwargs) > 0:
		pars = Params(options,short_desc,kwargs)
	else:
		pars = Params(options,short_desc)
		if not pars.guiGetParam(nCol=2):
			sys.exit(1)
	
	if not pars.skip:
		for chrom in pars.chroms:
			for sample in loadHapMap3.HapMap3_pops:
				popFile = os.path.join(pars.dest, "HapMap3_%s_chr%d.pop" % (sample, chrom))
				try:
					if os.path.isfile(popFile):
						pop = simuPOP.loadPopulation(popFile)
						if pop.popSize() == loadHapMap3.HapMap3_pop_sizes[sample]:
							if logger:
								logger.info("Skipping existing population %s." % popFile)
							continue
				except:
					print "do or do not, there is no try"# continue to load file
					pass
				pop = loadHapMapPop(chrom, sample)
				if logger:
					logger.info("Save population to %s." % popFile)
				pop.save(popFile)

	return pars

def getInitPop(logger=None,**kwargs):
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
	options = selectMarkers.options
	short_desc="""This script chooses specified markers from one or more HapMap\npopulations and saves them in simuPOP format.\n""",
	
	
	if len(kwargs) > 0:
		pars = Params(options,short_desc,**kwargs)
	else:
		pars = Params(options,short_desc)
		if not pars.guiGetParam(nCol=2):
			sys.exit(1)
	
	if os.path.isfile(pars.filename):
		logger.info("Merged population %s already exists, skipping ahead!" % pars.filename)
		return pars
	
	names = []
	if pars.markerList != '':
		mlist = open(pars.markerList)
		for line in mlist.readlines():
			if line.startswith('#') or line.strip() == '':
				continue
			names.append(line.split(',')[0].split()[0])
		if logger:
			logger.info('%d markers located from marker list file %s' %\
				(len(names), pars.markerList))
		
	pop = selectMarkers.getHapMapMarkers(pars.HapMap_dir, 
		names = names,
		chroms=pars.chroms, 
		HapMap_pops=pars.HapMap_pops,
		startPos = pars.startPos,
		endPos = pars.endPos,
		numMarkers = pars.numMarkers,
		minAF = pars.minAF,
		minDist = pars.minDist,
		mergeSubPops = pars.mergeSubPops,
		logger=logger)
		
	if logger:
		logger.info('Save population to %s and marker list to %s.lst' % \
			(pars.filename, pars.filename))
	pop.save(pars.filename)
	selectMarkers.saveMarkerList(pop, pars.filename + '.lst',logger=logger)
	return pars

def getExpandPop(logger=None,**kwargs):
	"""
	Wrapper for simuGWAS.py
	"""
	options = simuGWAS.options
	short_desc = '''This program evolves a subset of the HapMap dataset
	forward in time in order to simulate case control samples with realistic
	allele frequency and linkage disequilibrium structure.'''
	
	if len(kwargs) > 0:
		pars = Params(options,short_desc,**kwargs)
	else:
		pars = Params(options,short_desc)
		if not pars.guiGetParam():
			sys.exit(1)
	if os.path.isfile(pars.filename):
		logger.info("Expanded population %s already exists, skipping ahead!" % pars.filename)
		return pars
	if pars.run_mode == "Now":
		init=simuPOP.loadPopulation(pars.initPop)
		logger.info('Loaded initial population from file %s. ' % pars.initPop)
		pop = simuGWAS.simuGWAS(pars,init,logger)
		if pars.filename:
			logger.info("Saving expanded population to %s" % pars.filename)
			pop.vars().clear()
			pop.save(pars.filename)
		pars.expandPop =pop
	elif pars.run_mode == "Batch":
		pars.saveConfig("simuGWAS.config")
	
	return pars
	
	
def getCaseControl(logger=None,**kwargs):
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
	options = singleGeneModel.options
	short_desc= """This part of the pipeline selects Case and Control individuals
	via the "rejection sampling" method of Peng and Amos. This single gene model will
	determine case/control status based upon one marker, a relative risk, and wild type risk.
	"""
	if kwargs['gui']:
		pars = Params(options,short_desc)
		if not pars.guiGetParam():
			sys.exit(1)	
		return pars	

	else:
		pars = Params(options,short_desc,**kwargs)
		return pars

def get_formatters(logger=None,**kwargs):
	
	if kwargs['gui']:
		pars = Params(format.options,doc="Choose Progs to format input files for")
		if not pars.guiGetParam():
			sys.exit(1)
		return format.format(pars,logger)
	else:
		pars = Params(format.options,doc="Choose Progs to format input files for",**kwargs)
		return format.format(pars,logger)

def get_cline(logger=None,**kwargs):
	if kwargs['gui']:
		pars = Params(format.options,doc="Choose Progs to create bash scripts files for")
		if not pars.guiGetParam():
			sys.exit(1)	
		return cline_writer.cliner(pars,logger)

	else:
		pars = Params(format.options,doc="Choose Progs to create bash scripts for",**kwargs)
		return cline_writer.cliner(pars,logger)

def single_mode(pipeline_pars,logger=None):
	if pipeline_pars.download:
		download_pars=downloadData(logger)
	
	if pipeline_pars.init:
		init_pop_pars =getInitPop(logger)
	
	if pipeline_pars.expand:
		expand_pop_pars = getExpandPop(logger)
	
	if pipeline_pars.penetrance:
		case_control_pars = getCaseControl(logger)
		if pipeline_pars.expand:
			if expand_pop_pars.filename == case_control_pars.expandPop:
				case_control_pars.pop = expand_pop_pars.expandPop
				logger.info("Using expandPop from simuGWAS!")
			else:
				case_control_pars.pop = simuPOP.loadPopulation(case_control_pars.expandPop)
				logger.info("Expanded population %s loaded!" %case_control_pars.expandPop)
		if os.path.isfile(case_control_pars.sampledPop):
			logger.info("Skipping case control dataset, file %s exists." %case_control_pars.sampledPop)
		else:
			case_control_dataset = singleGeneModel.penetrance(case_control_pars,logger)	
			case_control_dataset.save(case_control_pars.sampledPop)
			logger.info("Sampled population saved at %s" %case_control_pars.sampledPop)

	if pipeline_pars.format:
		format_filenames = get_formatters(logger)
	
	if pipeline_pars.cline:
		cline_filenames = get_cline(logger)

def replicate_mode(pipeline_pars,logger=None):
	additional_args = pipeline_pars.asDict()
	if pipeline_pars.gui == 'batch':
		additional_args['gui'] = False
	else:
		additional_args['gui'] = True
	rep_opt = Params(replicator.replicator_options,replicator.short_desc,replicator.__doc__)
	if not rep_opt.getParam(checkArgs=False):
		sys.exit(1)
	additional_args['formatters']=rep_opt.formatters

	if rep_opt.createDirs:
		rep_opt.addOption("dirpaths", replicator.dir_setup(rep_opt,logger),label="List of directories")
		logger.info("Created %d directories" % len(rep_opt.dirpaths))
		
	if pipeline_pars.download:
		download_pars=downloadData(logger)
	
	if pipeline_pars.init:
		init_pop_pars =getInitPop(logger)
	
	#Need to work on this for cases where multiple MAF are used
	if pipeline_pars.expand:
		expand_pop_pars = getExpandPop(logger)
	
	if pipeline_pars.penetrance:
		replicator.rep_case_control(rep_opt,logger) 

	if pipeline_pars.format:
		format_filenames = get_formatters(logger,**additional_args)
	
	if pipeline_pars.cline:
		cline_filenames = replicator.rep_bash(dirpaths,logger,**additional_args)

	
	
	
short_desc = """
This scripts sets up a pipeline for analysis of a disease locus using
multiple analysis methods. Choose below the steps of the pipeline you
would like to set up using DPLSim.
"""	

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger()
	
	pipeline_pars = Params(pipeline_options,short_desc)
	if not pipeline_pars.getParam(checkArgs=False):
		sys.exit(1)
	if pipeline_pars.pipeline_mode=="single":
		single_mode(pipeline_pars,logger)
	elif pipeline_pars.pipeline_mode == "replicates":
		replicate_mode(pipeline_pars,logger)
		
	