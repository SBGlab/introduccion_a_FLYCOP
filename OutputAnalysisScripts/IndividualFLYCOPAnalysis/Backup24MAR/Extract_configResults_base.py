#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 00:29:22 2021

@author: Iván Martín Martín
"""

# Adaptar descripción docstring
# PENDIENTE COMPROBAR SIMPLIFICACIÓN INCLUIDA: columna SD (1, 0) + revisar script
# PENDIENTE ADAPTACIÓN PLOTTING

"""
DESCRIPTION

    Script for output analysis which calculates:
        ratio NAR_pCA
        ratio finalEc_finalKt
        
    Moreover, the script generates the corresponding plots of:
            ratio NAR_pCA vs. fitFunc
            ratio finalEc_finalKT vs. fitFunc
            
            final pCA vs. fitFunc
            final NAR vs. fitFunc
        
        These plots are generated:
            (a) For all configurations (ZeroDivisionError, SD excessive - included) - Folder ./Plots
            (b) For those configurations that fulfil the SD restriction - Folder: ./Plots_no0fitness
        
            
UTILITIES THAT MIGHT BE USED WITHIN THIS SCRIPT:  
    
        (a) Changing separator character (more than 1 '\t' for just 1 '\t')
                
EXPECTED INPUT

    "configurationsResults_Scenario0_sorted.txt" or "configurationsResults_Scenario0.txt"
    Please, change the name of input file if required.
    
OUTPUT

    Folder: ./Plots
        "configurationsResults_Scenario0_analysis.txt"  
        "configurationsResults_Scenario0_analysis.xlxs"  
        "configResults_NARpCAr.png"
        "configResults_NARpCA_fitness.png"
        "configResults_finalBiomass.png"
    
    Folder: ./Plots_no0fitness
        
    
NOTE THAT:
    
        Code lines where a change might be eventually required are marked as POTENTIAL CHANGE.
        
        The columns in 'configurationsResults_Scenario0_analysis.txt' are expected to be organised as follows:
            Fitness_function   configuration   fitness   sd   IntermediateProduct   FinalBiomass1   FinalProduct   FinalBiomass2   endCycle
            
            If organised otherwise, feel free to adapt the current script to suit your purposes.    
        
"""

import re
import pandas as pd
import os.path

scripts_path = os.getcwd()
os.chdir("../Utilities")
import Plotting as myplt

os.chdir(scripts_path)  # Creo que esto va a fallar, hace falta: os.chdir("../IndividualFLYCOPAnalysis")
path = "../Project4_EcPp2_M9adjusted/100SMAC10"
os.chdir(path)

# -----------------------------------------------------------------------------
# UTILITY FOR ELIMINATING DUPLICATE (repeated) HEADERS
# INPUT: input_file, name_corrected_file
# -----------------------------------------------------------------------------
def duplicate_headers(input_file, name_corrected_file):
    output = open(name_corrected_file, "w")
    with open(input_file, "r") as file:
        lines = file.readlines()
        output.write(lines[0])
        
        for line in lines:
            line = line.strip("\n").split("\t")
            if line[0] != "Fitness_function":
                output.write(("\t").join(line)+"\n")
        
    output.close()
    os.remove(input_file)
    return output
        
# -----------------------------------------------------------------------------
# UTILITY FOR CHANGING SEPARATOR CHARACTER in input file: more than 2 '\t' to just one '\t'
# Potential optimization?
# INPUT: input_file, name for the corrected file
# -----------------------------------------------------------------------------
def change_sep_char(input_file, name_corrected_file):
    output = open(name_corrected_file, "w")
    with open(input_file, "r") as file:
        lines = file.readlines()
        
        for line in lines:
            line_copy = re.sub("[\t]{2,5}", "\t", line)
            output.write(line_copy)
            
    output.close()
    os.remove(input_file)
    return output
    

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# SCRIPT CODE
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
      
    
# ORIGINAL DATAFRAME & ADAPTATIONS
# =============================================================================

final_file = "configurationsResults_Scenario0.txt"  # CHANGE name
# corrected_name = "configurationsResults_Scenario0_corrected.txt"

# CHANGING SEPARATOR CHARACTER
# final_file = change_sep_char("configurationsResults_Scenario0.txt", corrected_name)

# REMOVE DUPLICATE HEADERS
# final_file = duplicate_headers("configurationsResults_Scenario0.txt", corrected_name)

# =============================================================================

with open(final_file, "r") as newfile:
    
    # DATAFRAME
    # ---------
    configResults = pd.read_csv(newfile, sep="\t", header="infer")
    # print(configResults[configResults["fitFunc"] == 0])

    
    # CLASSIFY RECORDS DEPENDING ON SD: higher or lower than (0.1)*(fitFunc)
    # No 'ZeroDivisionError' in this script since these configurations are not included in 'configurationsResults_Scenario0.txt'
    # ------------------------------------------
    configResults["ID_SD"] = 0

    for row in configResults.itertuples():   # row[0] = Index Number
        
        if configResults.loc[row[0], "sd"] > (0.1)*(configResults.loc[row[0], "fitFunc"]):
            configResults.loc[row[0], "ID_SD"] = 1
    
    
    # Automatically detect column names
    column_names = list(configResults)
    # print(column_names)
    
    
    # INCLUDE THOSE DESIRED COLUMNS FROM THE OTHER DATATABLE OF INTEREST FOR THE FLYCOP RUN UNDER STUDY
    # -------------------------------------------------------------------------
    # dataTable_ratios = pd.read_excel("dataTable_AcceptedRatios_SDlt.xlsx", sheet_name="Uptake_initBiomass_r", engine="openpyxl")
    # column_to_export = "column_to_export"
    # configResults[column_to_export] = dataTable_ratios[column_to_export]
    # -------------------------------------------------------------------------
    
    
    # SORT BY ref_column: 'ID_SD', 'fitness' unless otherwise indicated 
    # ----------------------
    configResults = configResults.sort_values(by=['ID_SD', 'fitFunc'], ascending=[True, False])  # CHANGE sorting_order if desired
    # print(configResults["fitFunc"])
    
    
    
# =============================================================================
# COMPUTE RATIOS
# Note that the names of metabolites for uptake rates and microbes names have to be CHANGED whenever necessary
# =============================================================================
    
    # ratio NAR / pCA
    configResults_copy = configResults.copy()  # Avoid 'SettingWithCopyWarning'
    try:
        configResults_copy["Nar_mM_pCA_mM"] = round((configResults_copy["Nar_mM"] / configResults_copy["pCA_mM"]), 4)
    except ZeroDivisionError:
        configResults_copy["Nar_mM_pCA_mM"] = "NaN"
        
    # ratio finalEc / finalKT
    try:
        configResults_copy["FinalEc_gL_FinalKT_gL"] = round((configResults_copy["FinalEc_gL"] / configResults_copy["FinalKT_gL"]), 4)
    except ZeroDivisionError:
        configResults_copy["FinalEc_gL_FinalKT_gL"] = "NaN"
            
# POTENTIAL CHANGE FOR NAMES if a different consortium is used


        
# =============================================================================
# FINAL DATAFRAME COPY with ratios to EXCEL
# =============================================================================
# Automatically detect column names
column_names = list(configResults_copy)
# print(column_names)


# DATAFRAME TO EXCEL: ordered by fitFunc (descending)
configResults_copy.to_excel("configurationsResults_Scenario0_analysis.xlsx", sheet_name="Product_ratios", header=True, index=True, index_label=None)


# SAME DATAFRAME TO EXCEL: ordered by naringenin production (descending)
# configResults_nar = configResults_copy.sort_values(by=['ID_SD', 'Nar_mM'], ascending=[True, False])
# configResults_nar.to_excel("configurationsResults_Scenario0_analysis_Nar.xlsx", sheet_name="Product_ratios", header=True, index=True, index_label=None)


# -----------------------------------------------------------------------------
# Subset of configurations where ID_SD == 0; i.e. not included SD excessive configurations 
configResults_copy_no0fitness = configResults_copy[configResults_copy["ID_SD"] == 0]
# -----------------------------------------------------------------------------



# =============================================================================
# ASSOCIATED PLOTS with configurations in which fiFunc = 0, INCLUDED (SD excessive)
# =============================================================================
if not os.path.isdir("Plots"):
    os.mkdir("Plots")  # Create "Plots" directory
os.chdir("Plots")
# -----------------------------------------------------------------------------

# Ratios vs. fitFunc
myplt.two_plots_twolabels("fitFunc", "Nar_mM_pCA_mM", "FinalEc_gL_FinalKT_gL", configResults_copy, "configResults_NARpCAr_finalBiomass_limNut1")

# Final Products vs. fitFunc
myplt.two_plots_twolabels("fitFunc", "pCA_mM", "Nar_mM", configResults_copy, "configResults_products_fitness_limNut1")

# Final Biomass vs. fitFunc
myplt.two_plots_twolabels("fitFunc", "FinalEc_gL", "FinalKT_gL", configResults_copy, "configResults_finalBiomass_limNut1")

os.chdir("..")


# =============================================================================
# ASSOCIATED PLOTS with configurations in which fiFunc = 0, NOT INCLUDED (SD excessive)
# =============================================================================
if not os.path.isdir("Plots_no0fitness"):
    os.mkdir("Plots_no0fitness")  # Create "Plots_no0fitness" directory
os.chdir("Plots_no0fitness")
# -----------------------------------------------------------------------------

# Ratios vs. fitFunc
myplt.two_plots_twolabels("fitFunc", "Nar_mM_pCA_mM", "FinalEc_gL_FinalKT_gL", configResults_copy_no0fitness, "configResults_NARpCAr_finalBiomass_limNut_no0fitness1")

# Final Products vs. fitFunc
myplt.two_plots_twolabels("fitFunc", "pCA_mM", "Nar_mM", configResults_copy_no0fitness, "configResults_products_fitness_limNut_no0fitness1")

# Final Biomass vs. fitFunc
myplt.two_plots_twolabels("fitFunc", "FinalEc_gL", "FinalKT_gL", configResults_copy_no0fitness, "configResults_finalBiomass_limNut_no0fitness1")

os.chdir("..")












