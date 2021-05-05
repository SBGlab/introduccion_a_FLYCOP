#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 23:57:02 2021

@author: ivan
"""

import pandas as pd

def dead_biomass_tracking2(COMETS_file, endCycle, n_cycles = 10, biomass_indexes = []):
    CometsTable = pd.read_csv(COMETS_file, sep="\t", header=None)
    biomass_track = 0
    count_cons_cycles = 0
    initial_dead = 0
    
    # The endcycle can occur when the substrate (sucrose) is finally exhausted, which might not always happen in the last cycle
    # cycles_number = len(CometsTable) - 1 # Lenght: 241 (initial row + 240 cycles)    
    
    for row in CometsTable.itertuples():  # Note tuple 241 = cycle 240; tuple 0 = initial situation
        cycle = row[0]
        
        if cycle == 0:
            last_biomass1 = row[biomass_indexes[0]]
            last_biomass2 = row[biomass_indexes[1]]
            
        elif cycle != 0:
            biomass1 = row[biomass_indexes[0]]
            biomass2 = row[biomass_indexes[1]]
                
            if ((biomass1 - last_biomass1) < 0) or ((biomass2 - last_biomass2) < 0):  # cannot distinguish between the microbe experiencing biomass loss
                count_cons_cycles += 1                                                # might be just one or both
                last_dead = cycle
                
            else:
                count_cons_cycles = 0
                
            last_biomass1 = row[biomass_indexes[0]]
            last_biomass2 = row[biomass_indexes[1]]
                
        if count_cons_cycles > 10 and not biomass_track:
            biomass_track = 1
            initial_dead = last_dead - count_cons_cycles
            
                
    if biomass_track:
        dead_cycles = str(initial_dead)+"-"+str(last_dead)     
        return biomass_track, dead_cycles
            
    else:
        return biomass_track, "NoDeadTracking"
    
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
    
def dead_biomass_tracking3(COMETS_file, endCycle, n_cycles = 10, biomass_indexes = []):
    CometsTable = pd.read_csv(COMETS_file, sep="\t", header=None)
    biomass_track = 0
    count_cons_cycles = 0
    initial_dead = 0
    
    # The endcycle can occur when the substrate (sucrose) is finally exhausted, which might not always happen in the last cycle
    # cycles_number = len(CometsTable) - 1 # Lenght: 241 (initial row + 240 cycles)    
    
    for row in CometsTable.itertuples():  # Note tuple 241 = cycle 240; tuple 0 = initial situation
        cycle = row[0]
        
        if cycle == 0:
            last_biomass1 = row[biomass_indexes[0]]
            last_biomass2 = row[biomass_indexes[1]]
            last_biomass3 = row[biomass_indexes[2]]
            
        elif cycle != 0:
            biomass1 = row[biomass_indexes[0]]
            biomass2 = row[biomass_indexes[1]]
            biomass3 = row[biomass_indexes[2]]
                
            if ((biomass1 - last_biomass1) < 0) or ((biomass2 - last_biomass2) < 0) or ((biomass3 - last_biomass3) < 0):  
                count_cons_cycles += 1  # cannot distinguish between the microbe experiencing biomass loss                                
                last_dead = cycle  # might be just one or both
                
            else:
                count_cons_cycles = 0
                
            last_biomass1 = row[biomass_indexes[0]]
            last_biomass2 = row[biomass_indexes[1]]
            last_biomass3 = row[biomass_indexes[2]]
                
        if count_cons_cycles > 10 and not biomass_track:
            biomass_track = 1
            initial_dead = last_dead - count_cons_cycles
            
                
    if biomass_track:
        dead_cycles = str(initial_dead)+"-"+str(last_dead)     
        return biomass_track, dead_cycles
            
    else:
        return biomass_track, "NoDeadTracking"
    