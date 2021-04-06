#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 09:46:05 2021

@author: ivan
"""

"""
DESCRIPTION

    Series of tracking functions to consider the evolution of biomass or certain metabolites
        during the FLYCOP run.
        
    (See detailed description in each tracking function)


NOTE THAT:
    
    xxx
"""

import pandas as pd


# -----------------------------------------------------------------------------
# FUNCTION TO: track when biomass loss starts during the simulation
# Registers the cycle at which the effect starts (supposedly, when one essential nutrient is finally depleted)
# Death effect is consider to start when biomass loss (of one or more microbes) is prolonged for more than 'n_cycles' consecutive cycles

# INPUT: 
    # COMETS FILE (file where biomass and other metabolites' evolution during the simulation are registered) (csv)
    # endCycle: final cycle in the simulation (integer)
    # n_cycles: number of consecutive cycles that biomass loss is required to last, for the death effect to exist (integer)
        
# OUTPUT: same dataframe with new columns:
    # 'biomass_track': 1 if death effect is registered, 0 otherwise (integer)
    # 'dead_cycles': period for death effect if registered, "NoDeadTracking" otherwise (string)

# NOTE THAT: function 'when_death_starts' is dependent on the performance of the current function
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
# FUNCTION TO: obtain the initial cycle for death effect, from the dataframe where it has previously registered

# INPUT: dataframe where to operate (pandas dataframe)
# OUTPUT: same dataframe with new column:
    # 'DT_cycles_init': cycle when dead effect starts

# NOTE THAT: "NoDeadTracking" means there is no death effect, thus the value for 'DT_cycles_init' is 0.
# If the mean for the death effect (initial cycle) was computed, all configurations would be taken into 
    # account (in the denominator) and those with no biomass loss would "sum 0" (to the numerator)
    
# PENDIENTE: further implementation / reorganization of code lines
# -----------------------------------------------------------------------------

def when_death_starts(dataframe):
    dataframe["DT_cycles_init"] = 0
    for row in dataframe.itertuples():
        DT_cycles = dataframe.loc[row[0], "DT_cycles"].split("-")
        DT_cycles_init = DT_cycles[0]
        
        if DT_cycles_init != "NoDeadTracking":
            dataframe.loc[row[0], "DT_cycles_init"] = int(DT_cycles_init)
            
    return dataframe
# -----------------------------------------------------------------------------




# PENDIENTE ADAPTACIÓN / REVISIÓN DE ESTA ÚLTIMA FUNCIÓN
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




























