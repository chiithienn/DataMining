import pandas as pd
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

pd.set_option('display.max_columns', None)

# IMPORT DATASET
df1 = pd.read_csv(r"Dataset1.csv")

# Checking Null and NA value
print("Null values: ",df1.isnull().values.sum())
print("NA values: ",df1.isna().values.any())
print(df1.info())

# Convert Date field into datetime format
df_eda = df1.copy()
df_eda.drop('Name', axis=1, inplace=True)
df_eda['ModifiedDate'] = pd.to_datetime(df_eda.ModifiedDate)
print(df_eda.info())

# BAR CHART COMPARE THE NUMBER OF NULL VALUES
null_count = df_eda['ProductCost'].isna().sum()
valid_value_count = df_eda['ProductCost'].count()

values_bar = [null_count, valid_value_count, len(df_eda)]
labels_bar = ['ProductCost is Null', 'ProductCost has value', 'Total ProductCost']
color_bar = ['#FF6969', '#82CD47', '#22668D']

sizes_pie = [null_count, valid_value_count]
labels_pie = ['Null', 'Not Null']
color_pie = ['#FF6969', '#82CD47']

def compare_null_chart():
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 6))
    ax1.bar(labels_bar, values_bar, label=['null', 'not null', 'total'], color=color_bar, edgecolor="black")
    ax1.set_title('COMPARE THE NUMBER OF NULL VALUES', fontweight='bold')
    ax1.legend(title='')
    for i, v in enumerate(values_bar):
        ax1.text(i, v + 0.1, str(v), ha='center', va='bottom')

    ax2.pie(sizes_pie, labels=labels_pie, colors=color_pie,
            autopct='%1.1f%%', startangle=80, explode=(0.05, 0), shadow=True, wedgeprops={'edgecolor': 'black'})
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax2.set_title('PERCENTAGE OF NULL VALUES', fontweight='bold')
    ax2.legend(title='')

    plt.show()

compare_null_chart()