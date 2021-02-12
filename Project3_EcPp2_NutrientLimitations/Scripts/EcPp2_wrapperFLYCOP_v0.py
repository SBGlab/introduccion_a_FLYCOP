#!/usr/bin/python3

# See SMAC documentation for more details about *wrapper_vX.py, wrapper_scenario_vX.txt and *wrapper_params_vX.pcs

print("\nInicializamos ejecucion wrapper\n")
src='EcPp2_TemplateOptimizeConsortiumV0/'  # DIR EcPp2_TemplateOptimizeConsortiumV0
dst='EcPp2_TestTempV0'  # nuevo dir, carpeta temporal
dirPlots='../smac-output/EcPp2_PlotsScenario0/'  # salir de EcPp2_TemplateOptimizeConsortiumV0, entrar en smac-output/EcPp2_PlotsScenario0  --> más tarde se traslada a EcPp2_scenario0_FLYCOPdataAnalysis

fitFunc = "MaxNaringenin"
maxCycles = 240  #  See layout_template
repeats = 5

import cobra
import pandas as pd
import tabulate
import re
import sys
import getopt
import os.path
import copy
import csv
import math
import cobra.flux_analysis.variability
import massedit
import subprocess
import shutil, errno
import statistics
import importlib
import optlang
# import spec

# Load code of individual run
sys.path.append('../Scripts')
import EcPp2_limNut

# -----------------------------------------------------------------------------
# ALGORITMO DE EJECUCIÓN DE WRAPPER INDIVIDUAL
# -----------------------------------------------------------------------------
# cd "/home/FLYCOP/MicrobialCommunities" ;  python3 -W ignore ../Scripts/EcPp2_wrapperFLYCOP_v0.py no_instance 0 1.7976931348623157E308 2147483647 -1 -p1_sucr1 '-20' -p2_biomassEc '0.175' -p3_frc2 '-4' -p4_biomassKT '0.2'
#                                           <algo> <instance> <instance specific> <cutoff time> <runlength> <seed> <algorithm parameters>
# -----------------------------------------------------------------------------
  
# Parsing parameters:
# Reading the first 5 arguments in SMAC
instance = sys.argv[1]
specifics = sys.argv[2]
cutoff = int(float(sys.argv[3]) + 1)
runlength = int(sys.argv[4])
seed = int(sys.argv[5])

# instance = "no_instance"
# specifics = 0
# cutoff = 
# runlength = 
# seed = 123 vs. -1 (¿?)

# Reading this case study parameters to optimize by SMAC
sucr1 = float(sys.argv[7])
Ecbiomass = float(sys.argv[9])
frc2 = float(sys.argv[11])
KTbiomass = float(sys.argv[13])

# sucr1 = -10
# Ecbiomass = 0.75
# frc2 = -6
# KTbiomass = 0.1

# Mantenemos como estaba
# Copy the template directory
if (os.path.exists(dst)):
    shutil.rmtree(dst)  # Eliminar contenido
try:
    shutil.copytree(src, dst)
except OSError as exc: # python >2.5
    if exc.errno == errno.ENOTDIR:
        shutil.copy(src, dst)
    else: raise
    
os.chdir(dst)

if not os.path.exists(dirPlots):
    os.makedirs(dirPlots)
    
# At a higher level: Running the wrapper-script in SMAC: 
avgfitness,sdfitness=EcPp2_limNut.EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, frc2, KTbiomass, fitFunc, maxCycles, dirPlots, repeats)

# Print wrapper Output:
print('Result of algorithm run: SAT, 0, 0, '+str(1-avgfitness)+', 0, '+str(seed)+', '+str(sdfitness)) # fitness maximize
#print('Result of algorithm run: SAT, 0, 0, '+str(avgfitness)+', 0, '+str(seed)+', '+str(sdfitness)) # fitness minimize

# Remove the temporal dir for this run result
os.chdir('..')
shutil.rmtree(dst)

print("\nTerminamos ejecucion wrapper\n")

