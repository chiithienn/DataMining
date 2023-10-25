import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import mplcursors
from Run_FOSHU_SPMF import *

class Visualize_Results:
    def __init__(self):
        self.df1 = pd.read_csv('TrucQuanKQ1.csv')

    def generate_custom_colors(self, num_colors, get_cmap):
        cmap = get_cmap  # You can choose from 'tab10', 'tab20', 'tab20b', 'tab20c'
        return [cmap(i) for i in np.linspace(0, 1, num_colors)]

    def bar_chart(self):
        df_bar = pd.read_csv('TrucQuanKQ_Improve.csv')
        df_bar['Utility ($)'] = df_bar['Utility ($)'].astype(int)
        df_bar['Relative Utility'] = df_bar['Relative Utility'].astype(float)

        itemsets = df_bar['ProductName']
        utility = df_bar['Utility ($)']
        relative_utility = df_bar['Relative Utility']

        x = np.arange(len(itemsets))
        width = 0.35

        fig, ax1 = plt.subplots()

        custom_colors_ax1 = self.generate_custom_colors(len(itemsets), plt.get_cmap('tab10'))

        ax1.set_ylabel('Utility ($)', color='tab:blue')
        ax1.bar(x, utility, width, color=custom_colors_ax1, label=itemsets, edgecolor="black")
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))

        ax2 = ax1.twinx()
        ax2.plot(x, relative_utility, color='black', marker='o', label='Relative Utility')
        ax2.set_ylabel('Relative Utility', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        ax1.set_title('Utility and Relative Utility Comparison', fontweight='bold', pad=30, fontsize=20)
        ax1.grid(True, linestyle='--', alpha=0.7)

        ax1.set_facecolor('#f4f4f4')  # Thay đổi màu nền
        ax1.set_xticks([])
        ax1.set_xticklabels([])

        legend = ax1.legend(loc="upper left", bbox_to_anchor=(1.2, 0.95))
        legend.set_title('Product sets')
        legend.get_title().set_fontweight('bold')

        mplcursors.cursor(hover=True)

        plt.tight_layout()
        plt.show()

    def pie_chart(self):
        df_pie = self.df1.copy()
        df_pie_ = df_pie.groupby('Season')['Count'].sum().reset_index()
        colors=['#FFD700','#98FB98','#FF6347','#AEEEEE']

        print(df_pie_)
        fig, ax = plt.subplots()

        wedges, texts, autotexts = ax.pie(df_pie_['Count'], colors=colors,
                autopct='%1.1f%%', startangle=140, explode=(0.05, 0, 0, 0.05), shadow=True, wedgeprops={'edgecolor': 'black'})
        ax.set_title('Percent Frequency Of Itemsets Across Seasons', fontweight='bold', pad=10, fontsize=20)
        plt.setp(autotexts, size=10, weight="bold")
        plt.legend(wedges, df_pie_['Season'], title='Season')
        ax.axis('equal')

        plt.show()

    def plot_chart(self):
        df = self.df1

        fig, ax1 = plt.subplots()

        for itemset in df['Itemsets'].unique():
            itemset_data = df[df['Itemsets'] == itemset]
            ax1.plot(itemset_data['Season'], itemset_data['Total Profit'], label=itemset, marker='o')

        ax1.set_xlabel('Season', fontweight='bold')
        ax1.set_ylabel('Total Profit', fontweight='bold')
        ax1.set_title('Profit Of Itemsets Across Seasons', fontweight='bold', pad=20, fontsize=15)
        ax1.legend()
        ax1.grid(True)
        ax1.format_coord = lambda x, y: f"x={df['Season'].iloc[int(x)]}, y={int(y)}"

        mplcursors.cursor(hover=True)
        plt.show()

        fig, ax2 = plt.subplots()

        for itemset in df['Itemsets'].unique():
            itemset_data = df[df['Itemsets'] == itemset]
            ax2.plot(itemset_data['Season'], itemset_data['Count'], label=itemset, marker='*')

        ax2.set_xlabel('Season', fontweight='bold')
        ax2.set_ylabel('Count', fontweight='bold')
        ax2.set_title('Frequency Of Itemsets Across Seasons', fontweight='bold', pad=20, fontsize=15)
        ax2.legend()
        ax2.grid(True)
        ax2.format_coord = lambda x, y: f"x={df['Season'].iloc[int(x)]}, y={int(y)}"

        mplcursors.cursor(hover=True)
        plt.show()

    def heatmap_chart(self):
        df = self.df1
        pivot_table = df.pivot_table(values=['Total Profit', 'Count'], index='Itemsets', columns='Season')

        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot_table['Total Profit'], annot=True, cmap='Blues', fmt='.0f')
        plt.title('Correlation Between Seasonality And Profitability Of Itemsets', fontweight='bold', pad=20, fontsize=15)
        plt.show()

        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot_table['Count'], annot=True, cmap='YlOrRd', fmt='.0f')
        plt.title('Correlation Between Seasonality And Frequency Of Itemsets', fontweight='bold', pad=20, fontsize=15)

        plt.show()

if __name__ == '__main__':
    C_call = Visualize_Results()
    # C_call.pie_chart()
    # C_call.plot_chart()
    # C_call.heatmap_chart()
    C_call.bar_chart()