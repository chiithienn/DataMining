import pandas as pd
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

pd.set_option('display.max_columns', None)

# IMPORT DATASET
df2 = pd.read_csv(r"Dataset2.csv")

# Checking Null and NA value
print("Null values: ",df2.isnull().values.sum())
print("NA values: ",df2.isna().values.any())
print(df2.info())