#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez, Iván Martín Martín
# April 2018, April 2021
################################

"""
EcPp3 - Glycosilation project. Preliminary Analysis of the configurationsResults.txt file:

"""


import re
import sys
import os.path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
# import shutil, errno
# import cobra
# import tabulate
# import getopt
# import copy
# import csv
# import math
# import cobra.flux_analysis.variability
# import massedit
# import subprocess
# import statistics
# import importlib
# import optlang
# import spec


# PARSING PARAMETERS
# -----------------------------------------------------------------------------
# Reading the arguments given by command line
domainName = sys.argv[1]
id_number = sys.argv[2]
# -----------------------------------------------------------------------------



###############################################################################
###############################################################################
# PRE-PROCESSING 'FLYCOP_config_V0_log'
# -----------------------------------------------------------------------------
# ERROR COUNT
ZeroDivisionError_count = 0  # Error count for ZeroDivisionError
nonOptimalSolution_count = 0  # Error count for "model solution was not optimal"

# -----------------------------------------------------------------------------
# Original Analysis of 'FLYCOP_"+domainName+"_"+id_number+"_log.txt'
# This is the logFile after FLYCOP run
# -----------------------------------------------------------------------------

input_file = "FLYCOP_"+domainName+"_"+id_number+"_log.txt"
output1 = open("nonOptimalError_configurations.txt", "w")  # in LogError directory

with open(input_file, "r") as file:  
    lines = file.readlines()
    last_error = ""
    for line in lines:
        
        if re.match("\[WARN \] \[PROCESS-ERR\]", line):
            # ZeroDivisionError case
            if re.findall("ZeroDivisionError: float division by zero", line.strip("\n")):
                ZeroDivisionError_count += 1
                last_error = "ZeroDivisionError"
                
            # Non-optimal solution case
            if re.findall("Exception: model solution was not optimal", line.strip("\n")):
                nonOptimalSolution_count += 1
                last_error = "NonOptimal"
                
        if re.match("\[ERROR\]", line) and last_error == "NonOptimal":   
            if re.findall("The following algorithm call failed", line.strip("\n")):  # NOTE THAT NEXT LINE might need to be adapted as well
                extract = re.findall("-p1_sucr1 '[-]*[0.|\d.]*[\d]+' -p2_biomassEc '[-]*[0.|\d.]*[\d]+' -p3_biomassEc_glyc '[-]*[0.|\d.]*[\d]+' -p4_frc2 '[-]*[0.|\d.]*[\d]+' -p5_biomassKT '[-]*[0.|\d.]*[\d]+' -p6_nh4_Ec '[-]*[0.|\d.]*[\d]+' -p7_nh4_KT '[-]*[0.|\d.]*[\d]+' -p8_n_models '[\w]+'", line.strip("\n"))
                output1.write(str(extract[0])+"\n")
            last_error = ""

output1.close()        


# WRITE A BRIEF ERROR SUMMARY
configs_summary = open("ConfigurationsSummary.txt", "w")  # in PreliminaryAnalysis directory   
configs_summary.write("-------------------------------------------------------\n")
configs_summary.write("ERROR SUMMARY\n")
configs_summary.write("-------------------------------------------------------\n")
configs_summary.write("Number of ZeroDivisionError configurations found: "+str(ZeroDivisionError_count)+"\n")
configs_summary.write("Number of nonOptimalSolution configurations found: "+str(nonOptimalSolution_count)+"\n")
configs_summary.write("Total of ERROR configurations found: "+str(ZeroDivisionError_count + nonOptimalSolution_count)+"\n")
configs_summary.close()



# -----------------------------------------------------------------------------
# Create a file with base configurations for non-optimal solutions (FLYCOP)
# Used in further comparison
# -----------------------------------------------------------------------------

output2 = open("nonOptimalConfigs_asStrings.txt", "w")
with open("nonOptimalError_configurations.txt", "r") as file:  
    lines = file.readlines()
    for line in lines:
        config = ""
        params = re.findall("'[-]*[0.|\d.]*[\d]+'|'[\w]'", line)  # Dudas con esta expresión: ¿funciona?

        for parameter in params:
            if re.findall("'[-]*[0.|\d.]*[\d]+'", parameter) or re.findall("'[\w]'", parameter):
                parameter = float(parameter.replace("\'", ""))
            
            config += ","+str(parameter) if config else str(parameter)
        
        output2.write(config+"\n")

output2.close()
os.remove("nonOptimalError_configurations.txt")
###############################################################################
###############################################################################



###############################################################################
###############################################################################
# FURTHER CLASSIFYING RECORDS in configurationsResults.txt file
# -----------------------------------------------------------------------------

# Read configurationsResults.txt file
# configResults = pd.read_excel("configurationsResults_Scenario"+id_number+".xlsx", header = True, engine="openpyxl")  # update python3.5
configResults = pd.read_csv("configurationsResults_Scenario"+id_number+".txt", sep = "\t", header='infer')
configResults["ConfigKey"] = "Acceptable"  # New binary classification column


# INITIAL FILTERING: NON-ACCEPTABLE (NonOptimalConfig_Error) vs. ACCEPTABLE configurations
# -----------------------------------------------------------------------------
# Check if the file is empty (i.e. no 'nonOptimal' configurations found)
nonOptimal_flag = True if os.path.getsize("nonOptimalConfigs_asStrings.txt") else False

if nonOptimal_flag: 
    nonOptimal_file = pd.read_csv("nonOptimalConfigs_asStrings.txt", sep="\t", header='infer')  # Single column (configuration of parameters)
    
    for row in nonOptimal_file.itertuples():
        bad_config = row[1]
        
        for row in configResults.itertuples():
            if configResults[configResults.BaseConfig == bad_config]: configResults[row[0], "ConfigKey"] = "NonOptimal"
        
        
    
# FURTHER SORTING:   
# -----------------------------------------------------------------------------
# Sorting by 'ConfigKey': first 'Acceptable', then 'NonOptimal' configurations // Asegurar
# Sorting by 'ID_SD': excessive SD at the end of each group
# Within the last group, from highest to lowest fitness value
configResults = configResults.sort_values(by=["ConfigKey", 'ID_SD', 'fitFunc'], ascending=[True, True, False])  # CHANGE sorting_order if desired


# Remove repeated index_labels
for column in configResults.columns:  
    configResults = configResults.drop([column], axis = 1) if re.findall("Unnamed: .*", column) else configResults
    
# Save modified configurationsResults.txt file (overwritting last file)
configResults.to_csv("configurationsResults_Scenario"+id_number+".txt", sep = "\t", header='infer', index = False)
###############################################################################


# WRITE A BRIEF SUMMARY OF ACCEPTABLE vs. NON-ACCEPTABLE
# ------------------------------------------------------
configs_summary = open("ConfigurationsSummary.txt", "a")  # in PreliminaryAnalysis directory   
configs_summary.write("\n\n\n-------------------------------------------------------\n")
configs_summary.write("BRIEF SUMMARY OF CONFIGURATIONS\n")
configs_summary.write("-------------------------------------------------------\n")


# -------------------------
# ACCEPTABLE configurations
# -------------------------
configResults_acceptable = configResults[configResults["ConfigKey"] == "Acceptable"]  # Fraction of dataframe 'Acceptable'

# Biomass Loss
biomass_loss_cases_acc = configResults_acceptable[configResults_acceptable["DeadTracking"] == 1]
biomass_loss_cases_accSD_acc = biomass_loss_cases_acc[biomass_loss_cases_acc["ID_SD"] == 0]

# No Biomass Loss
non_biomass_loss_cases_acc = configResults_acceptable[configResults_acceptable["DeadTracking"] == 0]
non_biomass_loss_cases_accSD_acc = non_biomass_loss_cases_acc[non_biomass_loss_cases_acc["ID_SD"] == 0]

configs_summary.write("ACCEPTABLE CONFIGURATIONS\n")
configs_summary.write("-------------------------------------------------------")

configs_summary.write("\nTotal of acceptable configurations: "+str(len(configResults_acceptable))+"\n")
configs_summary.write("\nTotal of acceptable configurations with biomass loss: "+str(biomass_loss_cases_acc.count()[0])+"\n")
configs_summary.write("\t - of which, the number of configurations with ACCEPTABLE SD (< 10% avgFit) is: "+str(biomass_loss_cases_accSD_acc.count()[0])+"\n")

configs_summary.write("\nTotal of acceptable configurations with NO biomass loss: "+str(non_biomass_loss_cases_acc.count()[0])+"\n")
configs_summary.write("\t - of which, the number of configurations with ACCEPTABLE SD (< 10% avgFit) is: "+str(non_biomass_loss_cases_accSD_acc.count()[0])+"\n\n")


# Fraction of dataframe 'Acceptable' with acceptable SD for further plotting
# NO further subdivision in biomass loss vs. non-biomass loss
# -----------------------------------------------------------------------------
configResults_acceptable_SDok = configResults_acceptable[configResults_acceptable["ID_SD"] == 0]


# ------------------------------------------------------
# NON-ACCEPTABLE (NonOptimalConfig_Error) configurations
# ------------------------------------------------------

configs_summary.write("\nNON-OPTIMAL CONFIGURATIONS\n")
configs_summary.write("-------------------------------------------------------")

if nonOptimal_flag:
    configResults_nonOpt = configResults[configResults["ConfigKey"] == "NonOptimal"]  # Fraction of dataframe 'NonOptimal'
    
    # Biomass Loss
    biomass_loss_cases_nonOpt = configResults_nonOpt[configResults_nonOpt["DeadTracking"] == 1]
    biomass_loss_cases_accSD_nonOpt = biomass_loss_cases_nonOpt[biomass_loss_cases_nonOpt["ID_SD"] == 0]
    
    # No Biomass Loss
    non_biomass_loss_cases_nonOpt = configResults_nonOpt[configResults_nonOpt["DeadTracking"] == 0]
    non_biomass_loss_cases_accSD_nonOpt = non_biomass_loss_cases_nonOpt[non_biomass_loss_cases_nonOpt["ID_SD"] == 0]
    
    
    configs_summary.write("\nTotal of configurations with NonOptimalConfig_error: "+str(len(configResults_nonOpt))+"\n")
    configs_summary.write("\nTotal of configurations with NonOptimalConfig_error and biomass loss: "+str(biomass_loss_cases_nonOpt.count()[0])+"\n")
    configs_summary.write("\t - of which, the number of configurations with ACCEPTABLE SD (< 10% avgFit) is: "+str(biomass_loss_cases_accSD_nonOpt.count()[0])+"\n")
    
    configs_summary.write("\nTotal of configurations with NonOptimalConfig_error and NO biomass loss: "+str(non_biomass_loss_cases_nonOpt.count()[0])+"\n")
    configs_summary.write("\t - of which, the number of configurations with ACCEPTABLE SD (< 10% avgFit) is: "+str(non_biomass_loss_cases_accSD_nonOpt.count()[0])+"\n\n")
    
    # Fraction of dataframe 'NonOptimal' with acceptable SD for further plotting
    # NO further subdivision in biomass loss vs. non-biomass loss
    # -------------------------------------------------------------------------
    configResults_nonOpt_SDok = configResults_nonOpt[configResults_nonOpt["ID_SD"] == 0]

else:
    configs_summary.write("\nNon-optimal configurations not found\n")


# ---------------------
configs_summary.close()
###############################################################################
###############################################################################



###############################################################################
###############################################################################
# PLOTTING THE DISTRIBUTION OF CONFIGURATIONS DEPENDING ON CONSORTIUM ARCHITECTURE
# --------------------------------------------------------------------------------


def basic_boxplot_scatter(dataframe, x_var, y_var, x_label, y_label, filename, plot_title):
    
    fig = plt.figure(num=0, clear=True, figsize=(7, 7))
    ax_boxplot = sns.boxplot(x = x_var, y = y_var, data = dataframe, boxprops=dict(alpha=0.2))
    sns.stripplot(x=x_var, y=y_var, jitter = True, data = dataframe)
    ax_boxplot.set(xlabel = x_label, ylabel = y_label)
    
    plt.title(plot_title, fontsize = 14)
    fig.savefig(filename+".png")
    plt.close(fig)


# y_variable_count: Nombre de la columna sobre la que se cuenta para la altura de cada barra en el barplot
# x_categories: Lista ordenada de categorías en eje x
def basic_barplot(dataframe, y_variable_count, y_categories, x_categories, x_label, y_label, filename, plot_title):
    
    # Lists for each y_category, depending on the y_variable_count (Dictionary format)
    y_counts_dict = {}
    for y_category in y_categories:
        y_cat_values = []
        for x_category in x_categories: 
            x_category_prefilter_df = dataframe[dataframe["ConfigKey"] == x_category]
            y_cat_values.append(x_category_prefilter_df[x_category_prefilter_df[y_variable_count] == y_category].count()[0])
            y_counts_dict[y_category] = y_cat_values
    
    # Create figure
    # fig = plt.figure(num=0, clear=True, figsize=(7, 7))   
    fig, axes = plt.subplots(num=0, clear=True, figsize=(7, 7))

    colors = cm.rainbow(np.linspace(0, 1, len(y_categories)))
    bottom_flag = False
    
    for n_categories in range(len(y_categories)):
        if not bottom_flag:
            axes.bar(x_categories, y_counts_dict[y_categories[n_categories]], color=colors[n_categories], label=y_categories[n_categories])
            bottom = np.array(y_counts_dict[y_categories[n_categories]])
            bottom_flag = True
        else:
            axes.bar(x_categories, y_counts_dict[y_categories[n_categories]], color=colors[n_categories], bottom=bottom, label=y_categories[n_categories])
            bottom = bottom + np.array(y_counts_dict[y_categories[n_categories]])
    
    # Legend, labels, title
    plt.legend(loc="lower left", bbox_to_anchor=(0.8,1.0))
    plt.ylabel(y_label)
    plt.xlabel(x_label)  
    plt.title(plot_title, fontsize = 12)
    
    # Adjust y-axis
    # plt.ylim(top=len(dataframe))
    plt.yticks(np.linspace(0, len(dataframe), len(dataframe)//10))
    
    # Bar labels
    bars = axes.patches  # Bars
    labels = [bars[i].get_height() for i in range(len(bars))]  # Labels
    prev_height = 0
    
    for bar, label in zip(bars, labels):
        height = bar.get_height() + prev_height
        prev_height = height
        axes.text(bar.get_x() + bar.get_width() / 2, height - 10, label, fontfamily='sans', fontsize=12, color = "black")

    # Save and close figure
    fig.savefig(filename+".png")
    plt.close(fig)


# CONSIDER WHETHER NON-OPTIMAL CONFIGURATIONS WERE FOUND OR NOT
# -------------------------------------------------------------
if nonOptimal_flag:  # NonOptimal configurations found
    combined_configResults_SDok = pd.concat([configResults_acceptable_SDok, configResults_nonOpt_SDok], ignore_index = True)  # Combined dataframe for plotting
    model_architecture_categories = combined_configResults_SDok["Consortium_Arch"].unique().tolist()
    
    # BARPLOT OF MODEL ARCHITECTURE vs. Acceptable or NonOptimal configurations
    basic_barplot(combined_configResults_SDok, y_variable_count="Consortium_Arch", y_categories = model_architecture_categories, 
                  x_categories=["Nonoptimal", "Acceptable"], x_label="Configuration Key", y_label="Consortium Architecture", 
                  filename="consortiumArchitectureEvaluation", plot_title="Consortium Architecture Evaluation I")
    
    # --------------------------------------------------------------------------------------
    # ConfigKey classification with further subdivision of biomass loss vs. non-biomass loss
    # --------------------------------------------------------------------------------------
    
    # NON-OPTIMAL CONFIGURATIONS
    configResults_nonOpt_SDok_nonBL = configResults_nonOpt_SDok[configResults_nonOpt_SDok["DeadTracking"] == 0]
    configResults_nonOpt_SDok_nonBL["ConfigKey"] = "Nonoptimal_nonBL" 
    
    configResults_nonOpt_SDok_BL = configResults_nonOpt_SDok[configResults_nonOpt_SDok["DeadTracking"] == 1]
    configResults_nonOpt_SDok_BL["ConfigKey"] = "Nonoptimal_BL"
    
    combined_nonOptimal = pd.concat([configResults_nonOpt_SDok_nonBL, configResults_nonOpt_SDok_BL], ignore_index = True)  # Combined dataframe (Non-optimal)
    
    
    # ACCEPTABLE CONFIGURATIONS
    configResults_acceptable_SDok_nonBL = configResults_acceptable_SDok[configResults_acceptable_SDok["DeadTracking"] == 0]
    configResults_acceptable_SDok_nonBL["ConfigKey"] = "Acceptable_nonBL"
    
    configResults_acceptable_SDok_BL = configResults_acceptable_SDok[configResults_acceptable_SDok["DeadTracking"] == 1]
    configResults_acceptable_SDok_BL["ConfigKey"] = "Acceptable_BL" 
    
    combined_acceptable = pd.concat([configResults_acceptable_SDok_nonBL, configResults_acceptable_SDok_BL], ignore_index = True)  # Combined dataframe (acceptable)
    
    
    # FINAL COMBINED DATAFRAME
    final_combined = pd.concat([combined_nonOptimal, combined_acceptable], ignore_index = True)  # biomass loss + non-biomass loss
    # final_combined_nonBL = pd.concat([configResults_nonOpt_SDok_nonBL, configResults_acceptable_SDok_nonBL], ignore_index = True)  # just non-biomass loss
    model_architecture_categories = final_combined["Consortium_Arch"].unique().tolist()
    
    
    # BARPLOT OF MODEL ARCHITECTURE vs. Acceptable or NonOptimal configurations, with further subdivision of biomass loss vs. non-biomass loss
    basic_barplot(final_combined, y_variable_count="Consortium_Arch", y_categories = model_architecture_categories,
                  x_categories=["Nonoptimal_nonBL", "Nonoptimal_BL", "Acceptable_nonBL", "Acceptable_BL"], 
                  x_label="Configuration Key (BL vs. nonBL)", y_label="Consortium Architecture", 
                  filename="consortiumArchitectureEvaluation_BLvsnonBL", plot_title="Consortium Architecture Evaluation II")
    
    # --------------------------------------------------------------------------------------
    # ConfigKey classification with further subdivision depending on model architecture
    # Acceptable + Non-optimal configurations:
    #     - with acceptable SD
    #     - without biomass loss
    # --------------------------------------------------------------------------------------
    
    # NON-OPTIMAL CONFIGURATIONS
    configResults_nonOpt_SDok_nonBL_2models = configResults_nonOpt_SDok_nonBL[configResults_nonOpt_SDok_nonBL["Consortium_Arch"] == "2models"]
    configResults_nonOpt_SDok_nonBL_2models["ConfigKey"] = "Acceptable_2models"
    
    configResults_nonOpt_SDok_nonBL_3models = configResults_nonOpt_SDok_nonBL[configResults_nonOpt_SDok_nonBL["Consortium_Arch"] == "3models"]
    configResults_nonOpt_SDok_nonBL_3models["ConfigKey"] = "Acceptable_3models"
    
    combined_nonOptimal = pd.concat([configResults_nonOpt_SDok_nonBL_2models, configResults_nonOpt_SDok_nonBL_3models], ignore_index = True)  # Combined dataframe (non-optimal)
    
    
    # ACCEPTABLE
    configResults_acceptable_SDok_nonBL_2models = configResults_acceptable_SDok_nonBL[configResults_acceptable_SDok_nonBL["Consortium_Arch"] == "2models"]
    configResults_acceptable_SDok_nonBL_2models["ConfigKey"] = "Acceptable_2models"
    
    configResults_acceptable_SDok_nonBL_3models = configResults_acceptable_SDok_nonBL[configResults_acceptable_SDok_nonBL["Consortium_Arch"] == "3models"]
    configResults_acceptable_SDok_nonBL_3models["ConfigKey"] = "Acceptable_3models"
    
    combined_acceptable = pd.concat([configResults_acceptable_SDok_nonBL_2models, configResults_acceptable_SDok_nonBL_3models], ignore_index = True)  # Combined dataframe (acceptable)
    
    
    # FINAL COMBINED DATAFRAME
    final_combined = pd.concat([combined_nonOptimal, combined_acceptable], ignore_index = True)  # biomass loss + non-biomass loss
    
    # PLOT OF FITNESS vs. Acceptable or NonOptimal configurations, with further subdivision depending on model architecture (categorical, scatter-boxplot)
    basic_boxplot_scatter(final_combined, "ConfigKey", "fitFunc", "Configuration Key - model arch", "Fitness (mM/gL)",
                          "consortiumArchitectureEvaluation_fitness", "Consortium Architecture Evaluation III")
    
else:  # NonOptimal configurations NOT found

    # --------------------------------------------------------------------------------------
    # ACCEPTABLE CONFIGURATIONS with further subdivision of biomass loss vs. non-biomass loss
    # --------------------------------------------------------------------------------------

    configResults_acceptable_SDok_nonBL = configResults_acceptable_SDok[configResults_acceptable_SDok["DeadTracking"] == 0]
    configResults_acceptable_SDok_nonBL["ConfigKey"] = "Acceptable_nonBL"
    
    configResults_acceptable_SDok_BL = configResults_acceptable_SDok[configResults_acceptable_SDok["DeadTracking"] == 1]
    configResults_acceptable_SDok_BL["ConfigKey"] = "Acceptable_BL" 
    
    combined_acceptable = pd.concat([configResults_acceptable_SDok_nonBL, configResults_acceptable_SDok_BL], ignore_index = True)  # Combined dataframe (non-optimal)
    model_architecture_categories = combined_acceptable["Consortium_Arch"].unique().tolist()

    # BARPLOT OF MODEL ARCHITECTURE vs. Acceptable config with / without biomass loss (categorical, scatter-boxplot)
    basic_barplot(combined_acceptable, y_variable_count="Consortium_Arch", y_categories = model_architecture_categories, 
                  x_categories=["Acceptable_nonBL", "Acceptable_BL"], x_label="Acceptable config - BL vs. nonBL", y_label="Consortium Architecture", 
                  filename="consortiumArchitectureEvaluation_BLvsnonBL", plot_title="Consortium Architecture Evaluation I")
    
    # --------------------------------------------------------------------------------------
    # ACCEPTABLE CONFIGURATIONS with further subdivision of biomass loss vs. non-biomass loss
    #     - with acceptable SD
    #     - without biomass loss
    # --------------------------------------------------------------------------------------

    # ACCEPTABLE
    configResults_acceptable_SDok_nonBL_2models = configResults_acceptable_SDok_nonBL[configResults_acceptable_SDok_nonBL["Consortium_Arch"] == "2models"]
    configResults_acceptable_SDok_nonBL_2models["ConfigKey"] = "Acceptable_2models"
    
    configResults_acceptable_SDok_nonBL_3models = configResults_acceptable_SDok_nonBL[configResults_acceptable_SDok_nonBL["Consortium_Arch"] == "3models"]
    configResults_acceptable_SDok_nonBL_3models["ConfigKey"] = "Acceptable_3models"
    
    combined_acceptable = pd.concat([configResults_acceptable_SDok_nonBL_2models, configResults_acceptable_SDok_nonBL_3models], ignore_index = True)  # Combined dataframe (acceptable)

    # PLOT OF FITNESS vs. Acceptable or NonOptimal configurations, with further subdivision depending on model architecture (categorical, scatter-boxplot)
    basic_boxplot_scatter(combined_acceptable, "ConfigKey", "fitFunc", "Acceptable: BL vs. non BL - model arch", "Fitness (mM/gL)",
                          "consortiumArchitectureEvaluation_fitness", "Consortium Architecture Evaluation II")

###############################################################################
###############################################################################



###############################################################################
###############################################################################
# BOXPLOTS: categorical comparison of consortium architecture
# y-axis
    # Input variables: sucrose and fructose uptake rates, E.coli and KT NH4 uptake rates
    # Global final biomass (all microbes)
    # Fitness
# -----------------------------------------------------------------------------

# Read UPDATED configurationsResults.txt file
# configResults = pd.read_excel("configurationsResults_Scenario"+id_number+".xlsx", header = True, engine="openpyxl")  # update python3.5
configResults = pd.read_csv("configurationsResults_Scenario"+id_number+".txt", sep = "\t", header='infer')
# Fraction of dataframe 'Acceptable' with acceptable SD for further plotting
configResults_acceptable_SDok = configResults[configResults["ID_SD"] == 0]


def basic_boxplot_scatter_ax(ax, dataframe, x_var, y_var, x_label, y_label):
    sns.stripplot(ax=ax, x=x_var, y=y_var, jitter = True, data = dataframe)
    ax_boxplot = sns.boxplot(ax=ax, x = x_var, y = y_var, data = dataframe, boxprops=dict(alpha=0.2))
    ax_boxplot.set(xlabel = x_label, ylabel = y_label)


# Global Plot
global_figure, axes = plt.subplots(num=0, clear=True, figsize=(15, 15), nrows=2, ncols=3)
global_figure.suptitle("BoxPlots - categorical comparison of consortium architecture", fontsize = 24, fontfamily='DejaVu Sans')

# Subplots
basic_boxplot_scatter_ax(axes[0, 0], configResults_acceptable_SDok, "Consortium_Arch", "sucr_upt", "Consortium Architecture", "Sucrose uptake rate (mmol/ g DW h)")
basic_boxplot_scatter_ax(axes[1, 0], configResults_acceptable_SDok, "Consortium_Arch", "frc_upt", "Consortium Architecture", "Fructose uptake rate (mmol/ g DW h)")
basic_boxplot_scatter_ax(axes[0, 1], configResults_acceptable_SDok, "Consortium_Arch", "nh4_Ec", "Consortium Architecture", "NH4 uptake rate (mmol/ g DW h) - E.coli")
basic_boxplot_scatter_ax(axes[1, 1], configResults_acceptable_SDok, "Consortium_Arch", "nh4_KT", "Consortium Architecture", "NH4 uptake rate (mmol/ g DW h) - KT")
basic_boxplot_scatter_ax(axes[0, 2], configResults_acceptable_SDok, "Consortium_Arch", "Final_Biomass", "Consortium Architecture", "Global final biomass (gL-1)")
basic_boxplot_scatter_ax(axes[1, 2], configResults_acceptable_SDok, "Consortium_Arch", "fitFunc", "Consortium Architecture", "Fitness (mM / gL-1")

# Save and close global_figure
global_figure.savefig("model_architecture_boxplots.png")
plt.close(global_figure)


###############################################################################
# HEATMAP with input configuration values (values of parameters optimized by SMAC)
# Note that two different heatmaps are obtained:
    # 2models consortium architecture
    # 3models consortium architecture
# -----------------------------------------------------------------------------

# HEATMAP 2models
# ===============
heatmap_2models_df = configResults_acceptable_SDok[configResults_acceptable_SDok["Consortium_Arch"] == "2models"]

# Continuous SMAC variables for the heatmap (column names in the configurationsResults file)
heatmap_variables = ["sucr_upt", "InitEc", "frc_upt", "Init_KT", "nh4_Ec", "nh4_KT", "fitFunc", "SD"]
for column in heatmap_2models_df.columns:
    heatmap_2models_df = heatmap_2models_df.drop(columns=column) if column not in heatmap_variables else heatmap_2models_df

# Figure
heatmap_2models = plt.figure(figsize=(25, 15))
plt.title("HeatMap - input variables for 2models", fontsize = 20, fontfamily='DejaVu Sans')
sns.heatmap(heatmap_2models_df.corr(), annot=True, cmap="bwr")
heatmap_2models.savefig("heatmap_2models.png")
plt.close(heatmap_2models)


# HEATMAP 3models
# ===============
heatmap_3models_df = configResults_acceptable_SDok[configResults_acceptable_SDok["Consortium_Arch"] == "3models"]

# Continuous SMAC variables for the heatmap (column names in the configurationsResults file)
heatmap_variables = ["sucr_upt", "InitEc", "InitEc_glyc", "frc_upt", "Init_KT", "nh4_Ec", "nh4_KT", "fitFunc", "SD"]
for column in heatmap_3models_df.columns:
    heatmap_3models_df = heatmap_3models_df.drop(columns=column) if column not in heatmap_variables else heatmap_3models_df

# Figure
heatmap_3models = plt.figure(figsize=(25, 15))
plt.title("HeatMap - input variables for 3models", fontsize = 20, fontfamily='DejaVu Sans')
sns.heatmap(heatmap_3models_df.corr(), annot=True, cmap="bwr")
heatmap_3models.savefig("heatmap_3models.png")
plt.close(heatmap_3models)

###############################################################################
###############################################################################































