#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 12:42:28 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Multiple Comparative Statistical Analysis for FLYCOP runs
    
EXPECTED INPUT

    'configurationsResults_Scenario0_analysis_fitFunc.xlsx' OR
    'configurationsResults_Scenario0_analysis_Nar.xlsx' OR
    'configurationsResults_Scenario0_analysis_sub.xlsx' 
    
    from "Extract_configResults_limNut.py" script (OutputAnalysis) for all the FLYCOP runs to be considered in the Comparative Analysis
        
OUTPUT

    Folder: ./MultipleComparativeAnalysis
        "finalNH4_multiplescatter.png"
        "finalpi_multiplescatter.png"
        "finalsucr_multiplescatter.png"
        "DT_cycles_init_multiplescatter.png"
    
NOTE THAT:
    
    xxx
    
"""

# ¿Merece la pena hacer una función de este script?

# import re
import pandas as pd
import os.path
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
from FitnessRanks import extract_ratios
from TrackingFunctions import when_death_starts
import Plotting as myplt
script_path = os.getcwd()


# -----------------------------------------------------------------------------
# REFERENCE PATH
# -----------------------------------------------------------------------------

ref_path = "../Project3_EcPp2_LimNut_M9/Nitrogen"
os.chdir(ref_path)


# -----------------------------------------------------------------------------
# FIRST CONFIGURATION TO CONSIDER
path1 = "./M9base"
# path1 = "./M950N"
# path1 = "./M9100N"
# path1 = "./M9200N"
os.chdir(path1)

configResults1 = pd.read_excel("configurationsResults_Scenario0_analysis_sub.xlsx", sheet_name="Product_ratios", engine="openpyxl")
configResults1_copy = configResults1.copy()

# configResults1_copy = configResults1_copy.sort_values(by=['ID_SD'], ascending=[True])
# configResults1_copy = configResults1_copy[configResults1_copy["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD
# configResults1_copy = when_death_starts(configResults1_copy)
# print(configResults1_copy)
os.chdir("..")

# -----------------------------------------------------------------------------
# SECOND CONFIGURATION TO CONSIDER
path2 = "./M9base_nonSucr"
# path2 = "./M950N_nonSucr"
# path2 = "./M9100N_nonSucr"
# path2 = "./M9200N_nonSucr"
os.chdir(path2)

configResults2 = pd.read_excel("configurationsResults_Scenario0_analysis_sub_fitFunc.xlsx", sheet_name="Product_ratios", engine="openpyxl")
configResults2_copy = configResults2.copy()

configResults2_copy = configResults2_copy[configResults2_copy["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD
configResults2_copy = when_death_starts(configResults2_copy)
# print(configResults2_copy)
os.chdir("..")

# -----------------------------------------------------------------------------
# THIRD CONFIGURATION TO CONSIDER
path3 = "./M9base_nonSucr_nP"
# path3 = "./M950N_nonSucr_nP"
# path3 = "./M9100N_nonSucr_nP"
# path3 = "./M9200N_nonSucr_nP"
os.chdir(path3)

configResults3 = pd.read_excel("configurationsResults_Scenario0_analysis_fitFunc.xlsx", sheet_name="Product_ratios", engine="openpyxl")
configResults3_copy = configResults3.copy()

configResults3_copy = configResults3_copy[configResults3_copy["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD
configResults3_copy = when_death_starts(configResults3_copy)
# print(configResults3_copy)
os.chdir("..")
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# FOURTH CONFIGURATION TO CONSIDER
# path4 = "./M9200N_nonSucr_nP"
# os.chdir(path4)

# configResults4 = pd.read_excel("configurationsResults_Scenario0_analysis_fitFunc.xlsx", sheet_name="Product_ratios", engine="openpyxl")
# configResults4_copy = configResults4.copy()

# configResults4_copy = configResults4_copy[configResults4_copy["ID_SD"] != 1]  #  Only those values for configurations with an acceptable SD
# configResults4_copy = when_death_starts(configResults4_copy)
# print(configResults4_copy)
# os.chdir("..")
# -----------------------------------------------------------------------------


# ÚNICO DATAFRAME FINAL PARA TODAS LAS VARIABLES A COMPARAR
# SET OF DATAFRAMES: dictionary, note 'Key' is the classification variable for further CATEGORICAL PLOTTING
configResults_dataframes = {"M9based": configResults1_copy, "nonSucr_lim": configResults2_copy, "nonSucr_nP_lim": configResults3_copy} # "200": configResults4_copy}
# configResults_dataframes = {"nonSucr_lim": configResults2_copy, "nonSucr_nP_lim": configResults3_copy} # "200": configResults4_copy}
    
    
# MULTIPLE COMPARISON DATAFRAME
# comparison_df = pd.DataFrame({"NH4_mM": [], "pi_mM": [], "Key": [], "FinalSucr": []})  # Better to implement a variable of column names for the df
comparison_df = pd.DataFrame({})  # Better to implement a variable of column names for the df
comparison_df_rows = 0

for key in configResults_dataframes: 
    for row in configResults_dataframes[key].itertuples():
        
        # LOCATE CELLS OF INTEREST
        
        uptake_ratio, initBiomass_ratio = extract_ratios(configResults_dataframes[key].loc[row[0], "configuration"])
        pca = configResults_dataframes[key].loc[row[0], "pCA_mM"]
        nar = configResults_dataframes[key].loc[row[0], "Nar_mM"]
        
        final_Ec = configResults_dataframes[key].loc[row[0], "FinalEc_gL"]
        final_KT = configResults_dataframes[key].loc[row[0], "FinalKT_gL"]
        
        nh4 = configResults_dataframes[key].loc[row[0], "NH4_mM"]
        pi = configResults_dataframes[key].loc[row[0], "pi_mM"]
        
        # finalsucr = configResults_dataframes[key].loc[row[0], "FinalSucr"]
        # DT_init = configResults_dataframes[key].loc[row[0], "DT_cycles_init"]
        
        
        # INCLUDE IN COMPARISON DF
        comparison_df.loc[comparison_df_rows, "Key"] = key
        comparison_df.loc[comparison_df_rows, "Uptake_ratio"] = uptake_ratio
        comparison_df.loc[comparison_df_rows, "InitBiomass_ratio"] = initBiomass_ratio
        
        comparison_df.loc[comparison_df_rows, "pCA_mM"] = pca
        comparison_df.loc[comparison_df_rows, "Nar_mM"] = nar
        
        comparison_df.loc[comparison_df_rows, "FinalEc_gL"] = final_Ec
        comparison_df.loc[comparison_df_rows, "FinalKT_gL"] = final_KT
        
        
        comparison_df.loc[comparison_df_rows, "NH4_mM"] = nh4
        comparison_df.loc[comparison_df_rows, "pi_mM"] = pi
        
        # comparison_df.loc[comparison_df_rows, "FinalSucr"] = finalsucr
        # comparison_df.loc[comparison_df_rows, "DT_cycles_init"] = DT_init
        comparison_df_rows += 1
        
    # print(comparison_df_rows)

# print(comparison_df)
print(list(comparison_df.columns))
# print(comparison_df[comparison_df["Key"] == str(18.7)])
# print(comparison_df[comparison_df["Key"] == str(50)])
# print(comparison_df[comparison_df["Key"] == str(100)])


# -----------------------------------------------------------------------------
if not os.path.isdir("MultipleComparativeAnalysis_M9base"):
    os.mkdir("MultipleComparativeAnalysis_M9base")  # VERY IMPORTANT TO CHANGE THIS NAME SO THAT THE CONTENTS IN AN ALREADY EXISTING FOLDER DO NOT GET OVERWRITTEN
os.chdir("MultipleComparativeAnalysis_M9base")
# -----------------------------------------------------------------------------
# SEGUIR AQUÍ



myplt.basic_scatter(comparison_df, "Key", "Uptake_ratio", "FLYCOP run", "Uptake Rates ratio", "uptakeRratio_multiplescatter", "Uptake Rates ratio")
myplt.basic_scatter(comparison_df, "Key", "InitBiomass_ratio", "FLYCOP run", "Initial Biomass ratio", "initBratio_multiplescatter", "Initial Biomass ratio")

myplt.basic_scatter(comparison_df, "Key", "pCA_mM", "FLYCOP run", "Final [pCA] (mM)", "finalpca_multiplescatter", "Final pCA")
myplt.basic_scatter(comparison_df, "Key", "Nar_mM", "FLYCOP run", "Final [Nar] (mM)", "finalnar_multiplescatter", "Final Naringenin")

myplt.basic_scatter(comparison_df, "Key", "FinalEc_gL", "FLYCOP run", "Final E.coli (g/L)", "finalEc_multiplescatter", "Final E.coli biomass")
myplt.basic_scatter(comparison_df, "Key", "FinalKT_gL", "FLYCOP run", "Final P.putida KT (g/L)", "finalKT_multiplescatter", "Final P.putida KT biomass")

myplt.basic_scatter(comparison_df, "Key", "NH4_mM", "FLYCOP run", "Final [NH4] (mM)", "finalNH4_multiplescatter", "Final NH4")
myplt.basic_scatter(comparison_df, "Key", "pi_mM", "FLYCOP run", "Final [Pi] (mM)", "finalpi_multiplescatter", "Final Pi")
# myplt.basic_scatter_ylim(comparison_df, "Key", "pi_mM", "FLYCOP run", "Final [Pi] (mM)", 100, "finalpi_multiplescatter_ylim100", "Final Pi")
# myplt.basic_scatter_ylim(comparison_df, "Key", "pi_mM", "FLYCOP run", "Final [Pi] (mM)", 0.2, "finalpi_multiplescatter_ylim0.2", "Final Pi")
# myplt.basic_scatter_ylim(comparison_df, "Key", "pi_mM", "FLYCOP run", "Final [Pi] (mM)", 0.05, "finalpi_multiplescatter_ylim0.05", "Final Pi")

# myplt.basic_scatter(comparison_df, "Key", "FinalSucr", "FLYCOP run", "Final [Sucr] (mM)", "finalsucr_multiplescatter", "Final Sucrose")
# myplt.basic_scatter(comparison_df, "Key", "DT_cycles_init", "FLYCOP run", "Initial Death Cycle", "DT_cycles_init_multiplescatter", "Death Effect (initial cycle)")
os.chdir("..")


# PENDIENTE REVISAR Y GENERALIZAR
# -----------------------------------------------------------------------------
# Count the number of different final values (0, initial concentrations, disproportionate concentrations)
    # for Pi
    # for NH4

print()
for key in comparison_df["Key"].unique():
    print(key)
    
    # PHOSPHATE
    zero_Pi = 0
    low_Pi = 0
    intermediate_Pi = 0
    original_Pi = 0
    disproportionate1_Pi = 0
    disproportionate2_Pi = 0
    
    # NH4 AND RELATED
    final_nh4_zero = 0
    final_zero_nh4_pi = 0
    final_zero_nh4_over1_pi = 0
    final_zero_nh4_over2_pi = 0
    
    # DEATH EFFECT
    # no_death_eff = 0
    # death_eff = 0
    # death_eff_nh4 = 0
    # death_eff_nh4_pi = 0
    
    # SUCROSE
    # final_sucr_zero = 0
    
    # pCA
    final_pca_zero = 0
    
    for row in comparison_df[comparison_df["Key"] == key].itertuples():
        # print(key)
        nh4 = row[8]
        pi = row[9]
        pca = row[4]
        
        # sucr = row[10]
        # deadinit = row[11]
        
        if pi < 1:
            zero_Pi += 1
            
        if 1 < pi < 10:
            low_Pi += 1
            
        elif 10 < pi < 55:
            intermediate_Pi += 1
            
        elif 55 < pi < 69.9:
            original_Pi += 1
            
        elif 69.9 < pi:
            disproportionate1_Pi += 1
            
        if 1000 < pi:
            disproportionate2_Pi += 1
            
        if nh4 < 1 and pi < 1:
            final_zero_nh4_pi += 1
            
        if nh4 < 1 and 69.9 < pi:
            final_zero_nh4_over1_pi += 1
            
        if nh4 < 1 and 1000 < pi:
            final_zero_nh4_over2_pi += 1
            
        if nh4 < 1:
            final_nh4_zero += 1
            
        if pca < 1:
            final_pca_zero += 1
            
        # if deadinit == 0:
        #     no_death_eff += 1
        # else:
        #     death_eff += 1
            
        # if deadinit != 0 and nh4 < 1:
        #     death_eff_nh4 += 1
            
        # if deadinit != 0 and nh4 < 1 and pi < 1:
        #     death_eff_nh4_pi += 1
            
        # if sucr < 1:
        #     final_sucr_zero += 1
            
          
    # AÑADIR AQUÍ NÚMERO DE CONFIGURACIONES TOTALES y porcentaje        
    print("CONFIGURATION: ", key, "mM [NH4]")
    # print(comparison_df[comparison_df["Key"] == key].count())
    print("The number of low final [Pi] (under 1 mM) was: ", zero_Pi)
    print("The number of low final [Pi] (between 1 to 10 mM) was: ", low_Pi)
    print("The number of intermediate final [Pi] (10-55 mM) was: ", intermediate_Pi)
    print("The number of final [Pi] near original concentration (55-69.9 mM) was: ", original_Pi)
    
    print("The number of higher than initial or disproportionate final [Pi] (higher than 69.9 mM) was: ", disproportionate1_Pi)
    print("The number of higher than initial or disproportionate final [Pi] (higher than 1000 mM) was: ", disproportionate2_Pi)
    print()
    
    print("The number of final [nh4] nearly 0 or 0 was: ", final_nh4_zero)
    print("The number of final disproportionate [Pi] (higher than 69.9 mM) with final [nh4] nearly 0 was: ", final_zero_nh4_over1_pi)
    print("The number of final disproportionate [Pi] (higher than 1000 mM) with final [nh4] nearly 0 was: ", final_zero_nh4_over2_pi)
    print("The number of final [Pi] nearly 0 with final [nh4] nearly 0 was: ", final_zero_nh4_pi)
    print()
    
    print("The number of final [pca] nearly 0 or 0 was: ", final_pca_zero)
    # print("The number of final [sucr] nearly 0 or 0 was: ", final_sucr_zero)
    # print()
    # print("The number of cases without death effect was: ", no_death_eff)
    # print("The number of cases with death effect was: ", death_eff)
    # print("The number of cases with death effect and [nh4] exhaustion was: ", death_eff_nh4)
    # print("The number of cases with death effect and both [nh4] and [pi] exhaustion was: ", death_eff_nh4_pi)
    print("\n\n")
# -----------------------------------------------------------------------------
        






















































