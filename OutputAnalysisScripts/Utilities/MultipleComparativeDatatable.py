#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 23:49:14 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION - TABLE CREATION FOR FURTHER ANALYSIS IN MULTIPLE COMPARATIVE ANALYSIS (several FLYCOP runs)

    Series of functions to apply in "MultipleComparativeAnalysis.py" script or others similar.
    These functions filter and extract interesting information about FLYCOP runs, deppending on their initial input conditions.
        
        - counter_limiting_nuts_carbon_source()
        - counter_limiting_nuts_carbon_source_descriptive()
        
        - counter_death_effect()
        - counter_death_effect_descriptive()
    
    
    (See each particular function for detailed description)
    
NOTE THAT:
    
    xxx
    
"""

import pandas as pd

# -----------------------------------------------------------------------------
# FUNCTION TO ORGANIZE IN A TABLE:
    # - number of cases of final low concentration
    # - number of cases of final intermediate concentration
    # - number of cases of final high concentration
    
# for a series of given nutrients, and a given 'key' (i.e. FLYCOP run)

# INPUT
# -----
# comparison_df: reference (comparison) dataframe with several keys (i.e. FLYCOP runs)

# key (string) (i.e. FLYCOP runs)

# Reference nutrients (strings): limNut1, limNut2, carbon_source

# Ranges to organize final concentrations of a given nutrient: (lower_bound, upper_bound).
# Those values within these limits would be considered intermediate concentrations.
# range_limNut1, range_limNut2, range_carbon_source


# DATATABLE STRUCTURE (a table for every key in comparison_df)
# -------------------
    # Rows: concentration intervals
    # Columns: nutrient

# ROW_NAMES
    # First row: low concentration ("FinalLow")
    # Second row: intermediate concentration ("FinalMed")
    # Third row: high concentration ("FinalHigh")
# -----------------------------------------------------------------------------


def counter_limiting_nuts_carbon_source(comparison_df, key, range_limNut1, limNut1, range_limNut2, limNut2, range_carbon_source, carbon_source):

    # Limiting Nutrient 1
    low_limNut1 = 0
    intermediate_limNut1 = 0
    high_limNut1 = 0
        
    # Limiting Nutrient 2
    low_limNut2 = 0
    intermediate_limNut2 = 0
    high_limNut2 = 0
        
    # Carbon source
    low_carbon_source = 0
    intermediate_carbon_source = 0
    high_carbon_source = 0
    
    for row in comparison_df[comparison_df["Key"] == key].itertuples():
            
        limNut1 = comparison_df.loc[row[0], limNut1]
        limNut2 = comparison_df.loc[row[0], limNut2]
        carbon_source = comparison_df.loc[row[0], carbon_source]

        # Limiting Nutrient 1
        if limNut1 < range_limNut1[0]:
            low_limNut1 += 1
        elif range_limNut1[0] < limNut1 < range_limNut1[1]:
            intermediate_limNut1 += 1
        elif range_limNut1[1] < limNut1:
            high_limNut1 += 1
        limNut1_column = [low_limNut1, intermediate_limNut1, high_limNut1]

        # Limiting Nutrient 2
        if limNut2 < range_limNut2[0]:
            low_limNut2 += 1
        elif range_limNut2[0] < limNut2 < range_limNut2[1]:
            intermediate_limNut2 += 1
        elif range_limNut2[1] < limNut2:
            high_limNut2 += 1
        limNut2_column = [low_limNut2, intermediate_limNut2, high_limNut2],

        # Carbon source
        if carbon_source < range_carbon_source[0]:
            low_carbon_source += 1
        elif range_carbon_source[0] < carbon_source < range_carbon_source[1]:
            intermediate_carbon_source += 1
        elif range_carbon_source[1] < carbon_source:
            high_carbon_source += 1
        carbon_source_column = [low_carbon_source, intermediate_carbon_source, high_carbon_source]
        
    
    counter_df = pd.DataFrame(index=["FinalLow", "FinalMed", "FinalHigh"], 
                              columns = [limNut1_column, limNut2_column, carbon_source_column],
                              data = [limNut1, limNut2, carbon_source])
             
    return counter_df


# -----------------------------------------------------------------------------
# DESCRIPTIVE FUNCTION ASSOCIATED TO LAST FUNCTION: "counter_limiting_nuts_carbon_source()"

# Prints the number of final values with low, intermediate and high concentration for
# the provided nutrients, in the analyzed FLYCOP run

# INPUT
# -----
# counter_dataframe: dataframe returned by last function, "counter_limiting_nuts_carbon_source()"
# Key: name of the configuration to be printed (string)
# Names of nutrients considered: limNut1, limNut2, carbon_source (strings)
# -----------------------------------------------------------------------------

def counter_limiting_nuts_carbon_source_descriptive(counter_dataframe, key, limNut1, limNut2, carbon_source):
    
    # CONFIGURATION
    print("\n----------------------------------------------------------------")
    print("CONFIGURATION: ", key)
    
    # Limiting Nutrient 1
    print("\nNUTRIENT: ", limNut1)  
    print(f"Number of cases of final low {limNut1} concentration: ", counter_dataframe.loc["FinalLow", limNut1])
    print(f"Number of cases of final intermediate {limNut1} concentration: ", counter_dataframe.loc["FinalMed", limNut1])
    print(f"Number of cases of final high {limNut1} concentration: ", counter_dataframe.loc["FinalHigh", limNut1])
        
    # Limiting Nutrient 2
    print("\nNUTRIENT: ", limNut2)  
    print(f"Number of cases of final low {limNut2} concentration: ", counter_dataframe.loc["FinalLow", limNut2])
    print(f"Number of cases of final intermediate {limNut2} concentration: ", counter_dataframe.loc["FinalMed", limNut2])
    print(f"Number of cases of final high {limNut2} concentration: ", counter_dataframe.loc["FinalHigh", limNut2])
        
    # Carbon source
    print("\nNUTRIENT: ", carbon_source)  
    print(f"Number of cases of final low {carbon_source} concentration: ", counter_dataframe.loc["FinalLow", carbon_source])
    print(f"Number of cases of final intermediate {carbon_source} concentration: ", counter_dataframe.loc["FinalMed", carbon_source])
    print(f"Number of cases of final high {carbon_source} concentration: ", counter_dataframe.loc["FinalHigh", carbon_source])
    print("----------------------------------------------------------------\n")

# =============================================================================
# FURTHER OPTIMIZATION FOR  THESE LAST FUNCTIONS: pandas multiindex
"""
midx = pd.MultiIndex(levels=[['lama', 'cow', 'falcon'],
                             ['speed', 'weight', 'length']],
                     codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],
                            [0, 1, 2, 0, 1, 2, 0, 1, 2]])
"""
# =============================================================================





# -----------------------------------------------------------------------------
# FUNCTION TO ORGANIZE IN A TABLE:
    # - number of cases with death effect
    # - number of cases with death effect + limNut1 exhaustion
    # - number of cases with death effect + limNut2 exhaustion
    # - number of cases with death effect + limNut1 and limNut2 exhaustion
    # - number of cases with death effect + carbon source exhaustion
    

# INPUT
# -----
# comparison_df: reference (comparison) dataframe with several keys (i.e. FLYCOP runs)

# Reference nutrients (strings): limNut1, limNut2, carbon_source
# Death effect reference column (string): death_eff_column

# Exhaustion cutoff for limiting nutrients (integer or float)
# Exhaustion cutoff for carbon source (integer or float)


# DATATABLE STRUCTURE
# -------------------
    # rows: FLYCOP runs
    # columns: death_effect counter

# ROW_NAMES not available

    # First row: DeathEff
    # Second row: DeathEff+L1
    # Third row: DeathEff+L2
    # Fourth row: DeathEff+L12
    # Fifth row: DeathEff+CS
# -----------------------------------------------------------------------------

def counter_death_effect(comparison_df, limNut1, limNut2, carbon_source, death_eff_column, exhaustion_cutoff = 1, exhaustion_carbon_source = 1):

    counter_df = pd.DataFrame()  # FINAL COUNT DATAFRAME
    for key in comparison_df["Key"].unique():
        
        # Death effect cases (total)
        death_eff_counter = 0
        
        # Death effect cases + limNut1 exhaustion
        death_eff_ex1 = 0
        
        # Death effect cases + limNut2 exhaustion
        death_eff_ex2 = 0
        
        # Death effect cases + limNut1 and limNut2 exhaustion
        death_eff_ex12 = 0

        # Death effect cases + carbon exhaustion
        death_eff_carbon = 0
        
        
        for row in comparison_df[comparison_df["Key"] == key].itertuples():
            
            limNut1 = comparison_df.loc[row[0], limNut1]
            limNut2 = comparison_df.loc[row[0], limNut2]
            carbon_source = comparison_df.loc[row[0], carbon_source]
            death_effect = comparison_df.loc[row[0], death_eff_column]  # 1, biomass loss; 0, no biomass loss
            
            # Death effect cases (total)
            if death_effect: 
                death_eff_counter += 1
        
            # Death effect cases + limNut1 exhaustion
            if death_effect and limNut1 < exhaustion_cutoff:
                death_eff_ex1 += 0
        
            # Death effect cases + limNut2 exhaustion
            if death_effect and limNut2 < exhaustion_cutoff:
                death_eff_ex2 += 0
        
            # Death effect cases + limNut1 and limNut2 exhaustion
            if death_effect and (limNut1 < exhaustion_cutoff and limNut2 < exhaustion_cutoff):
                death_eff_ex12 += 0
        
            # Death effect cases + carbon exhaustion
            if death_effect and carbon_source < exhaustion_carbon_source:
                death_eff_carbon += 1
            
            # Final column to include in Dataframe
            key_column = [death_eff_counter, death_eff_ex1, death_eff_ex2, death_eff_ex12, death_eff_carbon]
        
        
        if not counter_df:
            counter_df = pd.DataFrame(index=["DeathEff", "DeathEff+L1", "DeathEff+L2", "DeathEff+L12", "DeathEff+CS"], 
                                      columns = key,
                                      data = key_column)
        else:
            counter_df[key] = key_column

            
    return counter_df


# -----------------------------------------------------------------------------
# DESCRIPTIVE FUNCTION ASSOCIATED TO LAST FUNCTION: "counter_death_effect()"

# Prints the number of final values with:
    # - number of cases with death effect
    # - number of cases with death effect + limNut1 exhaustion
    # - number of cases with death effect + limNut2 exhaustion
    # - number of cases with death effect + limNut1 and limNut2 exhaustion
    # - number of cases with death effect + carbon source exhaustion
    
# INPUT
# -----
# counter_dataframe: dataframe returned by last function, "counter_death_effect()"
# Names of nutrients considered: limNut1, limNut2, carbon_source (strings)
# -----------------------------------------------------------------------------

def counter_death_effect_descriptive(counter_dataframe, limNut1, limNut2, carbon_source):
    
    for key in list(counter_dataframe):  # Iterate over columns
        # CONFIGURATION
        print("\n----------------------------------------------------------------")
        print("CONFIGURATION: ", key)
        
        # Counter-Printer
        print("Number of cases with death effect: ", counter_dataframe.loc["DeathEff", key])
        print(f"Number of cases with death effect and final exhaustion of {limNut1}: ", counter_dataframe.loc["DeathEff+L1", key])
        print(f"Number of cases with death effect and final exhaustion of {limNut2}: ", counter_dataframe.loc["DeathEff+L2", key])
        print(f"Number of cases with death effect and final exhaustion of {limNut1} and {limNut2}: ", counter_dataframe.loc["DeathEff+L12", key])
        print(f"Number of cases with death effect and final exhaustion of {carbon_source}: ", counter_dataframe.loc["DeathEff+CS", key])
        print("----------------------------------------------------------------\n")
    print()
    
# FALTARÍAN FUNCIONES
# PARA OTROS NUTRIENTES / CONTEOS QUE SE DESEE EVALUAR (hacer función aparte)
# AÑADIR NÚMERO DE CONFIGURACIONES TOTALES y porcentajes






















