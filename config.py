"""
Set "global" variables for use by the penetrance models.
"""

SELECTED_CASE = 0
SELECTED_CONTROL = 0
DISCARDED_INDS = 0
NUM_WT_CASES = 0
NUM_MUT_CONTROLS = 0
risks = [1,1,1]
numCases = 1000
numControls = 1000

def reset():
	"""
	Resets the counters after a run of penetrance.
	"""
	SELECTED_CASE = 0
	SELECTED_CONTROL = 0
	DISCARDED_INDS = 0
	NUM_WT_CASES = 0
	NUM_MUT_CONTROLS = 0
	return	SELECTED_CASE,SELECTED_CONTROL,DISCARDED_INDS,NUM_WT_CASES,NUM_MUT_CONTROLS