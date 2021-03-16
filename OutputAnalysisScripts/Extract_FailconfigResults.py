#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Feb 16 09:03:08 2021

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Script for output analysis which extracts the ERRORs selected from FLYCOP_config_V0_log.txt:
        For now:
            - ZeroDivisionError: exhaustion of one of the microbes in the media (E. coli)
                * Final P.putida KT biomass:
                * Final Naringenin concentration
        
EXPECTED INPUT

    'FLYCOP_config_V0_log.txt'
        
OUTPUT

    "FailConfigResults_analysis.txt"
    
NOTE THAT:
    
        This script is highly specific: depending on the potential "errors" you have in 
        your current configuration, the code below might have to be adapted.
"""

import re
import os.path
import pandas as pd
path = "../Project3_EcPp2_LimNut_M9/Nitrogen/M9200N_nonSucr_nP"  # POTENTIAL CHANGE
os.chdir(path)
count = 0

# -----------------------------------------------------------------------------
# Original Analysis of 'FLYCOP_config_V0_log.txt'
# -----------------------------------------------------------------------------

output = open("FailConfigResults_analysis.txt", "w")
with open("FLYCOP_EcPp2_0_log.txt", "r") as file:  # POTENTIAL CHANGE
    lines = file.readlines()
    last_line = ""
    for line in lines:
        if re.match("\[WARN \] \[PROCESS-ERR\]", line):
            if re.findall("ZeroDivisionError: float division by zero", line.strip("\n")):
                output.write("\n\nNEW ERROR\n-----------------------------------------------------------\n")
                output.write(last_line)
                output.write(line+"\n")
                count += 1
                
            last_line = line
                
                
        if re.match("\[ERROR\]", line):   
            if re.findall("The following algorithm call failed", line.strip("\n")):
                extract = re.findall("-p1_sucr1 '-[\d]+' -p2_biomassEc '0.[\d]+' -p3_frc2 '-[\d]+' -p4_biomassKT '0.[\d]+'", line)  
                output.write("CONFIGURATION: "+str(extract[0])+"\n")
            else:
                output.write(line)
                
                
output.close()
if count == 0:
    os.remove("FailConfigResults_analysis.txt")
print("\nNumber of fail configurations found: ", count)


# -----------------------------------------------------------------------------
# Associated Storing File
# -----------------------------------------------------------------------------

no_lines = 0
output2 = open("FailConfigResults_dataTable.txt", "w")
output2.write("ERROR\tEx_Microbe\tConfig\tEc_finalB\tKT_finalB\tFinalNar")

# Column values
error = ""
microbe = ""
config = ""
nar_value = ""
Ec_value = ""
KT_value = ""

with open("FailConfigResults_analysis.txt", "r") as file:  
    # line_no = 1
    lines = file.readlines()
    for line in lines:
        
        if re.match("\[WARN \] \[PROCESS-ERR\]", line):
            if re.findall("E.coli", line.strip("\n")):  # Ajustar E.coli
                microbe = "E.coli"
            elif re.findall("P.putida KT", line.strip("\n")):
                microbe = "P.putida KT"
            
            if re.findall("ZeroDivisionError", line.strip("\n")):  # Pensado solo para este tipo de errores
                error = "ZeroDivisionError"
               
                
        if re.match("CONFIGURATION", line.strip("\n")):
                config_line = line.strip("\n")
                # no_lines += 1
            
                # Uptake rates + eliminación de dobles comillas ("''")
                conc = re.findall("'-*[\d]+'", config_line)
                conc2 = []
                for i in range(len(conc)):
                    match = re.findall("-*[\d]+", conc[i])
                    number = float(match[0])
                    conc2.append(number)
                
                # Biomass + eliminación de dobles comillas ("''")
                biomass = re.findall("'0.[\d]+'", config_line)  # Biomass < 1.0
                biomass2 = []
                for i in range(len(biomass)):
                    match = re.findall("0.[\d]+", biomass[i])
                    number = float(match[0])
                    biomass2.append(number)
                
                config = str(conc2[0])+","+str(biomass2[0])+","+str(conc2[1])+","+str(biomass2[1])
                # print(config)
                
        
        # Guardado exclusivo de los últimos valores, para estas tres variables, en cada sección 'NEW ERROR' de 'FailConfigResults_analysis.txt'
        # Nar, Ec_biomass, KT_biomass
        if re.match("\[ERROR\]", line):  
            
            if re.findall("Nar:", line.strip("\n")):
                nar_line = re.findall("Nar: [\d]+.[\d]+", line.strip("\n"))
                nar_value = re.findall("[\d]+.[\d]+", nar_line[0])  # Lista con 1 elemento
                nar_value = nar_value[0]
                # print(nar_value)

            if re.findall("Final Ec biomass:", line.strip("\n")):
                Ec_line = re.findall("Final Ec biomass:[\s]+[\d]+.[\d]+", line.strip("\n"))
                Ec_value = re.findall("[\d]+.[\d]+", Ec_line[0])  # Lista con 1 elemento
                Ec_value = Ec_value[0]
                # print(Ec_value)
        
            if re.findall("Final KT biomass:", line.strip("\n")):
                KT_line = re.findall("Final KT biomass:[\s]+[\d]+.[\d]+", line.strip("\n"))
                KT_value = re.findall("[\d]+.[\d]+", KT_line[0])  # Lista con 1 elemento
                KT_value = KT_value[0]
                # print(KT_value)
        
        if re.match("NEW ERROR", line):
            output2.write(error+"\t"+microbe+"\t"+config+"\t"+Ec_value+"\t"+KT_value+"\t"+nar_value+"\n")


# print(no_lines)
output2.write(error+"\t"+microbe+"\t"+config+"\t"+Ec_value+"\t"+KT_value+"\t"+nar_value+"\n")  # Final Recall
output2.close()













