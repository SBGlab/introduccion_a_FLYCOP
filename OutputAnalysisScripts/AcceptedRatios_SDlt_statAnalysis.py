#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Dec 27 23:02:18 2020

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Statistical analysis for the data obtained from "AcceptedRatios_SDlt.py" script
    
EXPECTED INPUT

    'dataTable_AcceptedRatios_SDlt.xlxs' from "AcceptedRatios_SDlt.py" script
        
OUTPUT

    Statistical description (on screen) of next variables: 
        fitFunc, ratio 'sucr1_frc2', ratio 'Ecbiomass_KTbiomass'
    
NOTE THAT:
    
    The variables to be displayed and the fitness ranks to be analyzed can be adapted if desired
    The order of the fitness_ranks_set should be: higher to lower rank; (lower_bound, upper_bound)
    
"""


# import re
import pandas as pd
import os.path
from FitnessRanks import describe_fitness_ranks
path = "../Project3_EcPp2_LimNut_M9/Nitrogen/M950N"   # Change to the desired path
os.chdir(path)

# -----------------------------------------------------------------------------
# STATISTICAL ANALYSIS
# -----------------------------------------------------------------------------
# INPUT: dataTable_AcceptedRatios_SDlt.xlsx, sorted descending by 'fitFunc'
dataTable = pd.read_excel("dataTable_AcceptedRatios_SDlt_sub.xlsx", sheet_name="Uptake_initBiomass_r", engine="openpyxl")
dataTable = dataTable[dataTable["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD

fitness_ranks_set = ((0, 10), (10, 25), (30, 40), (40, 55), (100, 200), (200, 300), (390, 450))
describe_fitness_ranks(fitness_ranks_set, dataTable, descr_columns = ["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"], ref_colum = "fitFunc")
















