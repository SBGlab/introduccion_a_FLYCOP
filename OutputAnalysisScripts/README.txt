With the available output analysis scripts and depending on your research interests, here are some suggested analysis to be performed after executing FLYCOP.

A. INDIVIDUAL FLYCOP RUN: PREVIOUS ANALYSIS. 
	
	1. Obtaining the number of configurations with:
		- Acceptable Standard Deviation (SD)
		- Excessive Standard Deviation (SD)
		- Wrong configurations because of biomass exhaustion during the simulation ('ZeroDivisionError' Python error)
		
	2. Further evaluating those wrong configurations with 'ZeroDivisionError'
	3. Further evaluating those configurations with excessive SD
	
	ASSOCIATED SCRIPTS: ConfigAnalysis_Error.py (2), ConfigAnalysis_NonError_SDexcess.py (3). See full description within the script itself.
	
	
B. INDIVIDUAL FLYCOP RUN: PARAMETER ANALYSIS (input, output)

	1. Input Parameters Analysis. Script: InputParametersAnalysis.py
	2. Output Parameters Analysis. Script: OutputParametersAnalysis.py
	3. Statistical Analysis input and output parameters. Script: InputOutputParameters_StatsAnalysis.py
		- count, mean, std, min, max, quartiles
	

C. INDIVIDUAL FLYCOP RUN: COMPARISON OF FITNESS RANKS

Description of the idea of fitness ranks
----------------------------------------
The total number of final configurations obtained in the FLYCOP run are organized according to the final fitness value, in approximate even ranks.
This operation would allow to understand how the input parameters condition the final fitness values (and the final production of the metabolite(s) of interest), and how the output parameters are related to each fitness interval.

Further comparison
------------------

	1. Input Parameters Comparison between fitness ranks. Script: IndivFitnessComparativeAnalysis_InputParams.py
	2. Output Parameters Comparison between fitnessranks. Script: IndivFitnessComparativeAnalysis_OutputParams.py



D. MULTIPLE FLYCOP RUNS: MULTIPLE COMPARATIVE ANALYSIS

Description
-----------
Several FLYCOP runs are compared in terms of their input and output parameters. Ideally, these FLYCOP runs should be equivalent except in one input (reference) parameter (or, at most, a few parameters). Thus the output differences between the different FLYCOP runs could be unequivocally attributed to the mentioned reference parameter.

Scripts
-------

	1. MultipleComparativeAnalysis.py
































