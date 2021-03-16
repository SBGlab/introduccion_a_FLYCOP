#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:02:18 2020

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Comparative Statistical Analysis for different fitness ranks within the same FLYCOP run
    
EXPECTED INPUT

    'dataTable_AcceptedRatios_SDlt.xlsx' from "AcceptedRatios_SDlt.py" script (OutputAnalysis)
        for the FLYCOP run to be considered in the Comparative Analysis
        
OUTPUT

    Folder: ./ComparativeAnalysisPlots
        "UptakeRatesRatio_Boxplot.png"
        "UptakeRatesRatio_Boxplot_AxisReduced.png"
        
        "InitBiomassRatio_Boxplot.png"
        "InitBiomassRatio_Boxplot_Boxplot_AxisReduced.png"
    
NOTE THAT:
    
    xxx
    
"""

# import re
import pandas as pd
import os.path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from FitnessRanks import organize_fitness_ranks
import Plotting as myplt
original_path = os.getcwd()

# -----------------------------------------------------------------------------
# STATISTICAL COMPARATIVE ANALYSIS
# -----------------------------------------------------------------------------

path1 = "../Project3_EcPp2_LimNut_M9/Nitrogen/M950N"
os.chdir(path1)
dataTable = pd.read_excel("dataTable_AcceptedRatios_SDlt_sub.xlsx", sheet_name="Uptake_initBiomass_r", engine="openpyxl")

# NEW ORGANIZED DATAFRAME
# -----------------------------------------------------------------------------
dataTable["FitRank"] = 0

# Define the new fitness ranks
fitness_ranks_set = ((0, 10), (10, 25), (30, 40), (40, 55), (100, 200), (200, 300), (390, 450))
dataTable = organize_fitness_ranks(dataTable, fitness_ranks_set, ref_colum = "fitFunc")  


# -----------------------------------------------------------------------------
# BOXPLOT & Scatter REPRESENTATION
# Default whiskers: 1.5*(IQR)
# -----------------------------------------------------------------------------
# Qué se evalúa / representa en los plots finales: 
    # Ratio Uptakes;
    # ratio initBiomass;
    # evolución de biomasa (¿parámetro?) con efecto de muerte;

# BoxPlot display
sns.set_theme(style="darkgrid")
sns.set_context('paper', font_scale=1.0, rc={'line.linewidth': 2.5, 
                'font.sans-serif': [u'Times New Roman']})


# -----------------------------------------------------------------------------
if not os.path.isdir("ComparativeAnalysisPlots"):
    os.mkdir("ComparativeAnalysisPlots")  # Create "ComparativeAnalysisPlots" directory
os.chdir("ComparativeAnalysisPlots")
# -----------------------------------------------------------------------------


# UPTAKE RATES
# ------------

# BOXPLOT 
myplt.basic_boxplot(dataTable, "FitRank", "sucr1_frc2", 'Fitness Ranks', 'Ratio of Uptake Rates', "UptakeRatesRatio_Boxplot")
myplt.basic_boxplot_ylims(dataTable, "FitRank", "sucr1_frc2", 'Fitness Ranks', 'Ratio of Uptake Rates', "UptakeRatesRatio_Boxplot_AxisReduced1", ylims = (0, 1))
myplt.basic_boxplot_ylims(dataTable, "FitRank", "sucr1_frc2", 'Fitness Ranks', 'Ratio of Uptake Rates', "UptakeRatesRatio_Boxplot_AxisReduced2", ylims = (0, 2))

    
# INITIAL BIOMASS
# ---------------

# BOXPLOT
myplt.basic_boxplot(dataTable, "FitRank", "Ecbiomass_KTbiomass", 'Fitness Ranks', 'Ratio of Initial Biomass', "InitBiomassRatio_Boxplot")
# myplt.basic_boxplot_ylims(dataTable, "FitRank", "Ecbiomass_KTbiomass", 'Fitness Ranks', 'Ratio of Initial Biomass', "InitBiomassRatio_Boxplot_Boxplot_AxisReduced", ylims = (0, 4))






















