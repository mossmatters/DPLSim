import DPLSim

class ProgramInfo(DPLSim.AnalysisMethod):
	def __init__(self):
		self.name="BETA"
		self.format = True
		self.formatter = self.getFormatter()