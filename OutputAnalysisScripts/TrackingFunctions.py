#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 09:46:05 2021

@author: ivan
"""

"""
PENDIENTE FULL DESCRIPTION
"""

import pandas as pd


# -----------------------------------------------------------------------------
# Cycle at which death effect starts (it is suppossed to be the cycle when NH4 is finally depleted)
# LIMITATION: cannot consider in the final count those configurations with "NoDeadTracking".
# Actually, it is consider in the denominator, since the associated value in this case is 0. Perfect!
# -----------------------------------------------------------------------------
# NOTE THAT names for colums of interest should be: 'DT_cycles_init', 'DT_cycles'

def when_death_starts(dataframe):
    dataframe["DT_cycles_init"] = 0
    for row in dataframe.itertuples():
        DT_cycles = dataframe.loc[row[0], "DT_cycles"].split("-")
        DT_cycles_init = DT_cycles[0]
        
        if DT_cycles_init != "NoDeadTracking":
            dataframe.loc[row[0], "DT_cycles_init"] = int(DT_cycles_init)
            
    return dataframe
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# FUNCTION dead_biomass_tracking  
# Dead Tracking within the community simulation: 
# if biomass of any strain (or both strains) decreases during more than 'n_cycles' consecutive cycles
# -----------------------------------------------------------------------------
def dead_biomass_tracking(COMETS_file, endCycle, n_cycles = 10):
    CometsTable = pd.read_csv(COMETS_file, sep="\t", header=None)
    # print(CometsTable)
    biomass_track = 0
    count_cons_cycles = 0
    
    # The endcycle can occur when the substrate (sucrose) is finally exhausted, which might not always happen in the last cycle
    # cycles_number = len(CometsTable) - 1 # Lenght: 241 (initial row + 240 cycles)    
    
    for row in CometsTable.itertuples():  # Note tuple 241 = cycle 240; tuple 0 = initial situation
        cycle = row[1]
        
        if cycle == 0:
            last_biomass1 = row[2]
            last_biomass2 = row[3]
            
        else:
            biomass1 = row[2]
            biomass2 = row[3]
                
            if ((biomass1 - last_biomass1) < 0) or ((biomass2 - last_biomass2) < 0):
                count_cons_cycles += 1
                last_dead = cycle
                
            else:
                count_cons_cycles = 0
                
            last_biomass1 = row[2]
            last_biomass2 = row[3]
                
        if count_cons_cycles > 10:
            biomass_track = 1
                
    if biomass_track:
        dead_cycles = str(last_dead - count_cons_cycles)+"-"+str(last_dead)     
        return biomass_track, dead_cycles
            
    else:
        return biomass_track, "NoDeadTracking"
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Function to track Pi overconsumption
    # Moderate Pi consumtion gives final levels around 60 or 50 mM (at most, 20 mM Pi consumption): x < [0.1 mM Pi consumed / cycle]
    # Full consumption of ~ 70 mM in 240 cycles would be ~ 0.30 mM consumed / cycle
    
# In usual cases of Pi overconsumption, full Pi consumption (60 to 70 mM) happens in 100 cycles or less (50, 25 cycles)
    # 60 mM / 100 cycles = 0.6 mM / cycle
    # 60 mM / 50 cycles = 1.2 mM / cycle
    # 60 mM / 25 cycles = 2.4 mM / cycle
    
# However, real examples of Pi overconsumption can reach 5.0 to 10.0 mM / cycle, as evaluated experimentally (in computational examples)

# -----------------------------------------------------------------------------
# row_pos_df: position of the metabolite to be tracked in the original dataframe (column_number)
def metabolite_tracking_overconsumption(COMETS_file, excessive_consumpt_rate, row_pos_df):
    CometsTable = pd.read_csv(COMETS_file, sep="\t", header=None)
    # print(CometsTable)
    met_overconsumption = 0
    
    initial_overconsumption_cycle = 0
    num_overconsumption_cycles = 0
    
    # cycles_number = len(CometsTable) - 1 # Lenght: 241 (initial row + 240 cycles)    
    
    for row in CometsTable.itertuples():  # Note tuple 241 = cycle 240; tuple 0 = initial situation
        cycle = row[1]
        
        if cycle == 0:
            last_met_conc = row[row_pos_df]
            
        else:
            met_conc = row[row_pos_df]
            
            if (last_met_conc - met_conc) > excessive_consumpt_rate and (met_overconsumption == 0):
                met_overconsumption = 1
                initial_overconsumption_cycle = cycle
                num_overconsumption_cycles += 1
                last_met_conc = met_conc
                
            elif (last_met_conc - met_conc) > excessive_consumpt_rate:   
                num_overconsumption_cycles += 1
                last_met_conc = met_conc
                
                # Note that if this condition is not met anymore because of low metabolite values, that does not necessarily mean that [metabolite] is already
                # 0 mM. This concentration value can be in low levels, without no further overconsumption.
                
            else:
                continue
            
            
    if met_overconsumption:
        met_cycles = str(initial_overconsumption_cycle)+"-"+str(initial_overconsumption_cycle + num_overconsumption_cycles)
        return met_overconsumption, met_cycles
            
    else:
        return met_overconsumption, "NoMetOverconsumption"
# -----------------------------------------------------------------------------
# TRIAL
# pi_case, pi_cycles = metabolite_tracking_overconsumption("Trials/biomass_vs_sucr_T4hcinnm_fru_nar_nh4_pi_template2.txt", 10, 9)
# print(pi_case)
# print(pi_cycles)
# -----------------------------------------------------------------------------




























