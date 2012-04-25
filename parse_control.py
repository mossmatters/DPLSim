"""
This script controls the formatting of data from binary simupop populations
into many different disease gene program input formats. In order to be extendable,
the API will be to have identical control elements for each program type.

By default, has_formatr(programName) will return False unless the formatr is created.
Alternatively, the formatr can be set to be another program's formatr. 

The main method:
1. Takes in a simupop population object.
2. Writes the necessary files.
3. Returns the names of the files created.
"""

import simuOpt
import analysisMethods

options = [
    {'name': 'formatters',
     'default': [],
     'chooseFrom':[x.split('.')[2] for x in analysisMethods.getAnalysisMethods()],
     'label': 'Formatters',
     'description': 'Names of analysis methods for which input files will be created.'
    },
    {'name': 'inputfile',
     'default': 'rep_1.pop',
     'label': 'simuPOP Population',
     'allowedTypes': types.StringType,
     'validate': simuOpt.valueValidFile(),
     'description': 'A simupop population file to parse and format.'
    }
    ]
short_desc = """
Main formatting function to parse simuPOP population file and output the files necessary
To run one or more analysis methods.
"""

if __name__ == "__main__":
	pars = simuOpt.Params(options, short_desc)
	if not pars.getParam():
		sys.exit(1)
