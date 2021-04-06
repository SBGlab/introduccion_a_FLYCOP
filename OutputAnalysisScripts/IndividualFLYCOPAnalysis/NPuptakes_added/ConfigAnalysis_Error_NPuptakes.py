#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Feb 16 09:03:08 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Script for output analysis which counts the number of cases with ERRORs, as reported in FLYCOP_config_V0_log.txt:
    Type of ERROR this script is suited for: 
        - ZeroDivisionError, exhaustion of one of the microbes in the media
        - NonOptimalConfig_Error: "model solution was not optimal", infeasible model because of different reasons (...)
        
        
    UTILITY IMPLEMENTED: extraction of those configurations with NonOptimalConfig_Error 
        (series of input parameters in a .txt script: "nonOptimalConfigs_asStrings.txt"
    
EXPECTED INPUT

    'FLYCOP_config_V0_log.txt'
        
OUTPUT

    - In screen: number of configurations for each of the FLYCOP (COBRA) errors
    - "nonOptimalConfigs_asStrings.txt": file with configurations raising a NonOptimalSolution error
    
    
NOTE THAT:
    
    Script suited for this type of configuration analysis: NonOptimalConfig_Error
        Format for config extraction ("nonOptimalConfigs_asStrings.txt"): -2.0,0.1,-14.0,0.1,-4.0,-10.0,-0.3,-0.75
    
"""


import re
import os.path
# import pandas as pd
path = "../../../Project3_EcPp2_LimNut_M9/NP_LimNutFinal_29Mar/NP3"  # CHANGE path
os.chdir(path)
ZeroDivisionError_count = 0  # Error count for ZeroDivisionError
nonOptimalSolution_count = 0  # Error count for "model solution was not optimal"

# -----------------------------------------------------------------------------
# Original Analysis of 'FLYCOP_config_V0_log.txt'
# This is the logFile after FLYCOP run
# -----------------------------------------------------------------------------

input_file = "FLYCOP_EcPp2_0_log.txt"  # CHANGE input_file
output1 = open("nonOptimalError_configurations.txt", "w")

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
            if re.findall("The following algorithm call failed", line.strip("\n")):
                extract = re.findall("-p1_sucr1 '[-]*[0.]*[\d]+' -p2_biomassEc '[-]*[0.]*[\d]+' -p3_frc2 '[-]*[0.]*[\d]+' -p4_biomassKT '[-]*[0.]*[\d]+' -p5_nh4_Ec '[-]*[0.]*[\d]+' -p6_nh4_KT '[-]*[0.]*[\d]+' -p7_pi_Ec '[-]*[0.]*[\d]+' -p8_pi_KT '[-]*[0.]*[\d]+'", line)  # ADAPT line_code
                output1.write(str(extract[0])+"\n")
            last_error = ""


output1.close()                
print("Number of ZeroDivisionError configurations found: ", ZeroDivisionError_count)
print("Number of nonOptimalSolution configurations found: ", nonOptimalSolution_count)
print("Total of ERROR configurations found: ", ZeroDivisionError_count + nonOptimalSolution_count)
print()



# -----------------------------------------------------------------------------

output2 = open("nonOptimalConfigs_asStrings.txt", "w")

with open("nonOptimalError_configurations.txt", "r") as file:  
    lines = file.readlines()
    for line in lines:
        config = ""
        params = re.findall("'[-]*[0.]*[\d]+'", line)

        for parameter in params:
            if re.findall("'[-]*[0.]*[\d]+'", parameter):
                parameter = float(parameter.replace("\'", ""))
            
            config += ","+str(parameter) if config else str(parameter)
        
        output2.write(config+"\n")


output2.close()
os.remove("nonOptimalError_configurations.txt")
































