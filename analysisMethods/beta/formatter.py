def createFiles(pop,reptext):
	"""Creates the three input files necessary for the R functions called BETA:
	1 genotype file.
	2 phenotype (status) file
	3 positions file"""
	locpos = pop.lociPos()
	outfilenames=[]
	for chrom in xrange(len(pop.chromNames())):
		
		genotypefilename = "Beta_haplotypes_%s_%s.txt" %(pop.chromNames()[chrom],reptext)
		phenotypefilename = "Beta_status_%s_%s.txt"	%(pop.chromNames()[chrom],reptext)
		positionfilename = "Beta_positions_%s_%s.txt"	%(pop.chromNames()[chrom],reptext)
		outfilenames.append((genotypefilename,phenotypefilename,positionfilename))
		genoOut = open(genotypefilename,'w')
		phenoOut = open(phenotypefilename,'w')
		positionOut = open(positionfilename,'w')
		numInd = pop.popSize()
		locNames = pop.lociNames()
		numLoc = pop.totNumLoci()
		allInd = pop.genotype()
		ploidy = pop.ploidy()
		
		chromLoci = locpos[pop.chromBegin(chrom):pop.chromEnd(chrom)]
		positionOut.write("\n".join([repr(int(x)) for x in chromLoci]))
		positionOut.close()
	
		for ind in pop.individuals():
			for x in range(ploidy):
				if ind.affected():
					phenoOut.write("1\n")
				else:
					phenoOut.write("0\n")
			for y in range(ploidy):
				genoOut.write(" ".join([repr(x) for x in ind.genotype(chroms=chrom,ploidy=y)])+"\n")
		
		genoOut.close()
		phenoOut.close()
		return [genotypefilename,phenotypefilename,positionfilename]