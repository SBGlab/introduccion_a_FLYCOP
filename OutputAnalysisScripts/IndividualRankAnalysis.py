#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 09:41:22 2021

@author: ivan
"""

"""
DESCRIPTION

    Individual Rank Analysis: consider one or several ranks in a particular FLYCOP run
    
EXPECTED INPUT

    'configurationsResults_Scenario0_analysis_fitFunc.xlsx' or 'configurationsResults_Scenario0_analysis_Nar.xlsx'
        from "Extract_configResults_limNut.py" script (OutputAnalysis) for the oarticular FLYCOP run to be considered
        
OUTPUT

    Folder: ./IndividualRankAnalysis
    
        "finalNH4_fitrank1_scatter.png"
        "finalpi_fitrank1_scatter.png"
        "finalsucr_fitrank1_scatter.png"
        "DT_cycles_fitrank1_scatter.png"
        
        "finalNH4_fitrank2_scatter.png"
        "finalpi_fitrank2_scatter.png"
        "finalsucr_fitrank2_scatter.png"
        "DT_cycles_fitrank2_scatter.png"
    
NOTE THAT:
    
    xxx
    
"""

# import re
import pandas as pd
import os.path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# from FitnessRanks import organize_fitness_ranks
from DeadTracking_functions import when_death_starts
import Plotting as myplt
script_path = os.getcwd()


# -----------------------------------------------------------------------------
# REFERENCE PATH
# -----------------------------------------------------------------------------

ref_path = "../Project3_EcPp2_LimNut_M9/Nitrogen/M950N_nonSucr"
os.chdir(ref_path)


# DATAFRAME IN FLYCOP CONFIGURATION TO BE TAKEN
configResults = pd.read_excel("configurationsResults_Scenario0_analysis_sub_fitFunc.xlsx", sheet_name="Product_ratios", engine="openpyxl")
configResults_copy = configResults.copy()

configResults_copy = configResults_copy[configResults_copy["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD
configResults_copy = when_death_starts(configResults_copy)


# FITNESS RANK IN DATAFRAME TO BE CONSIDERED
configResults_fitRank2 = configResults_copy[configResults_copy["fitFunc"] < 20]
configResults_fitRank2 = configResults_fitRank2[configResults_fitRank2["fitFunc"] > 10]

# configResults_fitRank1 = configResults_copy[configResults_copy["fitFunc"] < 10]
# configResults_fitRank2 = configResults_fitRank2[configResults_fitRank2["fitFunc"] > 10]


# -----------------------------------------------------------------------------
# PLOTTING
# -----------------------------------------------------------------------------
if not os.path.isdir("IndividualRankAnalysis"):
    os.mkdir("IndividualRankAnalysis")  # Create "IndividualRankAnalysis" directory
os.chdir("IndividualRankAnalysis")
# -----------------------------------------------------------------------------

# RANK 2 
myplt.one_plot("fitFunc", "NH4_mM", configResults_fitRank2, "finalNH4_fitrank2_scatter", "Final NH4 vs. fitness")
myplt.one_plot("fitFunc", "pi_mM", configResults_fitRank2, "finalpi_fitrank2_scatter", "Final Pi vs. fitness")
myplt.one_plot("fitFunc", "FinalSucr", configResults_fitRank2, "finalsucr_fitrank2_scatter", "Final Sucr vs. fitness")
myplt.one_plot("fitFunc", "DT_cycles_init", configResults_fitRank2, "DT_cycles_fitrank2_scatter", "Init Death Cycle vs. fitness")

myplt.one_plot("NH4_mM", "pi_mM", configResults_fitRank2, "finalpi_finalNH42_scatter", "Final Pi vs. Final NH4")
myplt.one_plot("NH4_mM", "FinalSucr", configResults_fitRank2, "finalsucrose_finalNH42_scatter", "Final Sucrose vs. Final NH4")

myplt.one_plot("DT_cycles_init", "pi_mM", configResults_fitRank2, "finalpi_DeathInit2_scatter", "Final Pi vs. Death Init Cycle")
myplt.one_plot("DT_cycles_init", "FinalSucr", configResults_fitRank2, "finalsucrose_DeathInit2_scatter", "Final Sucrose vs. Death Init Cycle")


# RANK 1
# myplt.one_plot("fitFunc", "NH4_mM", configResults_fitRank1, "finalNH4_fitrank1_scatter", "Final NH4 vs. fitness")
# myplt.one_plot("fitFunc", "pi_mM", configResults_fitRank1, "finalpi_fitrank1_scatter", "Final Pi vs. fitness")
# myplt.one_plot("fitFunc", "FinalSucr", configResults_fitRank1, "finalsucr_fitrank1_scatter", "Final Sucr vs. fitness")
# myplt.one_plot("fitFunc", "DT_cycles_init", configResults_fitRank1, "DT_cycles_fitrank1_scatter", "Init Death Cycle vs. fitness")
# myplt.one_plot("NH4_mM", "pi_mM", configResults_fitRank1, "finalpi_finalNH41_scatter", "Final Pi vs. Final NH4")
# myplt.one_plot("NH4_mM", "FinalSucr", configResults_fitRank1, "finalsucrose_finalNH41_scatter", "Final Sucrose vs. Final NH4")

































