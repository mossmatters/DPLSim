def createFiles(pop,infileroot):
	"""Creates phased inputdata file for TreeDT. Although not explicitly stated,
	the TreeDT algorithm is probably best run with one file per region, so the output
	is multiple files, one per chromosome."""
	numInd = pop.popSize()
	locNames = pop.lociNames()
	numLoc = pop.totNumLoci()
	outfilenames = []
	if pop.ploidy() == 2:
		haplotypes = True
	else:
		haplotypes = False

	for chrom in xrange(len(pop.chromNames())):
		chromName = pop.chromNames()[chrom]
		chromLoci = locNames[pop.chromBegin(chrom):pop.chromEnd(chrom)]
		
		
		outputfilename = "TreeDT_" + chromName +  "_" + infileroot + ".txt"
		outfilenames.append(outputfilename)
		outFile = open(outputfilename,'w')
	
		header_string = "Id Status %s \n" %(" ".join("M" + x for x in chromLoci))
		outFile.write(header_string)
	
		if haplotypes:
			for ind in xrange(numInd):
				for ploidy in range(2):
					haplo_out = " ".join(['1' if x == 0 else '2' for x in pop.individual(ind).genotype(chroms=chrom,ploidy=ploidy)])
					if pop.individual(ind).affected():
						outFile.write("case%s_%s a %s\n" %(ind,ploidy,haplo_out))
					else:
						outFile.write("control%s_%s c %s\n" %(ind,ploidy,haplo_out))
		else:
			for ind in xrange(numInd):
				haplo_out = " ".join(['1' if x == 0 else '2' for x in pop.individual(ind).genotype(chroms=chrom)])
				if pop.individual(ind).affected():
					outFile.write("case%s 2 %s\n" %(ind,haplo_out))
				else:
					outFile.write("control%s 1 %s\n" %(ind,haplo_out))

		outFile.close()
		return outfilenames
		