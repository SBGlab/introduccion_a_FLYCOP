#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 12:10:35 2021

@author: Iván Martín Martín
"""

# VERY SPECIFIC SCRIPT (TO MY CONSORTIUM OF NARINGENIN PRODUCTION)

"""
DESCRIPTION

    Track limiting nutrients and carbon sources with respect to final biomass, naringenin production and final fitness
    
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

import pandas as pd
import os.path
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import Plotting as myplt
from FitnessRanks import describe_fitness_ranks, organize_fitness_ranks
from DeadTracking_functions import when_death_starts
original_path = os.getcwd()


# -----------------------------------------------------------------------------
# PATH
# -----------------------------------------------------------------------------

path1 = "../Project3_EcPp2_LimNut_M9/Nitrogen/M9200N_nonSucr"
os.chdir(path1)

configResults_original = pd.read_csv("configurationsResults_Scenario0.txt", sep="\t", header="infer")
configResults = configResults_original.copy()
# print(configResults)



# -----------------------------------------------------------------------------
# ASSOCIATED PLOTS
# -----------------------------------------------------------------------------
if not os.path.isdir("DeadTracking_basics"):
    os.mkdir("DeadTracking_basics")  # Create "DeadTracking_basics" directory
os.chdir("DeadTracking_basics")
# -----------------------------------------------------------------------------

""" PLOTS
# Two different plots in the same figure
myplt.two_plots_twolabels(x_label, y_label1, y_label2, DataFrame, name_image)

# One plot per figure
myplt.one_plot(x_label, y_label, DataFrame, name_image)
"""


# FINAL BIOMASS vs. fitness
myplt.two_plots_twolabels("fitFunc", "FinalEc_gL", "FinalKT_gL", configResults, "FinalBiomass_vs_fitness")

# FINAL BIOMASS vs. naringenin production
myplt.two_plots_twolabels("Nar_mM", "FinalEc_gL", "FinalKT_gL", configResults, "FinalBiomass_vs_NarProd")


# N & P nutrients vs. fitness
myplt.two_plots_twolabels("fitFunc", "NH4_mM", "pi_mM", configResults, "NPnutrients_vs_fitness")

# N & P nutrients vs. naringenin production
myplt.two_plots_twolabels("Nar_mM", "NH4_mM", "pi_mM", configResults, "NPnutrients_vs_NarProd")


# Sucrose vs. fitness
myplt.one_plot("fitFunc", "FinalSucr", configResults, "FinalSucr_vs_fitness", "Final sucrose vs. Fitness")

# Sucrose vs. naringenin production
myplt.one_plot("Nar_mM", "FinalSucr", configResults, "FinalSucr_vs_NarProd", "Final sucrose vs. [Naringenin]")

os.chdir("..")


# -----------------------------------------------------------------------------
# Fitness Rank Analysis
# -----------------------------------------------------------------------------
print("\nFITNESS RANK ANALYSIS\n")
dataTable_fitFunc = pd.read_excel("configurationsResults_Scenario0_analysis_sub_fitFunc.xlsx", sheet_name="Product_ratios", engine="openpyxl")
dataTable_fitFunc = dataTable_fitFunc[dataTable_fitFunc["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD
dataTable_fitFunc = when_death_starts(dataTable_fitFunc)

fitness_ranks_set_fitFunc = ((0, 6), (6, 11), (20, 40), (95, 115))  # Modificar estos valores, ordenar rangos de menor a mayor
describe_fitness_ranks(fitness_ranks_set_fitFunc, dataTable_fitFunc, descr_columns = ["FinalSucr", "NH4_mM", "pi_mM", "DT_cycles_init"], ref_column = "fitFunc")


# -----------------------------------------------------------------------------
# Naringenin Rank Analysis
# -----------------------------------------------------------------------------
print("\n\n\nNARINGENIN RANK ANALYSIS\n")
dataTable_nar = pd.read_excel("configurationsResults_Scenario0_analysis_sub_Nar.xlsx", sheet_name="Product_ratios", engine="openpyxl")
dataTable_nar = dataTable_nar[dataTable_nar["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD
dataTable_nar = when_death_starts(dataTable_nar)

fitness_ranks_set_nar = ((0, 8), (10, 16), (25, 35), (35, 55), (60, 85), (120, 146))  # Modificar estos valores, ordenar rangos de menor a mayor
describe_fitness_ranks(fitness_ranks_set_nar, dataTable_nar, descr_columns = ["FinalSucr", "NH4_mM", "pi_mM", "DT_cycles_init"], ref_column = "Nar_mM")


# -----------------------------------------------------------------------------
# BOXPLOTS with last analysis
# -----------------------------------------------------------------------------

configResults_fitFunc = organize_fitness_ranks(dataTable_fitFunc, fitness_ranks_set_fitFunc, ref_column = "fitFunc")
configResults_nar = organize_fitness_ranks(dataTable_nar, fitness_ranks_set_nar, ref_column = "Nar_mM")
# print(configResults_fitFunc)
# print(configResults_nar)


# BoxPlot display
sns.set_theme(style="darkgrid")
sns.set_context('paper', font_scale=1.0, rc={'line.linewidth': 2.5, 
                'font.sans-serif': [u'Times New Roman']})


# -----------------------------------------------------------------------------
if not os.path.isdir("DeadTracking_plots"):
    os.mkdir("DeadTracking_plots")  # Create "DeadTracking_plots" directory
os.chdir("DeadTracking_plots")
# -----------------------------------------------------------------------------

# BoxPlots with x (fitFunc)
# myplt.basic_boxplot(configResults_fitFunc, "Rank", "FinalSucr", 'Fitness Ranks', 'Final Sucr (mM)', "FinalSucr_fitFunc_Boxplot")
# myplt.basic_boxplot(configResults_fitFunc, "Rank", "NH4_mM", 'Fitness Ranks', 'Final NH4 (mM)', "FinalNH4_fitFunc_Boxplot")
# myplt.basic_boxplot(configResults_fitFunc, "Rank", "pi_mM", 'Fitness Ranks', 'Final Pi (mM)', "FinalPi_fitFunc_Boxplot")
# myplt.basic_boxplot(configResults_fitFunc, "Rank", "DT_cycles_init", 'Fitness Ranks', 'Dead Init Cycle', "DeadInitCycle_fitFunc_Boxplot")

# ScatterPlots with x (fitFunc)
myplt.basic_scatter(configResults_fitFunc, "Rank", "FinalSucr", 'Fitness Ranks', 'Final Sucr (mM)', "FinalSucr_fitFunc_scatter")
myplt.basic_scatter(configResults_fitFunc, "Rank", "NH4_mM", 'Fitness Ranks', 'Final NH4 (mM)', "FinalNH4_fitFunc_scatter")
myplt.basic_scatter(configResults_fitFunc, "Rank", "pi_mM", 'Fitness Ranks', 'Final Pi (mM)', "FinalPi_fitFunc_scatter")
myplt.basic_scatter(configResults_fitFunc, "Rank", "DT_cycles_init", 'Fitness Ranks', 'Dead Init Cycle', "DeadInitCycle_fitFunc_scatter")


# BoxPlots with x (Nar_mM)
# myplt.basic_boxplot(configResults_nar, "Rank", "FinalSucr", 'Fitness Ranks', 'Final Sucr (mM)', "FinalSucr_NAR_Boxplot")
# myplt.basic_boxplot(configResults_nar, "Rank", "NH4_mM", 'Fitness Ranks', 'Final NH4 (mM)', "FinalNH4_NAR_Boxplot")
# myplt.basic_boxplot(configResults_nar, "Rank", "pi_mM", 'Fitness Ranks', 'Final Pi (mM)', "FinalPi_NAR_Boxplot")
# myplt.basic_boxplot(configResults_nar, "Rank", "DT_cycles_init", 'Fitness Ranks', 'Dead Init Cycle', "DeadInitCycle_NAR_Boxplot")

# BoxPlots with x (Nar_mM)
myplt.basic_scatter(configResults_nar, "Rank", "FinalSucr", 'Fitness Ranks', 'Final Sucr (mM)', "FinalSucr_NAR_scatter")
myplt.basic_scatter(configResults_nar, "Rank", "NH4_mM", 'Fitness Ranks', 'Final NH4 (mM)', "FinalNH4_NAR_scatter")
myplt.basic_scatter(configResults_nar, "Rank", "pi_mM", 'Fitness Ranks', 'Final Pi (mM)', "FinalPi_NAR_scatter")
myplt.basic_scatter(configResults_nar, "Rank", "DT_cycles_init", 'Fitness Ranks', 'Dead Init Cycle', "DeadInitCycle_NAR_scatter")


os.chdir("..")


# Ampliar escala de gráficos y/o considerar outliers












