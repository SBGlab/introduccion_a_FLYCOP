#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:02:18 2020

@author: Iván Martín Martín


DESCRIPTION - INPUT / OUTPUT PARAMETER COMPARISON 

    1. ACCEPTABLE CONFIGS COMPARISON
    --------------------------------
    Acceptable configurations: 
        * With biomass loss ("DeadTracking" == 1)
        * Without biomass loss ("DeadTracking" == 0)
        
    (Categorical comparison of these 4 groups in plotting)
    
    
    2. FULL COMPARISON
    ------------------
    - Acceptable configurations
        * With biomass loss
        * Without biomass loss
    - NonOptimalConfig_Error
        * With biomass loss
        * Without biomass loss
        
    (Categorical comparison of these 4 groups in plotting)

    ------------------------------------------------------    
    ------------------------------------------------------    
    Input / Output Parameters evaluated are (current script):
        - Uptake Rates ratio
        - Initial Biomass ratio
        - (...)
        
    
EXPECTED INPUT

    'configurationsResults_Scenario0_acceptableBiomassLoss_analysis.xlsx'
    'configurationsResults_Scenario0_COMPLETE.xlsx'
        
OUTPUT

    Plots at ./IndivComparison_biomassLoss
    Plots at ./FullComparison_Acc_NonOptimalConfig_Error
    
NOTE THAT:
    
    The variables to be displayed can be adapted if desired.
        (CHANGE keyword)
    
"""

# import re
import pandas as pd
import os.path
import seaborn as sns

scripts_path = os.getcwd()
os.chdir("../Utilities")
import Plotting as myplt
import FitnessRanks as fitRanks

os.chdir(scripts_path)
path = "../../Project3_EcPp2_LimNut_M9/NP_LimNutFinal_29Mar/NP3"  # CHANGE path
os.chdir(path)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ACCEPTABLE CONFIGS COMPARISON
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# ORIGINAL DATAFRAME
dataTable = pd.read_excel("configurationsResults_Scenario0_acceptableBiomassLoss_analysis.xlsx", sheet_name="Product_ratios", engine="openpyxl") 


# BOXPLOT & Scatter REPRESENTATION
# Discrete representation by biomass loss: 'x' categorical variable with values 0 (No Biomass Loss) and 1 (Biomass Loss)
# -----------------------------------------------------------------------------

# Special BoxPlot display
sns.set_theme(style="darkgrid")
sns.set_context('paper', font_scale=1.0, rc={'line.linewidth': 2.5, 
                'font.sans-serif': [u'Times New Roman']})


# -----------------------------------------------------------------------------
if not os.path.isdir("IndivComparison_biomassLoss"):
    os.mkdir("IndivComparison_biomassLoss")  # Create "IndivComparison_biomassLoss" directory
os.chdir("IndivComparison_biomassLoss")
# -----------------------------------------------------------------------------

# POTENTIAL CHANGE FOR NAMES if a different consortium is used
ratios = ["sucr1_frc2", "Ecbiomass_KTbiomass"]  # Names for new column_ratios to be plotted, in order
input_parameters = ["sucr1_IP", "frc1_IP", "EcInit_IP", "KTInit_IP", "NH4_Ec", "NH4_KT", "Pi_Ec", "Pi_KT"]
output_parameters = ["fitFunc", "Nar_mM", "pCA_mM", "FinalEc_gL", "FinalKT_gL", "FinalSucr"]

x_axis = 'DeadTracking'
y_axis1 = 'Ratio of Uptake Rates'
y_axis2 = 'Ratio of Initial Biomass'

name1 = "UptakeRatesRatio_Boxplot"
title1 = "Carbon Uptake Rates ratio"
name2 = "InitBiomassRatio_Boxplot"
title2 = "Initial Biomass ratio"


# BOXPLOT + SCATTER
# -----------------

# Basic Input Ratios: carbon sources and initial biomass
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", ratios[0], x_axis, y_axis1, name1, title1)
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", ratios[1], x_axis, y_axis2, name2, title2)


# NH4 and Pi uptake rates
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", input_parameters[4], x_axis, "NH4 uptake by E.coli", "NH4uptake_Ec_boxplot", "NH4 uptake - E.coli")
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", input_parameters[5], x_axis, "NH4 uptake by P.putida", "NH4uptake_KT_boxplot", "NH4 uptake - P.putida")
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", input_parameters[6], x_axis, "Pi uptake by E.coli", "Piuptake_Ec_boxplot", "Pi uptake - E.coli")
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", input_parameters[7], x_axis, "Pi uptake by P.putida", "Piuptake_KT_boxplot", "Pi uptake by P.putida")

# Final Sucrose
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", output_parameters[5], x_axis, "[Sucrose] (mM)", "finalSucrose_boxplot", "Final Sucrose")


# Final Biomass
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", output_parameters[3], x_axis, "E.coli biomass", "FinalEcBiomass_boxplot", "Final E.coli biomass")
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", output_parameters[4], x_axis, "P.putida biomass", "FinalKTBiomass_boxplot", "Final P.putida biomass")

# Final Products
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", output_parameters[1], x_axis, "[Naringenin] (mM)", "Nar_boxplot", "Final naringenin")
myplt.basic_boxplot_scatter(dataTable, "DeadTracking", output_parameters[2], x_axis, "[pCA] (mM)", "pCA_boxplot", "Final pCA")

os.chdir("..")


# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# FULL COMPARISON - categorical plotting
# Acceptable configurations (biomass loss vs. no-biomass loss) + NonOptimalConfig_Error (biomass loss vs. no-biomass loss)
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------

complete_df = pd.read_excel("configurationsResults_Scenario0_COMPLETE.xlsx", sheet_name="Complete", engine="openpyxl")


# -----------------------------------------------------------------------------
if not os.path.isdir("FullComparison_Acc_NonOptimalConfig_Error"):
    os.mkdir("FullComparison_Acc_NonOptimalConfig_Error")  # Create "FullComparison_Acc_NonOptimalConfig_Error" directory
os.chdir("FullComparison_Acc_NonOptimalConfig_Error")
# -----------------------------------------------------------------------------

# POTENTIAL CHANGE FOR NAMES if a different consortium is used (SAME NAMES AS BEFORE)
ratios = ["sucr1_frc2", "Ecbiomass_KTbiomass"]
input_parameters = ["sucr1_IP", "frc1_IP", "EcInit_IP", "KTInit_IP", "NH4_Ec", "NH4_KT", "Pi_Ec", "Pi_KT"]
output_parameters = ["fitFunc", "Nar_mM", "pCA_mM", "FinalEc_gL", "FinalKT_gL", "FinalSucr", "NH4_mM", "pi_mM", "FinalO2"]

x_axis = 'Acceptable vs. Error'
y_axis1 = 'Ratio of Uptake Rates'
y_axis2 = 'Ratio of Initial Biomass'

name1 = "UptakeRatesRatio_Boxplot"
title1 = "Carbon Uptake Rates ratio"
name2 = "InitBiomassRatio_Boxplot"
title2 = "Initial Biomass ratio"


# BOXPLOT + SCATTER
# -----------------

# Basic Input Ratios: carbon sources and initial biomass
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", ratios[0], x_axis, y_axis1, name1, title1)
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", ratios[1], x_axis, y_axis2, name2, title2)


# Carbon Uptakes and Initial Biomass
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[0], x_axis, "Sucr uptake by E.coli", "Sucruptake_Ec_boxplot", "Sucr uptake - E.coli")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[1], x_axis, "Frc uptake by P.putida", "Frcuptake_KT_boxplot", "Frc uptake - P.putida")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[2], x_axis, "Initial Biomass by E.coli", "InitBiom_Ec_boxplot", "Initial Biomass - E.coli")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[3], x_axis, "Initial Biomass by P.putida", "InitBiom_KT_boxplot", "Initial Biomass - P.putida")

# NH4 and Pi uptake rates
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[4], x_axis, "NH4 uptake by E.coli", "NH4uptake_Ec_boxplot", "NH4 uptake - E.coli")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[5], x_axis, "NH4 uptake by P.putida", "NH4uptake_KT_boxplot", "NH4 uptake - P.putida")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[6], x_axis, "Pi uptake by E.coli", "Piuptake_Ec_boxplot", "Pi uptake - E.coli")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", input_parameters[7], x_axis, "Pi uptake by P.putida", "Piuptake_KT_boxplot", "Pi uptake by P.putida")

# Final Sucrose, NH4, Pi, O2
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[5], x_axis, "[Sucrose] (mM)", "finalSucrose_boxplot", "Final Sucrose")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[6], x_axis, "[NH4] (mM)", "finalNH4_boxplot", "Final NH4")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[7], x_axis, "[Pi] (mM)", "finalPi_boxplot", "Final Pi")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[8], x_axis, "[O2] (mM)", "finalO2_boxplot", "Final O2")


# FITNESS (in this case, without discarding SD excessive configs)
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[0], x_axis, "Fitness (mM / gL-1)", "fitness_boxplot", "Fitness (mM / gL-1)")
myplt.basic_boxplot_scatter_upper_ylim(complete_df, "ConfigKey", output_parameters[0], x_axis, "Fitness (mM / gL-1)", "fitness_boxplot_YLIM", "Fitness (mM / gL-1)", 200)


# Final Biomass
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[3], x_axis, "E.coli biomass", "FinalEcBiomass_boxplot", "Final E.coli biomass")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[4], x_axis, "P.putida biomass", "FinalKTBiomass_boxplot", "Final P.putida biomass")

# Final Products
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[1], x_axis, "[Naringenin] (mM)", "Nar_boxplot", "Final naringenin")
myplt.basic_boxplot_scatter(complete_df, "ConfigKey", output_parameters[2], x_axis, "[pCA] (mM)", "pCA_boxplot", "Final pCA")

os.chdir("..")









































