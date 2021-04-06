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
        ratio of initial biomass (First microorganism / Second microorganism)
        
    Moreover, the script generates the corresponding plots:
            ratio of substrate uptake rates (First microorganism / Second microorganism) vs. fitFunc
            ratio of initial biomass (First microorganism / Second microorganism) vs. fitFunc
            
        These plots are generated:
            (a) For all configurations (ZeroDivisionError, SD excessive - included) - Folder ./Plots
            (b) For those configurations that fulfil the SD restriction - Folder: ./Plots_no0fitness
            
    
    FIRST PART OF THE SCRIPT
    ------------------------
    The script distinguishes between those configurations with an acceptable standard deviation (SD) vs. 
        those with excessive SD or those with a ZeroDivisionError for microbes death or exhaustion.
        An acceptable SD value would mean SD < (0.10)*(fitness)
        
        
    SECOND PART OF THE SCRIPT
    -------------------------
    Computing ratios and further interesting parameters. This code chunks could be adapted to
    suit the purposes of the consortiums under analysis, i.e. in case of a different number of microbes.
    Currently:
        
        * Ratio of (sucrose consumption / fructose consumption)
        * Ratio of (initial E.coli biomass / initial P.putida KT biomass)
    
    
    THIRD PART OF THE SCRIPT
    ------------------------
    1. Obtaining the final dataframe and exporting it to EXCEL
    2. Generating a partial dataframe with just those configurations (and related information) with an acceptable SD
    3. Plotting. For further information about each plotting utility, see Plotting.py
    
    
EXPECTED INPUT

    'dataTable_Scenario0.txt' from ./xxx_FLYCOPdataAnalysis folder
    'configurationsResults_Scenario0.txt' from ./xxx_FLYCOPdataAnalysis folder
        
OUTPUT

    "dataTable_AcceptedRatios_SDlt.txt"   
    "dataTable_AcceptedRatios_SDlt.xlxs"
    
    Folder: ./Plots
        "AccRatios_UptakeR_base.png"
        "AccRatios_UptakeR1.png"
        "AccRatios_UptakeR2.png"
        
        "AccRatios_initBiomass_base.png"
        "AccRatios_initBiomass1.png"
        "AccRatios_initBiomass2.png"
        
    
    Folder: ./Plots_no0fitness
        "AccRatios_UptakeR_base_no0fitness.png"
        "AccRatios_UptakeR_no0fitness1.png"
        "AccRatios_UptakeR_no0fitness2.png"
        
        "AccRatios_initBiomass_base_no0fitness.png"
        "AccRatios_initBiomass_no0fitness1.png"
        "AccRatios_initBiomass_no0fitness2.png"
    
    
NOTE THAT:
    
    Code lines where a change might be eventually required are marked as CHANGE.
    
    This script is currently adapted to the consortium for naringenin production, E.coli-P.putidaKT (2 microbes),
    where it calculates the ratio of carbon uptake rates between the two microbes and the ratio of initial biomass.
    
    Note that two different types of plots are obtained, given the script organization:
        
        - configurations in which fiFunc = 0, INCLUDED (SD excessive, ZeroDivisionError)
        - configurations in which fiFunc = 0, NOT INCLUDED (SD excessive, ZeroDivisionError)
        
        (Necessary adaptation in case of change: sections on "COMPUTE RATIOS" and "PLOTTING")
    
"""


# import re
import pandas as pd
import os.path

scripts_path = os.getcwd()
os.chdir("../Utilities")
import Plotting as myplt

os.chdir(scripts_path)  # Creo que esto va a fallar, hace falta: os.chdir("../IndividualFLYCOPAnalysis")

path = "../Project3_EcPp2_LimNut_M9/Nitrogen/M9200N"  # CHANGE path
os.chdir(path)


# -----------------------------------------------------------------------------
# ORIGINAL TABLE: dataTable_Scenario0.txt
# -----------------------------------------------------------------------------
dataTable = pd.read_csv("dataTable_Scenario0.txt", sep="\t", header="infer")
configResults = pd.read_csv("configurationsResults_Scenario0.txt", sep="\t", header="infer")
# print(dataTable)


# -----------------------------------------------------------------------------
# (1) CLASSIFY RECORDS DEPENDING ON SD: higher or lower than (0.1)*(fitFunc)
# (2) LOCATE RECORDS with fitness = 0.0 which constitute a ZeroDivisionError
# -----------------------------------------------------------------------------
dataTable["ID_SD"] = 0
dataTable["ZeroDivisionError"] = 0

for row_dataTable in dataTable.itertuples():
    if dataTable.loc[row_dataTable[0], "sd"] > (0.1)*(dataTable.loc[row_dataTable[0], "fitFunc"]):  # (1)
        dataTable.loc[row_dataTable[0], "ID_SD"] = 1  
        
    if dataTable.loc[row_dataTable[0], "fitFunc"] == 0:  # (2)
        sucr = float(row_dataTable[1])  # 'float' to obtain a float number, not an int
        EcBiomass = row_dataTable[2]
        frc = float(row_dataTable[3])
        KTbiomass = row_dataTable[4]
        config = str(sucr)+","+str(EcBiomass)+","+str(frc)+","+str(KTbiomass)
        
        # When a 'fitness = 0' configuration is not present in 'configurationsResults_Scenario0.txt', 
        # it means it constitutes a ZeroDivisionError
        dataTable.loc[row_dataTable[0], "ZeroDivisionError"] = 1
        for row_cR in configResults.itertuples():  
            if config == row_cR[2]:
                dataTable.loc[row_dataTable[0], "ZeroDivisionError"] = 0
                break



# -----------------------------------------------------------------------------
# COMPUTE RATIOS
# Note that the names of metabolites for uptake rates and microbes names have to be CHANGED whenever necessary
# -----------------------------------------------------------------------------

# Automatically detect column names
column_names = list(dataTable)


# UPTAKE RATES RATIO
ratiosDataframe = dataTable.copy()  # Avoid 'SettingWithCopyWarning'
try:
    ratiosDataframe["sucr1_frc2"] = round((ratiosDataframe["sucr1"] / ratiosDataframe["frc2"]), 4)
except ZeroDivisionError:
    ratiosDataframe["sucr1_frc2"] = "NaN"

# BIOMASS RATIO
try:
    ratiosDataframe["Ecbiomass_KTbiomass"] = round((ratiosDataframe["Ecbiomass"] / ratiosDataframe["KTbiomass"]), 4)
except:
    ratiosDataframe["Ecbiomass_KTbiomass"] = "NaN"
    
# POTENTIAL CHANGE FOR NAMES if a different consortium is used

    

# -----------------------------------------------------------------------------
# FINAL DATAFRAME COPY with ratios to EXCEL
# -----------------------------------------------------------------------------
# Automatically detect column names
column_names = list(ratiosDataframe)
# print(column_names)
accepted_ratios_sorted_copy = ratiosDataframe.sort_values(by="fitFunc", ascending=False)  # CHANGE sorting_order if desired
accepted_ratios_sorted_copy.to_excel("dataTable_AcceptedRatios_SDlt.xlsx", sheet_name="Uptake_initBiomass_r", header=True, index=True, index_label=None)

# -----------------------------------------------------------------------------
# Subset of configurations where ID_SD == 0; i.e. not included SD excessive nor ZeroDivisionError configurations 
ratiosDataframe_no0fitness = ratiosDataframe[ratiosDataframe["ID_SD"] == 0]
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# ASSOCIATED PLOTS with configurations in which fiFunc = 0, INCLUDED (SD excessive, ZeroDivisionError)
# -----------------------------------------------------------------------------
if not os.path.isdir("Plots"):
    os.mkdir("Plots")  # Create "Plots" directory
os.chdir("Plots")
# -----------------------------------------------------------------------------

myplt.one_plot("fitFunc", "sucr1_frc2", ratiosDataframe, "AccRatios_UptakeR_base", "Uptake Rate")  # Initial reference for further axis limitation
myplt.two_subplots_subsetxlim("fitFunc", "sucr1_frc2", ratiosDataframe, 100, "AccRatios_UptakeR1")
myplt.two_subplots_subset_x_lowerlim("fitFunc", "sucr1_frc2", ratiosDataframe, 100, "AccRatios_UptakeR2")


myplt.one_plot("fitFunc", "Ecbiomass_KTbiomass", ratiosDataframe, "AccRatios_initBiomass_base", "Initial Biomass")  # Initial reference for further axis limitation
myplt.two_subplots_subsetxlim("fitFunc", "Ecbiomass_KTbiomass", ratiosDataframe, 100, "AccRatios_initBiomass1")
myplt.two_subplots_subset_x_lowerlim("fitFunc", "Ecbiomass_KTbiomass", ratiosDataframe, 100, "AccRatios_initBiomass2")
os.chdir("..")


# -----------------------------------------------------------------------------
# ASSOCIATED PLOTS with configurations in which fiFunc = 0, NOT INCLUDED (SD excessive, ZeroDivisionError)
# -----------------------------------------------------------------------------
if not os.path.isdir("Plots_no0fitness"):
    os.mkdir("Plots_no0fitness")  # Create "Plots_no0fitness" directory
os.chdir("Plots_no0fitness")
# -----------------------------------------------------------------------------

myplt.one_plot("fitFunc", "sucr1_frc2", ratiosDataframe_no0fitness, "AccRatios_UptakeR_base_no0fitness", "Uptake Rate")   # Initial reference for further axis limitation
myplt.two_subplots_subsetxlim("fitFunc", "sucr1_frc2", ratiosDataframe_no0fitness, 100, "AccRatios_UptakeR_no0fitness1")
myplt.two_subplots_subset_x_lowerlim("fitFunc", "sucr1_frc2", ratiosDataframe_no0fitness, 100, "AccRatios_UptakeR_no0fitness2")


myplt.one_plot("fitFunc", "Ecbiomass_KTbiomass", ratiosDataframe_no0fitness, "AccRatios_initBiomass_base_no0fitness", "Initial Biomass")   # Initial reference for further axis limitation
myplt.two_subplots_subsetxlim("fitFunc", "Ecbiomass_KTbiomass", ratiosDataframe_no0fitness, 100, "AccRatios_initBiomass_no0fitness1")
myplt.two_subplots_subset_x_lowerlim("fitFunc", "Ecbiomass_KTbiomass", ratiosDataframe_no0fitness, 100, "AccRatios_initBiomass_no0fitness2")
os.chdir("..")











