#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:02:18 2020

@author: Iván Martín Martín
"""

"""
DESCRIPTION

    Statistical analysis for the data obtained from "Extract_configResults_base.py" script
    
EXPECTED INPUT

    'configurationsResults_Scenario0_analysis.xlsx' from "Extract_configResults_base.py" script
        
OUTPUT

    Statistical description (on screen) of next variables: fitness, Naringenin final concentration, 
        p-Coumarate final concentration, final E. coli biomass, final P. putida KT biomass
    
NOTE THAT:
    
    The variables to be displayed and the fitness ranks to be analyzed can be adapted if desired
    
"""

# import re
import pandas as pd
import os.path
path = "../Project4_EcPp2_M9adjusted/100SMAC10"
os.chdir(path)

# -----------------------------------------------------------------------------
# STATISTICAL ANALYSIS
# -----------------------------------------------------------------------------
# INPUT: 'configurationsResults_Scenario0_analysis.txt', sorted descending by 'fitness'
dataTable = pd.read_excel("configurationsResults_Scenario0_analysis.xlsx", sheet_name="Product_ratios", engine="openpyxl")


# print("First rank analyzed")
# print("==============================")
# rank1 = dataTable[dataTable["fitness"] < 20]
# rank11 = rank1[rank1["fitness"] > 15]
# rank11_descr = rank11[["fitness", "Nar(mM)", "pCA(mM)"]].describe()
# print(rank11_descr)
# print()

# mean11_uptP = rank11["Nar(mM)"].mean()
# median11_uptP = rank11["Nar(mM)"].median()
# sd11_uptP = rank11["Nar(mM)"].std()



# print("Second rank analyzed")
# print("==============================")
# rank2 = dataTable[dataTable["fitness"] < 15]
# rank22 = rank2[rank2["fitness"] > 10]
# rank22_descr = rank22[["fitness", "Nar(mM)", "pCA(mM)"]].describe()
# print(rank22_descr)
# print()

# mean22_uptP = rank22["Nar(mM)"].mean()
# median22_uptP = rank22["Nar(mM)"].median()
# sd22_uptP = rank22["Nar(mM)"].std()



# print("Third rank analyzed")
# print("==============================")
# rank3 = dataTable[dataTable["fitness"] < 10]
# rank33 = rank3[rank3["fitness"] > 5]
# rank33_descr = rank33[["fitness", "Nar(mM)", "pCA(mM)"]].describe()
# print(rank33_descr)
# print()

# mean33_uptP = rank33["Nar(mM)"].mean()
# median33_uptP = rank33["Nar(mM)"].median()
# sd33_uptP = rank33["Nar(mM)"].std()



# print("Fourth rank analyzed")
# print("==============================")
# rank44 = dataTable[dataTable["fitness"] < 5]
# # rank44 = rank4[rank4["fitness"] > 5]
# rank44_descr = rank44[["fitness", "Nar(mM)", "pCA(mM)"]].describe()
# print(rank44_descr)
# print()

# mean44_uptP = rank44["Nar(mM)"].mean()
# median44_uptP = rank44["Nar(mM)"].median()
# sd44_uptP = rank44["Nar(mM)"].std()


print("First rank analyzed")
print("==============================")
# rank1 = dataTable[dataTable["fitFunc"] < 100]
rank11 = dataTable[dataTable["fitness"] > 99]
rank11_descr = rank11[["fitness", "Nar_mM", "pCA_mM", "FinalEc_gL", "FinalKT_gL"]].describe()
print(rank11_descr)
print()

print("Second rank analyzed")
print("==============================")
rank2 = dataTable[dataTable["fitness"] < 99]
rank22 = rank2[rank2["fitness"] > 90]
rank22_descr = rank22[["fitness", "Nar_mM", "pCA_mM", "FinalEc_gL", "FinalKT_gL"]].describe()
print(rank22_descr)
print()

print("Second rank analyzed")
print("==============================")
rank22 = dataTable[dataTable["fitness"] < 90]
rank22_descr = rank22[["fitness", "Nar_mM", "pCA_mM", "FinalEc_gL", "FinalKT_gL"]].describe()
print(rank22_descr)
print()








