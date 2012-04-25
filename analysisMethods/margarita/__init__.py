import DPLSim
class ProgramInfo(DPLSim.AnalysisMethod):
	def __init__(self):
		self.name="MARGARITA"
		self.format=True
		self.formatter = self.getFormatter()