import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

print("hello world")

drugList = pd.read_csv("drug200.csv")
print(drugList.head(5))


## Spliting into 5 groups
drugY = drugList.loc[drugList['Drug'] == "drugY"]
drugX = drugList.loc[drugList['Drug'] == "drugX"]
drugA = drugList.loc[drugList['Drug'] == "drugA"]
drugB = drugList.loc[drugList['Drug'] == "drugB"]
drugC = drugList.loc[drugList['Drug'] == "drugC"]

print(drugY)
print(drugX)
print(drugA)
print(drugB)
print(drugC)