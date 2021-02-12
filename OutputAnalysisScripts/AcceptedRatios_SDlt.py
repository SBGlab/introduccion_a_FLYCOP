#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Dec 27 23:02:18 2020

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Script for output analysis which calculates:
        ratio of carbon substrate uptake rates (First microorganism / Second microorganism)
        ratio of biomass growth (First microorganism / Second microorganism)
        
    Moreover, the script generates the corresponding plots of:
        ratio of substrate uptake rates (First microorganism / Second microorganism) vs. fitFunc
        ratio of biomass growth (First microorganism / Second microorganism) vs. fitFunc
    
EXPECTED INPUT

    'dataTable_Scenario0.txt' from ./xxx_FLYCOPdataAnalysis folder
        
OUTPUT

    "dataTable_AcceptedRatios_SDlt.txt"   
    "dataTable_AcceptedRatios_SDlt.xlxs"
    "AccRatios_UptakeR.png"
    "AccRatios_initBiomass.png"
    
NOTE THAT:
    
        The columns in 'dataTable_Scenario0.txt' are expected to be organised as follows:
            SubstrateUptake1   Biomass1   SubstrateUptake2   Biomass2   SD   fitFunction
            
        If organised otherwise, feel free to adapt the current script to suit your purposes.
    
"""


# import re
import pandas as pd
import matplotlib.pyplot as plt
import os.path
path = "../Project4_EcPp2_M9adjusted/100SMAC10"  # Change to the desired path
os.chdir(path)


# ORIGINAL TABLE: dataTable_Scenario0.txt
# -----------------------------------------------------------------------------
dataTable = pd.read_csv("dataTable_Scenario0.txt", sep="\t", header="infer")
print(dataTable)


# TABLE SUBSET: SD < 10% * (fitFunc)
# -----------------------------------------------------------------------------
accepted_ratios = dataTable[dataTable["sd"] < (0.1)*(dataTable["fitFunc"])] 
# print(accepted_ratios)


# Automatically detect column names
column_names = list(accepted_ratios)
print(column_names)

# UPTAKE RATES RATIO
accepted_ratios_copy = accepted_ratios.copy()  # Avoid 'SettingWithCopyWarning'
try:
    accepted_ratios_copy[str(column_names[0])+"_"+str(column_names[2])] = round((accepted_ratios_copy[column_names[0]] / accepted_ratios_copy[column_names[2]]), 4)
except ZeroDivisionError:
    accepted_ratios_copy[str(column_names[0])+"_"+str(column_names[2])] = "NaN"

# BIOMASS RATIO
try:
    accepted_ratios_copy[str(column_names[1])+"_"+str(column_names[3])] = round((accepted_ratios_copy[column_names[1]] / accepted_ratios_copy[column_names[3]]), 4)
except:
    accepted_ratios_copy[str(column_names[1])+"_"+str(column_names[3])] = "NaN"
    
    
# FINAL DATAFRAME COPY with ratios to CSV (plain text file)
# -----------------------------------------------------------------------------
# print(accepted_ratios_copy)
# Automatically detect column names
column_names = list(accepted_ratios_copy)
# accepted_ratios_copy.to_csv("dataTable_AcceptedRatios_SDlt.txt", sep='\t', header=True, index=True, index_label=None)
accepted_ratios_sorted_copy = accepted_ratios_copy.sort_values(by="fitFunc", ascending=False)
accepted_ratios_sorted_copy.to_excel("dataTable_AcceptedRatios_SDlt.xlsx", sheet_name="Uptake_initBiomass_r", header=True, index=True, index_label=None)


# ASSOCIATED PLOTS
# -----------------------------------------------------------------------------
if not os.path.isdir("Plots"):
    os.mkdir("Plots")  # Create "Plots" directory
# -----------------------------------------------------------------------------

# FIGURE 1
# Base Figure: set desired graphic format 
# plt.clf()
fig1 = plt.figure(num=0, clear=True, figsize=(7, 7))

# Uptake Rates ratio vs. fitFunc
plt.subplot(211)
plt.xlabel(column_names[5])  
plt.ylabel(column_names[6])
plt.plot(accepted_ratios_copy[column_names[5]], accepted_ratios_copy[column_names[6]], '^g') 

# Uptake Rates ratio vs. fitFunc x2: subset to amplify y-axis scale
plt.subplot(212)
plt.xlabel(column_names[5])  
plt.ylabel(column_names[6])
subset_accepted_ratios_copy = accepted_ratios_copy[accepted_ratios_copy[column_names[6]] < 1]
plt.plot(subset_accepted_ratios_copy[column_names[5]], subset_accepted_ratios_copy[column_names[6]], '^g')  

fig1.savefig("Plots/AccRatios_UptakeR.png")  # If it is desired to save the figure
plt.close(fig1)


# FIGURE 2
# Base Figure: set desired graphic format 
# plt.clf()
fig2 = plt.figure(num=1, clear=True, figsize=(7, 7))

# Biomass ratio vs. fitFunc
plt.subplot(111)
plt.xlabel(column_names[5])  
plt.ylabel(column_names[7])
plt.plot(accepted_ratios_copy[column_names[5]], accepted_ratios_copy[column_names[7]], '^c')  

fig2.savefig("Plots/AccRatios_initBiomass.png")  # If it is desired to save the figure
plt.close(fig2)









