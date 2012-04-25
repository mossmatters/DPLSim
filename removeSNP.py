"""
Functions for removing SNPs from simuPOP population objects.

removeRare: removes SNPs with minor allele frequencies below a threshold.
	The threshold defaults are 0.0000001 or 0.999999, meaning only monomorphic loci are removed.
	A list of names of Disease Loci are required.

writeSNPLoc: writes a text file with the name of each DPL and the new index location.
	This function is useful for the programs which do not use marker names or locations,
	to later identify the causative SNP.

removeDPL: removes the DPL
"""
import simuOpt
simuOpt.setOptions(alleleType='binary', optimized=True,quiet=True)
import simuPOP as sim

def removeRare(pop,thresh_hi=0.999999,thresh_lo=0.000001,DPL=['rs4491689'],savefile=False):
	"""
	Removes rare SNPs with a minor allele frequency below a threshold value.
	The default thresholds will only remove monomorphic loci.
	If savefile=False, the population is simply modified.
		Set savefile to a string to save the population to a binary file.
	The function returns:
		the number of loci removed 
		a list of the the relative locations of the DPL.
	"""
	sim.stat(pop,alleleFreq=range(pop.totNumLoci()))
	lociToRemove = [l for l in xrange(pop.totNumLoci()) if pop.dvars().alleleFreq[l][0] > thresh_hi or pop.dvars().alleleFreq[l][0] < thresh_lo]
	pop.removeLoci(lociToRemove)
	if savefile:
		pop.save(savefile)
	return len(lociToRemove),[pop.locusByName(x) for x in DPL]
	
def writeSNPLoc(relLoc,filename,DPL=['rs4491689']):
	"""
	Writes a file containing the new relative locations for each DPL.
	"""
	outfile=open(filename,'w')
	for x in range(len(DPL)):
		outfile.write("%s,%d\n" % (DPL[x],relLoc[x]))
	outfile.close()
	
def removeDPL(pop,DPL=['rs4491689'],savefile=False):
	"""
	Removes a locus by name and (if specified) saves the population to savefile.
	Expands upon the simuPOP.removeLoci() by returning an error if one of the DPL is already removed. 
	"""
	for locus in DPL:
		try:
			pop.removeLoci(pop.locusByName(locus))
		except ValueError:
			return "Locus %s already removed!" %locus
	if savefile:
		pop.save(savefile)
	return 0
	
if __name__=='__main__':
	popname = 'rep_1.pop'
	newDPLfile = popname.split('.')[0] + "_newDPL_loc.txt"
	
	pop = sim.loadPopulation(popname)
	print "Started with %d loci" % pop.totNumLoci()
	numRemoved,newLoc = removeRare(pop,savefile='MAFremoved_'+popname)
	print "Removed %d Loci!" % numRemoved
	print "pop now has %d loci" % pop.totNumLoci()
	
	writeSNPLoc(newLoc,newDPLfile)
	
	removeDPL_success = removeDPL(pop,savefile='DPLremoved_'+popname)
	print removeDPL_success
	removeDPL_success = removeDPL(pop,savefile='DPLremoved_'+popname)
	print removeDPL_success