import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.ticker as mticker

pd.set_option('display.max_columns', None)

class EDA_3:
    def __init__(self):
        self.file_path = r"Dataset3.csv"
        self.df_eda = None

    def check_missing_value(self):
        df = pd.read_csv(self.file_path)
        print("Null values: ", df.isnull().values.sum())
        print("NA values: ", df.isna().values.any())
        print(df.info())

    def process_data(self):
        df = pd.read_csv(self.file_path)
        df_eda = df.copy()
        df_eda.drop('Name', axis=1, inplace=True)
        df_eda['ModifiedDate'] = pd.to_datetime(df_eda.ModifiedDate)
        print(df_eda.info())
        return df_eda

    def get_df_eda_processed(self):
        if self.df_eda is None:
            self.df_eda = self.process_data()
        return self.df_eda

    def split_by_year(self):
        self.get_df_eda_processed()
        year_dfs = {}
        for year in self.df_eda['ModifiedDate'].dt.year.unique():
            year_dfs[year] = self.df_eda[self.df_eda['ModifiedDate'].dt.year == year].copy()
        return year_dfs

    def time_period(self):
        print("Starting date: ", self.df_eda.iloc[0, -1])
        print("Ending date: ", self.df_eda.iloc[-1, -1])
        print("Duration: ", (self.df_eda.iloc[-1, -1]) - (self.df_eda.iloc[0, -1]))
        print("Actual Number of Date: " + str(self.df_eda['ModifiedDate'].nunique()))

    def describe_dataset(self):
        print(self.df_eda.describe())

    def frequency_columns(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(12, 6))

        ax1.hist(self.df_eda['SalesOrderID'], bins=20, color='skyblue', edgecolor='black')
        ax2.hist(self.df_eda['ProductID'], bins=20, color='gold', edgecolor='black')
        ax3.hist(self.df_eda['UnitPrice'], bins=20, color='lightgreen', edgecolor='black')
        ax4.hist(self.df_eda['ProductCost'], bins=20, color='lightcoral', edgecolor='black')

        ax1.set_title('SalesOrderID Distribution', fontweight='bold')
        ax2.set_title('ProductID Distribution', fontweight='bold')
        ax3.set_title('UnitPrice Distribution', fontweight='bold')
        ax4.set_title('ProductCost Distribution', fontweight='bold')

        mplcursors.cursor(hover=True)

        ax1.format_coord = lambda x, y: f"x={int(x)}, y={int(y)}"
        ax2.format_coord = lambda x, y: f"x={int(x)}, y={int(y)}"
        ax3.format_coord = lambda x, y: f"x={round(float(x), 4)}, y={int(y)}"
        ax4.format_coord = lambda x, y: f"x={(round(float(x), 2))}, y={int(y)}"

        plt.tight_layout()
        plt.show()

    def plot_columns(self):
        df_groupby = self.df_eda[['SalesOrderID', 'UnitPrice', 'UnitPriceDiscount', 'ProductCost', 'ModifiedDate']].copy()
        df_groupby['Profit'] = (self.df_eda['UnitPrice'] * (1 - self.df_eda['UnitPriceDiscount']) - self.df_eda['ProductCost'])
        df_groupby['Revenue'] = (self.df_eda['UnitPrice'] * (1 - self.df_eda['UnitPriceDiscount']))

        df_grouped = df_groupby.groupby('SalesOrderID').agg({
            'SalesOrderID': 'first',  # Chọn bất kỳ giá trị nào trong group
            'Revenue': 'sum',  # Tính tổng doanh thu
            'Profit': 'sum',  # Tính tổng lợi nhuận
            'ModifiedDate': 'first'  # Chọn bất kỳ giá trị nào trong group
        }).reset_index(drop=True)

        df_new = df_grouped.groupby('ModifiedDate').agg({
            'SalesOrderID': 'size',
            'Revenue': 'sum',
            'Profit': 'sum'
        }).reset_index()

        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, figsize=(15, 6))

        ax1.plot(df_new['ModifiedDate'], df_new['SalesOrderID'], color='blue', label='Number of sales orders')
        ax2.plot(df_new['ModifiedDate'], df_new['Revenue'], color='green', label='Amount of revenue')
        ax3.plot(df_new['ModifiedDate'], df_new['Profit'], color='red', label='Amount of profit')

        ax1.set_title('Sales Order Over Time', fontweight='bold')
        ax2.set_title('Revenue Over Time', fontweight='bold')
        ax3.set_title('Profit Over Time', fontweight='bold')

        mplcursors.cursor(hover=True)

        for ax in [ax1, ax2, ax3]:
            ax.format_coord = lambda x, y: f"x={x.astype('datetime64[D]').item()}, y={int(y)}"
            ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
            ax.legend()
            ax.grid(True)

        plt.tight_layout()
        plt.show()

    def heatmap_chart(self):
        print(self.df_eda)
        plt.title('Correlation Coefficient Chart Between Data In The Dataset', fontweight='bold', pad=30, fontsize=20)
        sns.heatmap(self.df_eda.corr(), cmap='Blues', annot=True)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    eda = EDA_3()
    eda.check_missing_value()
    eda.get_df_eda_processed()
    eda.time_period()
    eda.describe_dataset()
    eda.frequency_columns()
    eda.plot_columns()
    eda.heatmap_chart()
    print(eda.split_by_year())