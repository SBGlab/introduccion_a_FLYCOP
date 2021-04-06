#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 00:29:22 2021

@author: Iván Martín Martín
"""

# REVISAR POST ADAPTACIÓN NP_UPTAKE

"""
DESCRIPTION - OUTPUT PARAMETERS ANALYSIS

    Script for output analysis which calculates:
        
        input parameters ratios: carbon uptake, initial biomass, nh4 uptake, pi uptake (First microorganism / Second microorganism)
        ratio of metabolites, each produced by one of the two microbes in the corsortium (final product / intermediate product)
        ratio of final biomass (First microorganism / Second microorganism)
        
    Moreover, the script generates the corresponding plots of:
        
            ratio of metabolites vs. fitFunc
            ratio of final biomass (First microorganism / Second microorganism) vs. fitFunc
            
            final concentration of intermediate product vs. fitFunc
            final concentration of final product vs. fitFunc
        
            Limiting nutrient final concentration. vs. fitFunc 
            (where final conc != 0 mM, to easily find the fitness value for these particular cases)
            [IF THE CURRENT SIMULATION DOES NOT HAVE ANY LIMITING NUTRIENTS, THESE CODE LINES CAN BE OMITTED]
            
            PENDIENTE: añadir when_dead_starts()
        
    The script can be used with those configurations that do not raise a NonOptimalConfig_Error:
        EXCEL FILE: configurationsResults_Scenario0_acceptableBiomassLoss.xlsx
        
    Also, with those configs that raise a NonOptimalConfig_Error:
        EXCEL FILE: configurationsResults_Scenario0_NonOptimalConfig_error.xlsx
    
    The plots are generated:
            (a) For the whole set of configurations in the EXCEL FILE dataframe
            (b) Within the last ones, those with NO biomass loss
            
            
        
    FIRST PART OF THE SCRIPT
    ------------------------
    1. Read dataframe and categorize configurations according to its SD (excessive if > 10% (avgfit))
    2. Sort the dataframe by 'fitness' and 'SD_criterion' unless otherwise desired
        
    
    SECOND PART OF THE SCRIPT
    -------------------------
    Computing ratios and further interesting parameters. This code chunks could be adapted to
    suit the purposes of the consortiums under analysis, i.e. in case of 
    a different number of microbes or metabolites per microbe. Currently:
        
        * ratios of input parameters: carbon uptake, initial biomass, nh4 uptake, pi uptake (First microorganism / Second microorganism)
        * ratio of metabolites, each produced by one of the two microbes in the corsortium (final product / intermediate product)
        * ratio of final biomass (First microorganism / Second microorganism)
    
    
    THIRD PART OF THE SCRIPT
    ------------------------
    1. Obtain the final dataframe and export it to EXCEL
    2. Plotting. For further information about each plotting utility, see Plotting.py
    
    
    FINAL UTILITY (shutted down by default)
    -------------
    Create a complete dataframe with all configurations: NonOptimalConfig_Error + Acceptable,
        with an additional column (identifier) that allows for their differentiation (sort of a key for further categorical plotting)
        
    NOTE THAT this script chunck has to be run after running the current script for both groups of configurations independently: NonOptimalConfig_Error, Acceptable.
    
    
        
EXPECTED INPUT

    'configurationsResults_Scenario0_acceptableBiomassLoss.xlsx' OR
    'configurationsResults_Scenario0_NonOptimalConfig_error.xlsx'
    
    # configurationsResults_Scenario0_COMPLETE.xlsx
    
OUTPUT

    "configurationsResults_Scenario0_acceptableBiomassLoss_analysis.xlxs" OR
    "configurationsResults_Scenario0_NonOptimalConfig_error_analysis.xlsx"
    
    Plots (...)
    
    
NOTE THAT:
    
    Code lines where a change might be eventually required are marked as CHANGE.
    IMPORTANT CHANGES:
        - final file: with or without NonOptimalConfig_error
        - sheet_name
        - ConfigKey for further categorical plotting: NonOptimalConfig_Error + Acceptable
        - final EXCEL output name
        - Folder name for plots
    
    
    This script is currently adapted to the consortium for naringenin production, E.coli-P.putidaKT (2 microbes),
    where it calculates the ratio of final products between the two microbes and the ratio of final biomass.
    
        (Necessary adaptation in case of change: sections on "COMPUTE RATIOS" and "PLOTTING")
        Parameter names, plot titles and names, etc.
        
"""

import pandas as pd
import os.path

scripts_path = os.getcwd()
os.chdir("../Utilities")
import Plotting as myplt
import FitnessRanks as fitranks

os.chdir(scripts_path)  # Creo que esto va a fallar, hace falta: os.chdir("../IndividualFLYCOPAnalysis")
path = "../../../Project3_EcPp2_LimNut_M9/NP_LimNutFinal_29Mar/NP3"  # CHANGE path
os.chdir(path)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# SCRIPT CODE
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    

# =============================================================================
# ORIGINAL DATAFRAME & ADAPTATIONS
# =============================================================================

# DATAFRAME
# ---------
final_file = "configurationsResults_Scenario0_acceptableBiomassLoss.xlsx"  # CHANGE name
# final_file = "configurationsResults_Scenario0_NonOptimalConfig_error.xlsx"

sheet_name = "Acceptable_BiomassLoss"  # CHANGE name
# sheet_name = "NonOptimalConfig_error"

configResults = pd.read_excel(final_file, sheet_name=sheet_name, engine="openpyxl")
# print(configResults[configResults["fitFunc"] == 0])

    
# CLASSIFY RECORDS DEPENDING ON SD: higher or lower than (0.1)*(fitFunc)
# No 'ZeroDivisionError' in this script since these configurations are not included in 'configurationsResults_Scenario0.txt'
# ------------------------------------------
configResults["ID_SD"] = 0

for row in configResults.itertuples():   # row[0] = Index Number
        
    if configResults.loc[row[0], "sd"] >= (0.1)*(configResults.loc[row[0], "fitFunc"]):
        configResults.loc[row[0], "ID_SD"] = 1
    
    
# Automatically detect column names
column_names = list(configResults)
# print(column_names)


# SORT BY ref_column: 'ID_SD', 'fitness' unless otherwise indicated 
# ----------------------
configResults = configResults.sort_values(by=['ID_SD', 'fitFunc'], ascending=[True, False])  # CHANGE sorting_order if desired
# print(configResults["fitFunc"])
    
    
    
# =============================================================================
# COMPUTE RATIOS
# Note that the names of metabolites for uptake rates and microbes names have to be CHANGED whenever necessary
# =============================================================================
# NEEDS FURTHER OPTIMIZATION: ratios from DataTable (inputParameters)
configResults_copy = configResults.copy()  # Avoid 'SettingWithCopyWarning'
add_columns_to_dataframe = ["sucr1_frc2", "Ecbiomass_KTbiomass", "NH4_Ec_KT", "Pi_Ec_KT", 
                            "sucr1_IP", "frc1_IP", "EcInit_IP", "KTInit_IP", "NH4_Ec", "NH4_KT", "Pi_Ec", "Pi_KT"]

for new_column in add_columns_to_dataframe:
    configResults_copy[new_column] = 0


for row in configResults_copy.itertuples():   # row[0] = Index Number
    uptake_ratio, initbiomass_ratio, NH4_Ec_KT, Pi_Ec_KT = fitranks.extract_ratios_NP(configResults_copy.loc[row[0], "BaseConfig"])
    sucr1, frc1, EcInitIP, KTInitIP, NH4_Ec, NH4_KT, Pi_Ec, Pi_KT = fitranks.extract_baseConfig_NP(configResults_copy.loc[row[0], "BaseConfig"])
    
    configResults_copy.loc[row[0], "sucr1_frc2"] = uptake_ratio
    configResults_copy.loc[row[0], "Ecbiomass_KTbiomass"] = initbiomass_ratio
    configResults_copy.loc[row[0], "NH4_Ec_KT"] = NH4_Ec_KT
    configResults_copy.loc[row[0], "Pi_Ec_KT"] = Pi_Ec_KT

    configResults_copy.loc[row[0], "sucr1_IP"] = sucr1
    configResults_copy.loc[row[0], "frc1_IP"] = frc1
    configResults_copy.loc[row[0], "EcInit_IP"] = EcInitIP
    configResults_copy.loc[row[0], "KTInit_IP"] = KTInitIP
    
    configResults_copy.loc[row[0], "NH4_Ec"] = NH4_Ec
    configResults_copy.loc[row[0], "NH4_KT"] = NH4_KT
    configResults_copy.loc[row[0], "Pi_Ec"] = Pi_Ec
    configResults_copy.loc[row[0], "Pi_KT"] = Pi_KT



# POTENTIAL CHANGE FOR NAMES if a different consortium is used
ratios = ["Nar_mM_pCA_mM", "FinalEc_gL_FinalKT_gL"]  # Names for new column_ratios to be calculated, in order
finalProducts = ["Nar_mM", "pCA_mM"]  # Numerator, denominator (in that order) for the first of the ratios to be calculated
finalBiomass = ["FinalEc_gL", "FinalKT_gL"]  # Numerator, denominator (in that order) for the second of the ratios to be calculated
    
# ratio NAR / pCA
# configResults_copy = configResults.copy()  # Avoid 'SettingWithCopyWarning'
try:
    configResults_copy[ratios[0]] = round((configResults_copy[finalProducts[0]] / configResults_copy[finalProducts[1]]), 4)
except ZeroDivisionError:
    configResults_copy[ratios[0]] = "NaN"
        
# ratio finalEc / finalKT
try:
    configResults_copy[ratios[1]] = round((configResults_copy[finalBiomass[0]] / configResults_copy[finalBiomass[1]]), 4)
except ZeroDivisionError:
    configResults_copy[ratios[1]] = "NaN"
            

        
# =============================================================================
# FINAL DATAFRAME COPY with ratios to EXCEL
# =============================================================================
# Automatically detect column names
column_names = list(configResults_copy)
# print(column_names)


# DATAFRAME TO EXCEL: ordered by fitFunc (descending)
configResults_copy["ConfigKey"] = "Acceptable"  # CHANGE: Acceptable OR NonOptimalE
configResults_copy.to_excel("configurationsResults_Scenario0_acceptableBiomassLoss_analysis.xlsx", sheet_name="Product_ratios", header=True, index=True, index_label=None)
# configResults_copy.to_excel("configurationsResults_Scenario0_NonOptimalConfig_error_analysis.xlsx", sheet_name="Product_ratios", header=True, index=True, index_label=None)



# =============================================================================
# ASSOCIATED PLOTS with all configurations in the dataframe
# =============================================================================
if not os.path.isdir("Plots_acceptableBiomassLoss"):
    os.mkdir("Plots_acceptableBiomassLoss")  # Create "Plots_acceptableBiomassLoss" directory. CHANGE: Plots_acceptableBiomassLoss OR Plots_NonOptimalConfig_error
os.chdir("Plots_acceptableBiomassLoss")
# -----------------------------------------------------------------------------

input_parameters = ["sucr1_IP", "frc1_IP", "EcInit_IP", "KTInit_IP", "NH4_Ec", "NH4_KT", "Pi_Ec", "Pi_KT"]
title_inputParams = "configResults_inputparams_"

# ratios = ["Nar_mM_pCA_mM", "FinalEc_gL_FinalKT_gL"]  
# finalProducts = ["Nar_mM", "pCA_mM"]  
# finalBiomass = ["FinalEc_gL", "FinalKT_gL"]  

input_ratios = ["sucr1_frc2", "Ecbiomass_KTbiomass", "NH4_Ec_KT", "Pi_Ec_KT"] 
title0 = "Input Parameter ratios"
png_name0 = "configResults_inputParametersVSfitness"


# ratios = ["Nar_mM_pCA_mM", "FinalEc_gL_FinalKT_gL"]  
title1 = "Output Parameter ratios"
png_name1 = "configResults_NARpCAr_finalBiomass_limNut"


# finalProducts = ["Nar_mM", "pCA_mM"]  
title2 = "Final Products"
png_name2 = "configResults_products_fitness_limNut"


# finalBiomass = ["FinalEc_gL", "FinalKT_gL"]
title3 = "Final Biomass"
png_name3 = "configResults_finalBiomass_limNut"


limNut_name = "NH4_mM"  # CHANGE limiting nutrient
title4 = "Limiting nutrient"
png_name4 = "configResults_"+limNut_name+"_limNut"


# Input Ratios vs. fitFunc
myplt.two_plots_twolabels("fitFunc", input_ratios[0], input_ratios[1], configResults_copy, png_name0+"1", title0)  # Carbon Uptake ratio
myplt.two_plots_twolabels("fitFunc", input_ratios[2], input_ratios[3], configResults_copy, png_name0+"2", title0)  # Nitrogen Uptake ratio

# Other displays for Input Parameters
myplt.one_plot(input_parameters[0], input_parameters[1], configResults_copy, title_inputParams+"carbonSource", "Carbon Uptake")
myplt.one_plot(input_parameters[2], input_parameters[3], configResults_copy, title_inputParams+"initial_biomass", "Initial Biomass")
myplt.one_plot(input_parameters[4], input_parameters[5], configResults_copy, title_inputParams+"NH4uptake", "NH4 Uptake")
myplt.one_plot(input_parameters[6], input_parameters[7], configResults_copy, title_inputParams+"Piuptake", "Pi Uptake")


# Ratios vs. fitFunc
myplt.two_plots_twolabels("fitFunc", ratios[0], ratios[1], configResults_copy, png_name1+"1", title1)
# myplt.two_plots_twolabels_xlim("fitFunc", ratios[0], ratios[1], configResults_copy, 100, png_name1+"2", title1)
# myplt.two_plots_twolabels_x_lowerlim("fitFunc", ratios[0], ratios[1], configResults_copy, 100, png_name1+"3", title1)

# Final Products vs. fitFunc
myplt.two_plots_twolabels("fitFunc", finalProducts[0], finalProducts[1], configResults_copy, png_name2+"1", title2)
# myplt.two_plots_twolabels_xlim("fitFunc", finalProducts[0], finalProducts[1], configResults_copy, 100, png_name2+"2", title2)
# myplt.two_plots_twolabels_x_lowerlim("fitFunc", finalProducts[0], finalProducts[1], configResults_copy, 100, png_name2+"3", title2)

# Final Biomass vs. fitFunc
myplt.two_plots_twolabels("fitFunc", finalBiomass[0], finalBiomass[1], configResults_copy, png_name3+"1", title3)
# myplt.two_plots_twolabels_xlim("fitFunc", finalBiomass[0], finalBiomass[1], configResults_copy, 100, png_name3+"2", title3)
# myplt.two_plots_twolabels_x_lowerlim("fitFunc", finalBiomass[0], finalBiomass[1], configResults_copy, 100, png_name3+"3", title3)

# LimitNut vs. fitFunc, in those cases when LimitNut != 0 (at the end)
limNut_dataframe = configResults_copy[configResults_copy[limNut_name] != 0]  # Section of the dataframe
myplt.one_plot("fitFunc", limNut_name, limNut_dataframe, png_name4+"1", title4)
# myplt.one_plot_xlim("fitFunc", limNut_name, limNut_dataframe, 100, png_name4+"2", title4)
# myplt.one_plot_x_lowerlim("fitFunc", limNut_name, limNut_dataframe, 100, png_name4+"3", title4)

os.chdir("..")


# =============================================================================
# Within the last group, those configs with NO biomass loss
# =============================================================================
if not os.path.isdir("Plots_acceptable_No_BiomassLoss"):
    os.mkdir("Plots_acceptable_No_BiomassLoss")  # Create "Plots_acceptable_No_BiomassLoss" directory. CHANGE: Plots_acceptable_No_BiomassLoss OR Plots_NonOptimalConfig_No_BiomassLoss
os.chdir("Plots_acceptable_No_BiomassLoss")

# FILTER BY DEATH EFFECT: we do not want configurations with biomass loss
# -----------------------------------------------------------------------------
configResults_copy_NoBiomassLoss = configResults_copy[configResults_copy["DeadTracking"] == 0]
print("Number of cases with no biomass loss: ", len(configResults_copy_NoBiomassLoss))
# -----------------------------------------------------------------------------
    
input_parameters = ["sucr1_IP", "frc1_IP", "EcInit_IP", "KTInit_IP", "NH4_Ec", "NH4_KT", "Pi_Ec", "Pi_KT"]
title_inputParams = "configResults_inputparams_"

# ratios = ["Nar_mM_pCA_mM", "FinalEc_gL_FinalKT_gL"]  
# finalProducts = ["Nar_mM", "pCA_mM"]  
# finalBiomass = ["FinalEc_gL", "FinalKT_gL"]  


input_ratios = ["sucr1_frc2", "Ecbiomass_KTbiomass", "NH4_Ec_KT", "Pi_Ec_KT"] 
title0 = "Input Parameter ratios"
png_name0 = "configResults_inputParametersVSfitness"


# ratios = ["Nar_mM_pCA_mM", "FinalEc_gL_FinalKT_gL"]  
title1 = "Output Parameter ratios"
png_name1 = "configResults_NARpCAr_finalBiomass_limNut"


# finalProducts = ["Nar_mM", "pCA_mM"]  
title2 = "Final Products"
png_name2 = "configResults_products_fitness_limNut"


# finalBiomass = ["FinalEc_gL", "FinalKT_gL"]
title3 = "Final Biomass"
png_name3 = "configResults_finalBiomass_limNut"


limNut_name = "NH4_mM"  # CHANGE limiting nutrient
title4 = "Limiting nutrient"
png_name4 = "configResults_"+limNut_name+"_limNut"


# Input Ratios vs. fitFunc
myplt.two_plots_twolabels("fitFunc", input_ratios[0], input_ratios[1], configResults_copy_NoBiomassLoss, png_name0+"1", title0)
myplt.two_plots_twolabels("fitFunc", input_ratios[2], input_ratios[3], configResults_copy_NoBiomassLoss, png_name0+"2", title0)

# Other displays for Input Parameters
myplt.one_plot(input_parameters[0], input_parameters[1], configResults_copy_NoBiomassLoss, title_inputParams+"carbonSource", "Carbon Uptake")
myplt.one_plot(input_parameters[2], input_parameters[3], configResults_copy_NoBiomassLoss, title_inputParams+"initial_biomass", "Initial Biomass")
myplt.one_plot(input_parameters[4], input_parameters[5], configResults_copy_NoBiomassLoss, title_inputParams+"NH4uptake", "NH4 Uptake")
myplt.one_plot(input_parameters[6], input_parameters[7], configResults_copy_NoBiomassLoss, title_inputParams+"Piuptake", "Pi Uptake")


# Ratios vs. fitFunc
myplt.two_plots_twolabels("fitFunc", ratios[0], ratios[1], configResults_copy_NoBiomassLoss, png_name1+"1", title1)
# myplt.two_plots_twolabels_xlim("fitFunc", ratios[0], ratios[1], configResults_copy_NoBiomassLoss, 100, png_name1+"2", title1)
# myplt.two_plots_twolabels_x_lowerlim("fitFunc", ratios[0], ratios[1], configResults_copy_NoBiomassLoss, 100, png_name1+"3", title1)

# Final Products vs. fitFunc
myplt.two_plots_twolabels("fitFunc", finalProducts[0], finalProducts[1], configResults_copy_NoBiomassLoss, png_name2+"1", title2)
# myplt.two_plots_twolabels_xlim("fitFunc", finalProducts[0], finalProducts[1], configResults_copy_NoBiomassLoss, 100, png_name2+"2", title2)
# myplt.two_plots_twolabels_x_lowerlim("fitFunc", finalProducts[0], finalProducts[1], configResults_copy_NoBiomassLoss, 100, png_name2+"3", title2)

# Final Biomass vs. fitFunc
myplt.two_plots_twolabels("fitFunc", finalBiomass[0], finalBiomass[1], configResults_copy_NoBiomassLoss, png_name3+"1", title3)
# myplt.two_plots_twolabels_xlim("fitFunc", finalBiomass[0], finalBiomass[1], configResults_copy_NoBiomassLoss, 100, png_name3+"2", title3)
# myplt.two_plots_twolabels_x_lowerlim("fitFunc", finalBiomass[0], finalBiomass[1], configResults_copy_NoBiomassLoss, 100, png_name3+"3", title3)

# LimitNut vs. fitFunc, in those cases when LimitNut != 0 (at the end)
limNut_dataframe = configResults_copy_NoBiomassLoss[configResults_copy_NoBiomassLoss[limNut_name] != 0]  # Section of the dataframe
if len(limNut_dataframe) > 0:
    myplt.one_plot("fitFunc", limNut_name, limNut_dataframe, png_name4+"1", title4)
    # myplt.one_plot_xlim("fitFunc", limNut_name, limNut_dataframe, 100, png_name4+"2", title4)
    # myplt.one_plot_x_lowerlim("fitFunc", limNut_name, limNut_dataframe, 100, png_name4+"3", title4)

os.chdir("..")




# =============================================================================
# COMPLETE DATAFRAME CREATION
# Create a complete dataframe with all configurations: NonOptimalConfig_Error + Acceptable,
# with an additional column (identifier) that allows for their differentiation (sort of a key for further categorical plotting)
# =============================================================================

#  SHUTTED DOWN
# """

acceptable_complete = pd.read_excel("configurationsResults_Scenario0_acceptableBiomassLoss_analysis.xlsx", sheet_name="Product_ratios", engine="openpyxl")

for row in acceptable_complete.itertuples():
    if acceptable_complete.loc[row[0], "DeadTracking"] == 1:
        acceptable_complete.loc[row[0], "ConfigKey"] = "Acceptable_BL"  # with biomass loss
        
    elif acceptable_complete.loc[row[0], "DeadTracking"] == 0:
        acceptable_complete.loc[row[0], "ConfigKey"] = "Acceptable_nonBL"  # without biomass loss


NonOptimalConfig_complete = pd.read_excel("configurationsResults_Scenario0_NonOptimalConfig_error_analysis.xlsx", sheet_name="Product_ratios", engine="openpyxl")

for row in NonOptimalConfig_complete.itertuples():
    if NonOptimalConfig_complete.loc[row[0], "DeadTracking"] == 1:
        NonOptimalConfig_complete.loc[row[0], "ConfigKey"] = "NonOptimalE_BL"  # with biomass loss
        
    elif NonOptimalConfig_complete.loc[row[0], "DeadTracking"] == 0:
        NonOptimalConfig_complete.loc[row[0], "ConfigKey"] = "NonOptimalE_nonBL"  # without biomass loss



# DATAFRAME TO EXCEL
complete_df = pd.concat([acceptable_complete, NonOptimalConfig_complete], ignore_index = True)
complete_df = complete_df.drop(["Unnamed: 0"], axis = 1)  # Remove repeated index_labels
complete_df.to_excel("configurationsResults_Scenario0_COMPLETE.xlsx", sheet_name="Complete", header=True, index=True, index_label=None)


# """
#  SHUTTED DOWN



















































