from EDA3 import *

class Convert_to_SPMF:
    def __init__(self):
        self.df_org = EDA_3().get_df_eda_processed()
        self.df_grouped_lookup = None

    def group_by(self):
        df = self.df_org.copy()

        df['Season'] = pd.cut(df['ModifiedDate'].dt.month, bins=[1, 4, 7, 10, 13], labels=[0, 1, 2, 3], include_lowest=True)
        df['Positive_Profit_Total'] = (df['UnitPrice'] * (1 - df['UnitPriceDiscount']) - df['ProductCost']).clip(lower=0)
        df['Profit_Unit'] = (df['UnitPrice'] * (1 - df['UnitPriceDiscount']) - df['ProductCost'])

        grouped = df.groupby('SalesOrderID').agg({
            'ProductID': lambda x: ' '.join(map(str, x)),
            'Positive_Profit_Total': lambda x: round(x.sum(), 0).astype(int),
            'Profit_Unit': lambda x: ' '.join(map(str, round(x, 0).astype(int))),
            'Season': 'max'
        }).reset_index()

        return grouped

    def format_spmf_each_year(self,df):
        df['Season'] = pd.cut(df['ModifiedDate'].dt.month, bins=[1, 4, 7, 10, 13], labels=[0, 1, 2, 3], include_lowest=True)
        df['Positive_Profit_Total'] = (df['UnitPrice'] * (1 - df['UnitPriceDiscount']) - df['ProductCost']).clip(lower=0)
        df['Profit_Unit'] = (df['UnitPrice'] * (1 - df['UnitPriceDiscount']) - df['ProductCost'])

        grouped = df.groupby('SalesOrderID').agg({
            'ProductID': lambda x: ' '.join(map(str, x)),
            'Positive_Profit_Total': lambda x: round(x.sum(), 0).astype(int),
            'Profit_Unit': lambda x: ' '.join(map(str, round(x, 0).astype(int))),
            'Season': 'max'
        }).reset_index()

        # Tạo chuỗi kết quả
        grouped['Result'] = grouped['ProductID'] + ':' + grouped['Positive_Profit_Total'].astype(str) + ':' + grouped[
            'Profit_Unit'] + ':' + grouped['Season'].astype(str)
        spmf_format_each_year = grouped['Result'].copy()

        return spmf_format_each_year

    def format_SPMF(self):
        grouped = self.group_by()
        # Tạo chuỗi kết quả
        grouped['Result'] = grouped['ProductID'] + ':' + grouped['Positive_Profit_Total'].astype(str) + ':' + grouped[
            'Profit_Unit'] + ':' + grouped['Season'].astype(str)
        spmf_format = grouped['Result'].copy()

        return spmf_format

    def save_into_txt(self, spmf_format):
        with open('Dataset_SPMF_Format.txt', 'w') as file:
            file.write('')
        with open('Dataset_SPMF_Format.txt', 'a') as file:
            for i, r in enumerate(spmf_format):
                file.writelines(r)
                if i + 1 != len(spmf_format):
                    file.writelines('\n')

    def save_into_txt_each_year(self, spmf_format_each_year, name_file):
        with open(name_file, 'w') as file:
            file.write('')
        with open(name_file, 'a') as file:
            for i, r in enumerate(spmf_format_each_year):
                file.writelines(r)
                if i + 1 != len(spmf_format_each_year):
                    file.writelines('\n')

    def get_df_grouped_lookup(self):
        if self.df_grouped_lookup is None:
            self.df_grouped_lookup = self.group_by()
        return self.df_grouped_lookup

if __name__ == '__main__':
    ctspmf = Convert_to_SPMF()
    ctspmf.save_into_txt(ctspmf.format_SPMF())

    EDA_3 = EDA_3()

    ctspmf.save_into_txt_each_year(ctspmf.format_spmf_each_year(EDA_3.split_by_year()[2011]),'Dataset_2011.txt')
    ctspmf.save_into_txt_each_year(ctspmf.format_spmf_each_year(EDA_3.split_by_year()[2012]), 'Dataset_2012.txt')
    ctspmf.save_into_txt_each_year(ctspmf.format_spmf_each_year(EDA_3.split_by_year()[2013]), 'Dataset_2013.txt')
    ctspmf.save_into_txt_each_year(ctspmf.format_spmf_each_year(EDA_3.split_by_year()[2014]), 'Dataset_2014.txt')