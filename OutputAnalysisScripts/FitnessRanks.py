#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 21:20:59 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Series of functions to define and process fitness ranks (utility for further scripts)
    
EXPECTED INPUT

    - Dataframe: dataframe to be processed
    - rank_limits_set: tuple with a series of smaller tuples (fitness rank intervals)
    - rank_limits: smaller tuple (fitness rank individual interval)
    
    - ref_colum: reference column to extract the fraction of the dataframe. Default :'fitness'
    - frac_dataframe: fraction of a particular dataframe
    - descr_columns: columns to be described with 'Pandas' statistical description (method .describe())
    
        
OUTPUT

    See each particular function
    
NOTE THAT:
    
    Script in development (...)
    
"""

# import re
import pandas as pd
import os.path


# RETURNS FRACTION OF INTEREST (fitness rank, all columns) OF THE DATAFRAME 
def obtain_fitness_rank(rank_limits, dataframe, ref_colum):
    frac_dataframe = dataframe[dataframe[ref_colum] < rank_limits[1]]  # Higher limit
    final_frac_dataframe = frac_dataframe[frac_dataframe[ref_colum] > rank_limits[0]]  # Lower limit
    return final_frac_dataframe
    

# STATISTICAL DESCRIPTION for the selected fitness rank, columns selected 
def stats_description(frac_dataframe, descr_columns):
    stat_description = frac_dataframe[descr_columns].describe()
    return stat_description


# COMBINES TWO LAST FUNCTIONS
def describe_fitness_ranks(rank_limits_set, dataframe, descr_columns, ref_column):
    
    """  'SAVE STATS' version
    filename = "stats_description.txt"  # Valorar qué nombre
    with open(filename, "w") as stats_file:
        for rank_limits_tuple in rank_limits_set:
            fitness_rank = obtain_fitness_rank(rank_limits_tuple, dataframe, ref_column)
            stat_descr = stats_description(fitness_rank, descr_columns)
            stats_file.write(stat_descr+"\n")
    """
        
    # 'PRINT' version
    for rank_limits_tuple in rank_limits_set:
        fitness_rank = obtain_fitness_rank(rank_limits_tuple, dataframe, ref_column)
        stat_descr = stats_description(fitness_rank, descr_columns)
        print(f"{ref_column} rank: {rank_limits_tuple[0]}-{rank_limits_tuple[1]}")   
        print(stat_descr)
        print()
    
    
# LIMITACIONES
# ------------
# Limitación: el primero de los rangos, hay que pasarle un límite superior más alto que el mejor de los fitness
# Limitación: cálculos individuales de un único parámetro estadístico. Véase mean(), median() (individualmente) 


# AUTOMATIZAR
# -------------------------------
# Set con tuplas para los rangos
# NUEVA IDEA: llevar análisis estadístico a archivo para posterior 'ComparativeAnalysis' entre configuraciones
    # Array 3D
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# DEFINES FITNESS RANKS (new column 'FitRank') for the Comparative Analysis within the FLYCOP run
def organize_fitness_ranks(dataframe, rank_limits_set, ref_column):
    
    for row in dataframe.itertuples():  # row[0] = Index Number
        ref_variable = dataframe.loc[row[0], ref_column]
        
        for i in range(1, len(rank_limits_set)+1):
            rank_tuple = rank_limits_set[i-1]
                
            if rank_tuple[0] < ref_variable < rank_tuple[1]:
                dataframe.loc[row[0], "Rank"] = int(i)
                break
                
            elif ref_variable == 0:
                ConfigError = dataframe.loc[row[0] , "ZeroDivisionError"]
                
                if ConfigError == 0:
                    dataframe.loc[row[0] , "Rank"] = 0
                else:
                    dataframe.loc[row[0] , "Rank"] = -1
    return dataframe
# -----------------------------------------------------------------------------


# -8.0,0.35,-10.0,0.25
# EXTRACT UPTAKE RATES RATIO AND INITIAL BIOMASS RATIO from a string-line configuration
def extract_ratios(string_line_config):
    list_line = string_line_config.split(",")
    
    sucr_ur = float(list_line[0])
    frc_ur = float(list_line[2])
    uptake_ratio = round(sucr_ur/frc_ur, 3)
    
    Ec_init = float(list_line[1])
    KT_init = float(list_line[3])
    initbiomass_ratio = round(Ec_init/KT_init, 3)
    
    return uptake_ratio, initbiomass_ratio







































































