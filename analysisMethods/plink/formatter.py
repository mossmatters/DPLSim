def createFiles(pop,inputfileroot):
	"""Creates inputdata file for PLINK in biallelic format. Assumes inputdata is phased haplotypes, one line
	per individual."""
	if pop.ploidy() != 2:
		print "PLINK requires biallelic data!"
		return 0
		
	numInd = pop.popSize()
	locNames = pop.lociNames()
	numLoc = pop.totNumLoci()
	allInd = pop.genotype()
	
	markerfilename = inputfileroot + ".ped"
	markerOut = open(markerfilename,'w')
	id_counter = 0
	for ind in pop.individuals():
		geno = ind.genotype()
		hap1 = ['1' if x == 0 else '2' for x in geno[:numLoc]]
		hap2 = ['1' if x == 0 else '2' for x in geno[numLoc:]]
		geno_out = " ".join(["%s %s"%(hap1[i],hap2[i]) for i in xrange(numLoc)])
		if ind.affected():
			outstring = "case%d 1 0 0 1 2 %s\n"%(id_counter,geno_out)
		else:
			outstring = "control%d 1 0 0 1 1 %s\n"%(id_counter,geno_out)
		id_counter +=1
		markerOut.write(outstring)
	markerOut.close()
	
	
	positionfilename = inputfileroot + ".map"
	positionOut = open(positionfilename,'w')
	for loc in xrange(numLoc):
		positionOutString = "%s\t%s\t0\t%s\n" %(pop.chromName(pop.chromLocusPair(loc)[0]),locNames[loc],pop.locusPos(loc))
		positionOut.write(positionOutString)
	positionOut.close()
	return [markerfilename,positionfilename]
