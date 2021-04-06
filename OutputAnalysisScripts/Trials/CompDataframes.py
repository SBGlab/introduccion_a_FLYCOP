#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 11:58:38 2021

@author: ivan
"""

import pandas as pd

A = pd.DataFrame([["Luis", 1, "A"], ["Juan", 2, "A"]], columns=["Name", "ID", "Team"])
B = pd.DataFrame([["Sofía", 10, "B"], ["María", 11, "B"]], columns=["Name", "ID", "Team"])
C = pd.DataFrame([["Alex", 20, "C"], ["Mario", 21, "C"]], columns=["Name", "ID", "Team"])
D = pd.DataFrame([["Lucía", 30, "D"], ["Ana", 31, "D"]], columns=["Name", "ID", "Team"])


complete_df = pd.concat([A, B, C, D], ignore_index = True)
# print(complete_df)

print(list(complete_df))
print(complete_df)





























