#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun Dec 27 23:02:18 2020

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Statistical analysis for the data obtained from "AcceptedRatios_SDlt.py" script
    
EXPECTED INPUT

    'dataTable_AcceptedRatios_SDlt.xlxs' from "AcceptedRatios_SDlt.py" script
        
OUTPUT

    Statistical description (on screen) of next variables: 
        fitFunc, ratio 'sucr1_frc2', ratio 'Ecbiomass_KTbiomass'
    
NOTE THAT:
    
    The variables to be displayed and the fitness ranks to be analyzed can be adapted if desired
    
"""


# import re
import pandas as pd
import os.path
path = "../Project4_EcPp2_M9adjusted/100SMAC10"   # Change to the desired path
os.chdir(path)


# -----------------------------------------------------------------------------
# STATISTICAL ANALYSIS
# -----------------------------------------------------------------------------
# INPUT: dataTable_AcceptedRatios_SDlt.xlsx, sorted descending by 'fitFunc'
dataTable = pd.read_excel("dataTable_AcceptedRatios_SDlt.xlsx", sheet_name="Uptake_initBiomass_r", engine="openpyxl")


# print("First rank analyzed")
# print("==============================")
# # rank1 = dataTable[dataTable["fitFunc"] < 100]
# rank11 = dataTable[dataTable["fitFunc"] > 75]
# rank11_descr = rank11[["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"]].describe()
# print(rank11_descr)
# print()

# mean11_uptR = rank11["sucr1_frc2"].mean()
# sd11_uptR = rank11["sucr1_frc2"].std()
# mean11_bR = rank11["Ecbiomass_KTbiomass"].mean()
# sd11_bR = rank11["Ecbiomass_KTbiomass"].std()



# print("Second rank analyzed")
# print("==============================")
# rank2 = dataTable[dataTable["fitFunc"] < 75]
# rank22 = rank2[rank2["fitFunc"] > 50]
# rank22_descr = rank22[["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"]].describe()
# print(rank22_descr)
# print()

# mean22_uptR = rank22["sucr1_frc2"].mean()
# sd22_uptR = rank22["sucr1_frc2"].std()
# mean22_bR = rank22["Ecbiomass_KTbiomass"].mean()
# sd22_bR = rank22["Ecbiomass_KTbiomass"].std()



# print("Third rank analyzed")
# print("==============================")
# rank3 = dataTable[dataTable["fitFunc"] < 50]
# rank33 = rank3[rank3["fitFunc"] > 20]
# rank33_descr = rank33[["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"]].describe()
# print(rank33_descr)
# print()

# mean33_uptR = rank33["sucr1_frc2"].mean()
# sd33_uptR = rank33["sucr1_frc2"].std()
# mean33_bR = rank33["Ecbiomass_KTbiomass"].mean()
# sd33_bR = rank33["Ecbiomass_KTbiomass"].std()



# print("Fourth rank analyzed")
# print("==============================")
# rank44 = dataTable[dataTable["fitFunc"] < 20]
# # rank44 = rank4[rank4["fitFunc"] > 5]
# rank44_descr = rank44[["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"]].describe()
# print(rank44_descr)
# print()

# mean44_uptR = rank44["sucr1_frc2"].mean()
# sd44_uptR = rank44["sucr1_frc2"].std()
# mean44_bR = rank44["Ecbiomass_KTbiomass"].mean()
# sd44_bR = rank44["Ecbiomass_KTbiomass"].std()


print("First rank analyzed")
print("==============================")
# rank1 = dataTable[dataTable["fitFunc"] < 100]
rank11 = dataTable[dataTable["fitFunc"] > 99]
rank11_descr = rank11[["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"]].describe()
print(rank11_descr)
print()

print("Second rank analyzed")
print("==============================")
rank2 = dataTable[dataTable["fitFunc"] < 99]
rank22 = rank2[rank2["fitFunc"] > 90]
rank22_descr = rank22[["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"]].describe()
print(rank22_descr)
print()

print("Second rank analyzed")
print("==============================")
rank22 = dataTable[dataTable["fitFunc"] < 90]
rank22_descr = rank22[["fitFunc", "sucr1_frc2", "Ecbiomass_KTbiomass"]].describe()
print(rank22_descr)
print()





























