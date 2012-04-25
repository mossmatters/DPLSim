"""
Given a simuPOP population object, this will create the necessary files for Blossoc.

Blossoc requires a haplotypes file and a positions file. 
"""

def createFiles(pop,inputfileroot):
	"""Given a simuPOP population object and a file name root,
	Create a haplotype and position file and return their names."""
	numInd = pop.popSize()
	locpos = pop.lociPos()
	totNumLoc = pop.totNumLoci()
	
	if pop.ploidy() == 2:
		haplotypes = True
	else:
		haplotypes = False
	
	for chrom in xrange(len(pop.chromNames())):
		chromName = pop.chromNames()[chrom]
		chromLoci = locpos[pop.chromBegin(chrom):pop.chromEnd(chrom)]
		
		positionfilename = "Blossoc_positions_%s_%s.txt"%(chromName,inputfileroot) 
		posOut = open(positionfilename,'w')
		posOut.write(" ".join([str(x) for x in chromLoci])+'\n')
		posOut.close()	
		
		genofilename = "Blossoc_genotypes_%s_%s.txt"%(chromName,inputfileroot)
		genoOut = open(genofilename,'w')
		
		for ind in pop.individuals():
			if haplotypes:
				for ploidy in range(2):
					hap = " ".join([str(x) for x in ind.genotype(chroms=chrom,ploidy=ploidy)])
					if ind.affected():
						genoOut.write('1 %s\n'%(hap))
					else:
						genoOut.write('0 %s\n'%(hap))
			else:
				hap = " ".join([str(x) for x in ind.genotype(chroms=chrom)])
				if ind.affected():
					genoOut.write('1 %s\n'%(hap))
				else:
					genoOut.write('0 %s\n'%(hap))
		genoOut.close()	
		return [genofilename,positionfilename]
