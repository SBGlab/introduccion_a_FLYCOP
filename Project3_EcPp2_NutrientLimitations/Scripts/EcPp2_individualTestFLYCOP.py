#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez
# April 2018
################################

# Running an individual test, for a particular consortium configuration given by arguments
# cp -p -R EcPp2_TemplateOptimizeConsortiumV0 EcPp2_scenario0_optimalConfiguration
# cd EcPp2_scenario0_optimalConfiguration
# python3 ../../Scripts/EcPp2_individualTestFLYCOP.py -10 0.75 -6 0.1 MaxNaringenin
print("\nInicializamos ejecucion individualTest\n")

import sys
import os
import importlib
sys.path.append('../../Scripts')
import EcPp2_limNut

# assoc_args
print(sys.argv)
print(os.getcwd())

sucr1 = float(sys.argv[1])  # cannot convert string to float ERROR
Ecbiomass = float(sys.argv[2])
frc2 = float(sys.argv[3])
KTbiomass = float(sys.argv[4])
fitness = sys.argv[5]

avgfitness,sdfitness=EcPp2_limNut.EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, frc2, KTbiomass, fitness, 240, './IndividualRunsResults/', 5)
print("\nTerminamos ejecucion individualTest\n")
