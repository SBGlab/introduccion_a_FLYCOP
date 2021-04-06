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
        
        - limitingNutrient_deathEffect()
        - 
    
    
    (See each particular function for detailed description)
    
NOTE THAT:
    
    xxx
        (CHANGE keyword)
    
"""

# -----------------------------------------------------------------------------
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
        pca = row[4]
        nh4 = row[8]
        pi = row[9]
        
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