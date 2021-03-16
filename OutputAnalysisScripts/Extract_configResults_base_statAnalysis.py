#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:02:18 2020

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Statistical analysis for the data obtained from "Extract_configResults_base.py" script
    
EXPECTED INPUT

    'configurationsResults_Scenario0_analysis.xlsx' from "Extract_configResults_base.py" script
        
OUTPUT

    Statistical description (on screen) of next variables: fitness, Naringenin final concentration, 
        p-Coumarate final concentration, final E. coli biomass, final P. putida KT biomass
    
NOTE THAT:
    
    The variables to be displayed and the fitness ranks to be analyzed can be adapted if desired
    The order of the fitness_ranks_set should be: higher to lower rank; (lower_bound, upper_bound)
    
"""

# import re
import pandas as pd
import os.path
from FitnessRanks import describe_fitness_ranks
path = "../Project4_EcPp2_M9adjusted/100SMAC10"
os.chdir(path)

# -----------------------------------------------------------------------------
# STATISTICAL ANALYSIS
# -----------------------------------------------------------------------------
# INPUT: 'configurationsResults_Scenario0_analysis.txt', sorted descending by 'fitness'
dataTable = pd.read_excel("configurationsResults_Scenario0_analysis.xlsx", sheet_name="Product_ratios", engine="openpyxl")
dataTable = dataTable[dataTable["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD

fitness_ranks_set = ((100, 150), (70, 100), (50, 60), (40, 50), (30, 40), (20, 30), (10, 20), (0, 10))  # Modificar estos valores, ordenar rangos de menor a mayor
describe_fitness_ranks(fitness_ranks_set, dataTable, descr_columns = ["fitFunc", "Nar_mM", "pCA_mM", "FinalEc_gL", "FinalKT_gL"], ref_colum = "fitFunc")
























