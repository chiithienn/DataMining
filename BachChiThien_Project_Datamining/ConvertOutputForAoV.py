from ConvertToSPMF import *
from Run_FOSHU_SPMF import *

pd.set_option('display.max_columns', None)

class Convert_Output_To_Model:
    def __init__(self,df_eda,df_groupby,df_result):
        self.df_eda = df_eda
        self.df_groupby = df_groupby
        self.df_result = df_result

        self.df_result_splited = None
        self.df_looked_for = None

        self.unitprice = 0
        self.discount = 0
        self.cost = 0

    def split_itemsets_into_list(self):
        df_result_split = []
        for item in self.df_result['Itemsets']:
            df_result_split.append({'Itemsets': item.split()})
        self.df_result_splited = pd.DataFrame(df_result_split)
        return self.df_result_splited

    def get_name(self):
        df_dataset = pd.read_csv('Dataset3.csv')
        df_result = self.df_result

        df_new = pd.DataFrame(columns=['ProductName', 'Utility ($)', 'Relative Utility'])

        # Tách chuỗi Itemsets thành các mã sản phẩm
        for index, row in df_result.iterrows():
            itemsets = row['Itemsets'].split()
            product_names = []
            for item in itemsets:
                item = int(item)
                # Kiểm tra sự trùng khớp với cột ProductID của df_dataset
                match = df_dataset[df_dataset['ProductID'] == item]
                if not match.empty:
                    product_name = match['Name'].values[0]
                    product_names.append(product_name)

            # Tạo một dòng mới cho df_new
            if product_names:
                df_new = pd.concat([df_new, pd.DataFrame({'ProductName': ['\n'.join(product_names)],
                                                          'Utility ($)': [row['Utility ($)']],
                                                          'Relative Utility': [row['Relative Utility']]})])

        # return df_new
        df_new.to_csv(r'D:\Nam4_HKI\NhaKho_DuLieu\Midterm_Project\TrucQuanKQ_Improve.csv', index=False)

    def look_for_output_in_dataset(self):
        df_check = []
        df_result_splited = self.split_itemsets_into_list()
        df_groupby = self.df_groupby.copy()
        mapping = {0: 'Spring', 1: 'Summer', 2: 'Fall', 3: 'Winter'}
        df_groupby['Season'] = df_groupby['Season'].replace(mapping)
        for i, r in df_groupby.iterrows():
            salesorderid = r['SalesOrderID']
            itemsets = r['ProductID']
            season = r['Season']

            for row in df_result_splited['Itemsets']:
                sodem = 0
                profit = 0
                for j in range(0, len(row), 1):
                    self.unitprice = 0
                    self.discount = 0
                    self.cost = 0
                    if row[j] in itemsets:
                        sodem += 1
                        self.unitprice = self.df_eda.loc[(self.df_eda['SalesOrderID'] == salesorderid) & (
                                self.df_eda['ProductID'] == int(row[j])), 'UnitPrice'].values[0]
                        self.discount = self.df_eda.loc[(self.df_eda['SalesOrderID'] == salesorderid) & (
                                self.df_eda['ProductID'] == int(row[j])), 'UnitPriceDiscount'].values[0]
                        self.cost = self.df_eda.loc[(self.df_eda['SalesOrderID'] == salesorderid) & (
                                self.df_eda['ProductID'] == int(row[j])), 'ProductCost'].values[0]
                        profit += (self.unitprice * (1 - self.discount) - self.cost)
                        continue
                    else:
                        break
                if sodem == len(row):
                    df_check.append(
                        {'SalesOrderID': salesorderid, 'Itemsets': row, 'Profit': int(round(profit, 0)), 'Season': season})

        self.df_looked_for = pd.DataFrame(df_check)
        return self.df_looked_for

    def Convert_df_for_AoV(self):
        df_looked_for = self.look_for_output_in_dataset()

        copy = df_looked_for[['Itemsets', 'Profit', 'Season']].copy()
        copy['Itemsets'] = copy['Itemsets'].apply(lambda x: ' '.join(x))
        copy['Count'] = copy['Itemsets']

        df_pt1 = copy.groupby(['Itemsets', 'Season']).agg({
            'Profit': 'sum',
            'Count': 'size'
        }).reset_index()
        df_pt1.columns = ['Itemsets', 'Season', 'Total Profit', 'Count']

        print(df_pt1)
        df_pt1.to_csv(r'D:\Nam4_HKI\NhaKho_DuLieu\Midterm_Project\TrucQuanKQ1.csv', index=False)
        print('Xong rồi')
        return df_pt1

if __name__ == '__main__':
    C_eda = EDA_3()
    df_eda = C_eda.get_df_eda_processed()

    C_convertSPMF = Convert_to_SPMF()
    df_groupby = C_convertSPMF.get_df_grouped_lookup()

    foshu_spmf = FOSHU_SPMF()
    df_result = foshu_spmf.get_df_result()

    call_class = Convert_Output_To_Model(df_eda,df_groupby,df_result)
    call_class.Convert_df_for_AoV()
    call_class.get_name()