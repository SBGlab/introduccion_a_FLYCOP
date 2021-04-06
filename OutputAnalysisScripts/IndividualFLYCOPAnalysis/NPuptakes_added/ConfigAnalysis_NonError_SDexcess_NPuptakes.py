#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Feb 17 00:06:44 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Script for output analysis in case of FLYCOP (COBRA) error: NonOptimalConfig_Error.
    It is necessary to make a difference between those configurations that raise this error and those that does not.
    
    Moreover, in each group, it is further necessary to distinguish between configurations:
        
        * with biomass loss;
        * without biomass loss;
                                                
    So the current script obtains a final dataframe (excel file) for both groups:
        
        * NonOptimalConfig_Error configurations;
        * Acceptable (no error) configurations;
        
        and further counts the number of occurrences for each group. Within each group, 
            the number of cases with / without biomass loss is also calculated.
        
    
EXPECTED INPUT

    'configurationsResults_Scenario0.txt'
    
OUTPUT

    Section of 'configurationsResults_Scenario0.txt' with the mentioned configurations: 'configurationsResults_Scenario0_acceptableBiomassLoss.xlsx'
    Section of 'configurationsResults_Scenario0.txt' with the mentioned configurations: 'configurationsResults_Scenario0_NonOptimalConfig_error.xlsx'
    
NOTE THAT:
    
        This script is currently adapted to the consortium for naringenin production, E.coli-P.putidaKT (2 microbes).
        If you wanted to use it with a different consortium, please take into account the next adaptations - Recall: CHANGE 'variable'
            
                - variable 'path'
                
        Note that this script is all about NonOptimalConfig_Error FLYCOP (COBRA) error, and further biomass loss.
"""

# import re
import os.path
import pandas as pd
path = "../../../Project3_EcPp2_LimNut_M9/NP_LimNutFinal_29Mar/NP3"  # CHANGE PATH
os.chdir(path)

count_SDconfigs = 0  # Count of configurations with final fitness 0, because of excessive SD


# -----------------------------------------------------------------------------
# Configurations at 'configurationsResults_Scenario0.txt'
# -----------------------------------------------------------------------------
configResults = pd.read_csv("configurationsResults_Scenario0.txt", sep="\t", header="infer")
nonOptimal_file = pd.read_csv("nonOptimalConfigs_asStrings.txt", sep="\t", header=None, names = ["Configurations"])  # Single column (configuration of parameters)



# NON-ACCEPTABLE CONFIGURATIONS: those with NonOptimalConfig_Error
# -----------------------------------------------------------------------------
empty_dataframe = True  # Still not found NonOptimalConfig_Error in configResults_dataframe

for row in nonOptimal_file.itertuples():
    bad_config = row[1]
    
    if empty_dataframe:
        configResults_nonOpt = configResults[configResults.BaseConfig == bad_config]
        empty_dataframe = False  # First found: NonOptimalConfig_Error config
    else:
        configResults_nonOpt = configResults_nonOpt.append(configResults[configResults.BaseConfig == bad_config])
        
print("Total of configurations with NonOptimalConfig_error: ", len(configResults_nonOpt))
biomass_loss_number_nonOpt = configResults_nonOpt[configResults_nonOpt["DeadTracking"] == 1]
print("Total of configurations with NonOptimalConfig_error and NO biomass loss: ", len(configResults_nonOpt) - len(biomass_loss_number_nonOpt))
print("Total of configurations with NonOptimalConfig_error and biomass loss: ", len(biomass_loss_number_nonOpt))

# New dataframe to EXCEL
configResults_nonOpt.to_excel("configurationsResults_Scenario0_NonOptimalConfig_error.xlsx", sheet_name="NonOptimalConfig_error", header=True, index=False, index_label=None)
# -----------------------------------------------------------------------------



# ACCEPTABLE CONFIGURATIONS: those with NO NonOptimalConfig_Error
# -----------------------------------------------------------------------------
for row in nonOptimal_file.itertuples():
    bad_config = row[1]
    configResults = configResults[configResults.BaseConfig != bad_config]
   
print()
print("Total of configurations without NonOptimalConfig_error: ", len(configResults))
biomass_loss_acceptable = configResults[configResults["DeadTracking"] == 1]
print("Total of configurations without those under NonOptimalConfig_error and NO biomass loss: ", len(configResults) - len(biomass_loss_acceptable))
print("Total of configurations without those under NonOptimalConfig_error and biomass loss: ", len(biomass_loss_acceptable))

# New dataframe to EXCEL
configResults.to_excel("configurationsResults_Scenario0_acceptableBiomassLoss.xlsx", sheet_name="Acceptable_BiomassLoss", header=True, index=False, index_label=None)
# -----------------------------------------------------------------------------





















