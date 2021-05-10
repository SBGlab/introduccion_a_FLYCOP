#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez, Iván Martín Martín
# April 2018, April 2021
################################

"""
EcPp3 - Glycosilation project. Wrapper file using functions:

        - EcoliPputidaFLYCOP_selectConsortiumArchitecture(sucr1, Ecbiomass, Ecbiomass_glyc, frc2, KTbiomass, nh4_Ec, nh4_KT, consortium_arch, ...)

"""

src='EcPp3_TemplateOptimizeConsortiumV0/'  # DIR EcPp3_TemplateOptimizeConsortiumV0
dst='EcPp3_TestTempV0'  # nuevo dir, carpeta temporal
dirPlots='../smac-output/EcPp3_PlotsScenario0/'  # salir de EcPp3_TemplateOptimizeConsortiumV0, entrar en smac-output/EcPp3_PlotsScenario0  --> más tarde se traslada a EcPp3_scenario0_FLYCOPdataAnalysis

fitFunc = "MaxNaringenin"
maxCycles = 240  #  See layout_template
repeats = 5

# import cobra
import sys
import shutil, errno
import os.path
# import pandas as pd
# import tabulate
# import re
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

# Load code of individual run
sys.path.append('../Scripts')
import EcPp3

# Parsing parameters:
# Reading the first 5 arguments in SMAC
instance = sys.argv[1]
specifics = sys.argv[2]
cutoff = int(float(sys.argv[3]) + 1)
runlength = int(sys.argv[4])
seed = int(sys.argv[5])


# Reading this case study parameters to optimize by SMAC
sucr1 = float(sys.argv[7])
Ecbiomass = float(sys.argv[9])
Ecbiomass_glyc = float(sys.argv[11])  # Not used in case of consortium architecture based on two models
frc2 = float(sys.argv[13])
KTbiomass = float(sys.argv[15])

# N uptake rates
nh4_Ec = float(sys.argv[17])
nh4_KT = float(sys.argv[19])
consortium_arch = sys.argv[21]
cutoff_SD = float(sys.argv[23])


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
# -----------------------------------------------------------------------------
avgfitness,sdfitness=EcPp3.EcoliPputidaFLYCOP_selectConsortiumArchitecture(sucr1, Ecbiomass, Ecbiomass_glyc, frc2, KTbiomass, nh4_Ec, nh4_KT, consortium_arch, \
                                                                           fitFunc, maxCycles, dirPlots, repeats, cutoff_SD)  


# Print wrapper Output:
# -----------------------------------------------------------------------------
print('Result of algorithm run: SAT, 0, 0, '+str(1-avgfitness)+', 0, '+str(seed)+', '+str(sdfitness)) # fitness maximize
# print('Result of algorithm run: SAT, 0, 0, '+str(avgfitness)+', 0, '+str(seed)+', '+str(sdfitness)) # fitness minimize

# Remove the temporal dir for this run result
os.chdir('..')
shutil.rmtree(dst)























