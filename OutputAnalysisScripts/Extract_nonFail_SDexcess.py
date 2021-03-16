#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Feb 17 00:06:44 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Script for output analysis which extracts those configurations with excessive SD
    [SD > 10% (avgfitness)], but which do not raise a ZeroDIvisionError --> "SDexcess_configs"
    
    'dataTable_Scenario0.txt', all configurations are obtained: right_configs, SDexcess_configs, ZeroDivisionError_configs
    We would be interested just in those with fitness = 0; SDexcess_configs, ZeroDivisionError_configs
    
    'configurationsResults_Scenario0.txt' just contains right_configs and SDexcess_configs
    So those configurations with fitness = 0 (from 'dataTable_Scenario0.txt') being in this file, would be SDexcess_configs
    
    
EXPECTED INPUT

    'dataTable_Scenario0.txt'
    'configurationsResults_Scenario0.txt'
    
OUTPUT

    "nonFailConfig_SDexcess_analysis.csv"
    
NOTE THAT:
    
        This script might need to be adapted, depending on the parameters in the 
        variable 'configuration' in your particular FLYCOP run
"""

import re
import os.path
import pandas as pd
path = "../Project3_EcPp2_LimNut_M9/Nitrogen/M9200N_nonSucr_nP"  # POTENTIAL CHANGE
os.chdir(path)
count_configs = 0

# -----------------------------------------------------------------------------
# Configurations at 'configurationsResults_Scenario0.txt'
# -----------------------------------------------------------------------------
configResults = pd.read_csv("configurationsResults_Scenario0.txt", sep="\t", header="infer")
# print(configResults)


# -----------------------------------------------------------------------------
# Configurations with fitness = 0 from 'dataTable_Scenario0.txt'
# -----------------------------------------------------------------------------

# A new file is created with the information for those configurations
output = open("nonFailConfig_SDexcess_analysis.txt", "w")
output.write("Configuration\tsucr_frc\tinitEc_KT\tfitness\tsd\tpCA_mM\tFinalEc_gL\tNar_mM\tFinalKT_gL\n")
# Others: \tNH4_mM\tpi_mM\tendCycle

# DataTable
# ---------
dataTable = pd.read_csv("dataTable_Scenario0.txt", sep="\t", header="infer")
filtered_dataTable = dataTable[dataTable['fitFunc'] == 0]
# print(filtered_dataTable)
# print(filtered_dataTable.describe())

for row in filtered_dataTable.itertuples(): 
        sucr = float(row[1])  # 'float' para que el número sea decimal (.0), necesario en comparación posterior
        EcBiomass = row[2]
        frc = float(row[3])
        KTbiomass = row[4]
        config = str(sucr)+","+str(EcBiomass)+","+str(frc)+","+str(KTbiomass)
        # print(config)
        
        
        # When a 'fitness = 0' configuration is not present in 'configurationsResults_Scenario0.txt', 
        # it means it constitutes a ZeroDivisionError
        
        # if config in configResults["configuration"]:  # Esta alternativa no funciona
        for row in configResults.itertuples():
            if config == row[2]:
                # print(config)
                count_configs +=1
                
                # Ratios of interest
                sucr_frc = str(round(sucr/frc, 3))
                initBiomass = str(round(EcBiomass/KTbiomass, 3))
                
                fitness = str(round(row[3], 3))
                SD = str(round(row[4], 3))
                pCA = str(row[5])
                finalEc = str(row[6])
                Nar = str(row[7])
                finalKT = str(row[8])
                
                output.write(config+"\t"+sucr_frc+"\t"+initBiomass+"\t"+fitness+"\t"+SD+"\t"+pCA+"\t"+finalEc+"\t"+Nar+"\t"+finalKT+"\n")

print("Total of SDexcess_configs (ZeroDivisionError not included): ", count_configs)
output.close()


# -----------------------------------------------------------------------------
# New dataframe 'nonFailConfig_SDexcess_analysis.txt' to CSV
# -----------------------------------------------------------------------------
configResults_excessSD = pd.read_csv("nonFailConfig_SDexcess_analysis.txt", sep="\t", header="infer")
configResults_excessSD.to_csv("nonFailConfig_SDexcess_analysis.csv", sep='\t', header=True, index=True, index_label=None)
os.remove("nonFailConfig_SDexcess_analysis.txt")




