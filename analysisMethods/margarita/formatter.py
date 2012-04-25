def createFiles(pop,inputfileroot):
	"""Margarita requires a phased haplotype file, with an individual's haplotypes on consecutive lines."""
	numcases = sum(1 if ind.affected() else 0 for ind in pop.individuals())
	numInd = pop.popSize()
	numcontrols = numInd - numcases
	locpos = pop.lociPos()
	totNumLoc = pop.totNumLoci()
	
	if pop.ploidy() == 2:
		haplotypes = True
	else:
		haplotypes = False
	
	for chrom in xrange(len(pop.chromNames())):
		chromName = pop.chromNames()[chrom]
		chromLoci = locpos[pop.chromBegin(chrom):pop.chromEnd(chrom)]
		if haplotypes:
			filestats = "%d %d %d\n" %(numcases*2,numcontrols*2,len(chromLoci))
		else:
			filestats = "%d %d %d\n" %(numcases,numcontrols,len(chromLoci))

		outputfilename = "Margarita_%s_%s.txt"%(chromName,inputfileroot)
		out = open(outputfilename,'w')
		out.write(filestats)
		out.write("\n".join([str(x) for x in chromLoci])+'\n')
		
		for ind in pop.individuals():
			if ind.affected():
				if haplotypes:
					for ploidy in range(2):
						hap = "".join([str(x) for x in ind.genotype(chroms=chrom,ploidy=ploidy)])
						out.write('%s\n'%(hap))
				else:
					hap = "".join([str(x) for x in ind.genotype(chroms=chrom)])
					out.write('%s\n'%(hap))
		for ind in pop.individuals():
			if not ind.affected():
				if haplotypes:
					for ploidy in range(2):
						hap = "".join([str(x) for x in ind.genotype(chroms=chrom,ploidy=ploidy)])
						out.write('%s\n'%(hap))
					
				else:
					hap = "".join([str(x) for x in ind.genotype(chroms=chrom)])
					out.write('%s\n'%(hap))
		out.close()	
		return outputfilename
