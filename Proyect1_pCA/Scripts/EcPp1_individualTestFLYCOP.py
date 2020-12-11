#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez
# April 2018
################################

# Running an individual test, for a particular consortium configuration given by arguments
# cp -p -R EcPp1_TemplateOptimizeConsortiumV0 EcPp1_scenario0_optimalConfiguration
# cd EcPp1_scenario0_optimalConfiguration
# python3 ../../Scripts/EcPp1_individualTestFLYCOP.py assoc_args

import sys
import importlib
sys.path.append('../../Scripts')
import EcPp1

# assoc_args
print(sys.argv)
sucr1 = float(sys.argv[1])  # cannot convert string to float ERROR
Ecbiomass = float(sys.argv[2])
frc2 = float(sys.argv[3])
KTbiomass = float(sys.argv[4])
fitness = sys.argv[5]

avgfitness,sdfitness=EcPp1.EcoliPputidaFLYCOP_oneConf(sucr1, Ecbiomass, frc2, KTbiomass, fitness, 500, './IndividualRunsResults/', 3)
