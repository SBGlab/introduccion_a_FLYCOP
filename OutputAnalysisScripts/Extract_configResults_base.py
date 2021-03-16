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
import matplotlib.pyplot as plt
import os.path
import subprocess
path = "../Project4_EcPp2_M9adjusted/100SMAC10"
os.chdir(path)

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
      
    
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# SCRIPT CODE
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    
# ORIGINAL DATAFRAME
# =============================================================================

final_file = "configurationsResults_Scenario0.txt"  # POTENTIAL CHANGE

# CHANGING SEPARATOR CHARACTER
# corrected_name = input("Name for the corrected file (please, no blank spaces): ")  # corrected_configResults.txt
# change_sep_char(file, corrected_name)
# final_file = corrected_name

# -----------------------------------------------------------------------------

with open(final_file, "r") as newfile:
    
    # DATAFRAME
    # ---------
    configResults = pd.read_csv(newfile, sep="\t", header="infer")
    # print(configResults)
    
    
    # CLASSIFY RECORDS DEPENDING ON SD: higher or lower than (0.1)*(fitFunc)
    # ------------------------------------------
    configResults["ID_SD"] = 0

    for row in configResults.itertuples():   # row[0] = Index Number
        
        if configResults.loc[row[0], "sd"] > (0.1)*(configResults.loc[row[0], "fitness"]):
            configResults.loc[row[0], "ID_SD"] = 1
    
    
    # Automatically detect column names
    column_names = list(configResults)
    print(column_names)
    
    
    # ORDERING BY ref_column: 'ID_SD', 'fitness' unless otherwise indicated 
    # ----------------------
    configResults = configResults.sort_values(by=['ID_SD', 'fitFunc'], ascending=[True, False])
    # print(configResults["fitFunc"])
    
    
    # ratio NAR / pCA
    configResults_copy = configResults.copy()  # Avoid 'SettingWithCopyWarning'
    try:
        configResults_copy[str(column_names[6])+"_"+str(column_names[4])] = round((configResults_copy[column_names[6]] / configResults_copy[column_names[4]]), 4)
    except ZeroDivisionError:
        configResults_copy[str(column_names[6])+"_"+str(column_names[4])] = "NaN"
        
    # ratio finalEc / finalKT
    try:
        configResults_copy[str(column_names[5])+"_"+str(column_names[7])] = round((configResults_copy[column_names[5]] / configResults_copy[column_names[7]]), 4)
    except ZeroDivisionError:
        configResults_copy[str(column_names[5])+"_"+str(column_names[7])] = "NaN"
            

        
# -----------------------------------------------------------------------------   
# FINAL DATAFRAME COPY with ratios to CSV (plain text file)
# -----------------------------------------------------------------------------
# Automatically detect column names
column_names = list(configResults_copy)
# ['Fitness_function', 'configuration', 'fitness(mM)', 'sd(mM)', 'pCA(mM)', 'FinalEc(gL-1)', 'Nar(mM)', 'FinalKT(gL-1)', 'endCycle', 'NH4(mM)', 'pi(mM)', 'Nar(mM)_pCA(mM)', 'FinalEc(gL-1)_FinalKT(gL-1)']
configResults_copy.to_csv("configurationsResults_Scenario0_analysis.txt", sep='\t', header=True, index=True, index_label=None)
configResults_copy.to_excel("configurationsResults_Scenario0_analysis.xlsx", sheet_name="Product_ratios", header=True, index=True, index_label=None)
# os.remove(corrected_name)  # If 'change_sep_char' has been used

# ASSOCIATED PLOTS
# -----------------------------------------------------------------------------
if not os.path.isdir("Plots"):
    os.mkdir("Plots")  # Create "Plots" directory
# -----------------------------------------------------------------------------

# FIGURE 1
# Base Figure: set desired graphic format 
fig = plt.figure(num=2, clear=True, figsize=(7, 7))

# NAR_pCA ratio vs. fitFunc
plt.subplot(211)   # Change if next plot is also made
plt.xlabel(column_names[2])  
plt.ylabel(column_names[9])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[9]], '^g')  

# (Final) Biomass ratio vs. fitFunc
plt.subplot(212)
plt.xlabel(column_names[2])  
plt.ylabel(column_names[10])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[10]], '^c')  

fig.savefig("Plots/configResults_NARpCAr.png")  # If it is desired to save the figure
plt.close(fig)    
# -----------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------
# FIGURE 2
# Base Figure: set desired graphic format 
fig2 = plt.figure(num=3, clear=True, figsize=(7, 7))

# final pCA(mM) vs. fitFunc
plt.subplot(211)
plt.xlabel(column_names[2])  
plt.ylabel(column_names[4])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[4]], '^g')  

# final NAR(mM) vs. fitFunc
plt.subplot(212)
plt.xlabel(column_names[2])  
plt.ylabel(column_names[6])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[6]], '^c')  

fig2.savefig("Plots/configResults_NARpCA_fitness.png")  # If it is desired to save the figure
plt.close(fig2)    
# -----------------------------------------------------------------------------
    

# -----------------------------------------------------------------------------
# FIGURE 3
# Base Figure: set desired graphic format 
fig3 = plt.figure(num=4, clear=True, figsize=(7, 7))

# final EcBiomass vs. fitFunc
plt.subplot(211)
plt.xlabel(column_names[2])  
plt.ylabel(column_names[5])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[5]], '^g')  

# final KTBiomass vs. fitFunc
plt.subplot(212)
plt.xlabel(column_names[2])  
plt.ylabel(column_names[7])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[7]], '^c')     
    
fig3.savefig("Plots/configResults_finalBiomass.png")  # If it is desired to save the figure
plt.close(fig3)  
# -----------------------------------------------------------------------------









