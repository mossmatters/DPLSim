import DPLSim

class ProgramInfo(DPLSim.AnalysisMethod):
	def __init__(self):
		self.name="BLOSSOC"
		self.format = True
		self.formatter = self.getFormatter()		
		self.cline=True
		self.clineWriter = self.getClineFunction()