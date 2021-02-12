#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 00:29:22 2021

@author: Iván Martín Martín
"""

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
        
        Limiting nutrient conc. vs. fitFunc 
        (where final conc != 0 mM, to easily find the fitness value for these particular cases)

            
UTILITIES THAT MIGHT BE USED WITHIN THIS SCRIPT:  
    
        (a) Changing separator character (more than 1 '\t' for just 1 '\t')
        (b) Ordering the set of records, in descendent order, by the reference column desired
                
EXPECTED INPUT

    "configurationsResults_Scenario0_sorted.txt" or "configurationsResults_Scenario0"
    Please, change the name of input file if required.
    
OUTPUT

    "configurationsResults_Scenario0_analysis.txt"  
    "configurationsResults_Scenario0_analysis.xlxs"  
    
    "configResults_NARpCAr_initBiomass_limNut.png"
    "configResults_NARpCA_fitness_limNut.png"
    "Plots/configResults_"+limNut_name+"_limNut.png"
    "configResults_finalBiomass_limNut.png"
    
NOTE THAT:
    
        The columns in 'configurationsResults_Scenario0_analysis.txt' are expected to be organised as follows:
            Fitness_function   configuration   fitness   sd   IntermediateProduct   FinalBiomass1   FinalProduct   FinalBiomass2   endCycle   LimNut1   LimNut2
            
        If organised otherwise, feel free to adapt the current script to suit your purposes.    
    
"""

import re
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import subprocess
path = "../Nutrientes/NutOpt/100SMAC5P_fitOK"
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
    
# -----------------------------------------------------------------------------
# UTILITY FOR ORDERING RECORDS in ascending order, according to the reference column ('column_ref') desired
# -----------------------------------------------------------------------------
def order_records_by_fitness(input_dataframe, column_ref):
    ordered_dataframe = input_dataframe.sort_values(by=column_ref, ascending=False)  
    return ordered_dataframe
   
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# SCRIPT CODE
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    
# ORIGINAL DATAFRAME
# =============================================================================
# CHANGING SEPARATOR CHARACTER
# nondup_file = duplicate_headers("configurationsResults_Scenario0_nonAdapted.txt", "configurationsResults_Scenario0.txt")  # In case of repeated headers, activate line
wish_to_change_sep_char = (input("Would you like to use the change_sep_char utility? (EXPECTED ANSWER: boolean): ")).lower()

if wish_to_change_sep_char != "no":
    file = "configurationsResults_Scenario0.txt"  # POTENTIAL CHANGE
    corrected_name = input("Name for the corrected file (please, no blank spaces): ")  # configurationsResults_Scenario0corrected.txt
    change_sep_char(file, corrected_name)
    final_file = corrected_name
else: 
    final_file = "configurationsResults_Scenario0.txt"  # POTENTIAL CHANGE
# -----------------------------------------------------------------------------

with open(final_file, "r") as newfile:
    
    # DATAFRAME
    # ---------
    configResults = pd.read_csv(newfile, sep="\t", header="infer")
    # print(configResults)
    
    # ORDERING BY ref_column
    # ----------------------
    wish_to_order = (input("Would you like to use the order_records_by_fitness utility? (EXPECTED ANSWER: boolean): ")).lower()
    if wish_to_order != "no":
        ref_column = input("Reference column for ordering (please, no blank spaces): ")  # fitness
        configResults = order_records_by_fitness(configResults, ref_column)
    # print(configResults)
    
    
    # SUPPRESS RECORDS WITH SD > (0.1) (fitFunc)
    # ------------------------------------------
    configResults = configResults[configResults["sd_mM"] < (0.1)*(configResults["fitness_mM"])] 
    
    # Automatically detect column names
    column_names = list(configResults)
    # ['Fitness_function', 'configuration', 'fitness(mM)', 'sd(mM)', 'pCA(mM)', 'FinalEc(gL-1)', 'Nar(mM)', 'FinalKT(gL-1)', 'endCycle', 'NH4(mM)', 'pi(mM)']
    
    
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
os.remove(corrected_name)


# ASSOCIATED PLOTS
# -----------------------------------------------------------------------------
# FIGURE 1
# Base Figure: set desired graphic format 
fig = plt.figure(num=5, clear=True, figsize=(7, 7))

# NAR_pCA ratio vs. fitFunc
plt.subplot(211)
plt.xlabel(column_names[2])  
plt.ylabel(column_names[11])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[11]], '^g')  

# (Final) Biomass ratio vs. fitFunc
plt.subplot(212)
plt.xlabel(column_names[2])  
plt.ylabel(column_names[12])
plt.plot(configResults_copy[column_names[2]], configResults_copy[column_names[12]], '^c')  

fig.savefig("Plots/configResults_NARpCAr_initBiomass_limNut.png")  # If it is desired to save the figure
plt.close(fig)    
# -----------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------
# FIGURE 2
# Base Figure: set desired graphic format 
fig2 = plt.figure(num=6, clear=True, figsize=(7, 7))

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

fig2.savefig("Plots/configResults_NARpCA_fitness_limNut.png")  # If it is desired to save the figure
plt.close(fig2)    
# -----------------------------------------------------------------------------
    
# -----------------------------------------------------------------------------
# FIGURE 3
# Base Figure: set desired graphic format 
fig3 = plt.figure(num=7, clear=True, figsize=(7, 7))

# limNut_name = input("Limiting nutrient (please, same name as in the original input file (column name)): ")  # NH4(mM) vs. pi(mM)
limNut_name = "pi_mM"

# LimitNut vs. fitFunc, in those cases when LimitNut != 0 (at the end)
limNut = configResults_copy[configResults_copy[limNut_name] != 0]
plt.subplot(111)
plt.xlabel(column_names[2])  
plt.ylabel(limNut_name)
plt.plot(limNut[column_names[2]], limNut[limNut_name], '^g')     
    
fig3.savefig("Plots/configResults_"+limNut_name+"_limNut.png")  # If it is desired to save the figure
plt.close(fig3)  
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# FIGURE 4
# Base Figure: set desired graphic format 
fig4 = plt.figure(num=8, clear=True, figsize=(7, 7))

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
    
fig4.savefig("Plots/configResults_finalBiomass_limNut.png")  # If it is desired to save the figure
plt.close(fig4)  
# -----------------------------------------------------------------------------










