#!/usr/bin/python3

############ FLYCOP ############
# Author: Beatriz García-Jiménez, Iván Martín Martín
# April 2018, April 2021
################################

"""
EcPp3 - Glycosilation project. Wrapper file using functions:

        - EcoliPputidaFLYCOP_selectConsortiumArchitecture(sucr1, Ecbiomass, Ecbiomass_glyc, frc2, KTbiomass, nh4_Ec, nh4_KT, consortium_arch, ...)

"""

print("\nInitialize individualTest execution\n")

import sys
sys.path.append('../../Scripts')
# import os
import EcPp3

# assoc_args
# print(sys.argv)
# print(os.getcwd())

sucr1 = float(sys.argv[1])  # cannot convert string to float ERROR
Ecbiomass = float(sys.argv[2])
Ecbiomass_glyc = float(sys.argv[3])
frc2 = float(sys.argv[4])
KTbiomass = float(sys.argv[5])

nh4_Ec = float(sys.argv[6])
nh4_KT = float(sys.argv[7])
consortium_arch = sys.argv[8]
cutoff_SD = sys.argv[9]
fitness = sys.argv[10]

avgfitness,sdfitness = EcPp3.EcoliPputidaFLYCOP_selectConsortiumArchitecture(sucr1, Ecbiomass, Ecbiomass_glyc, frc2, KTbiomass, nh4_Ec, nh4_KT, consortium_arch, \
                                                        fitObj='MaxNaringenin', maxCycles = 240, dirPlot='', repeat=5, cutoff_SD = cutoff_SD)
EcPp3.final_model_summary(consortium_arch)
print("\nFinish individualTest execution\n")
