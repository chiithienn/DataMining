import pyodbc
import pandas as pd

print(pyodbc.drivers())

SERVER = r'DESKTOP-5C33P4O\BCT'
DATABASE = 'AdventureWorks2022'
USERNAME = 'mkla123'
PASSWORD = '123'
Encrypt = 'no'

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};\
                    SERVER={SERVER};\
                    DATABASE={DATABASE};\
                    Encrypt={Encrypt};\
                    UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(connectionString)

with open('QueryForDataset1.sql','r') as file:
    sql_query_1 = file.read()
with open('QueryForDataset2.sql','r') as file:
    sql_query_2 = file.read()
with open('QueryForDataset3.sql','r') as file:
    sql_query_3 = file.read()

dataset1 = pd.read_sql_query(sql_query_1,conn)
dataset2 = pd.read_sql_query(sql_query_2,conn)
dataset3 = pd.read_sql_query(sql_query_3,conn)

df1 = pd.DataFrame(dataset1)
df2 = pd.DataFrame(dataset2)
df3 = pd.DataFrame(dataset3)

print(df1.info())
print(df2.info())
print(df3.info())

df1.to_csv (r'D:\Nam4_HKI\NhaKho_DuLieu\Midterm_Project\Dataset1.csv', index = False)
df2.to_csv (r'D:\Nam4_HKI\NhaKho_DuLieu\Midterm_Project\Dataset2.csv', index = False)
df3.to_csv (r'D:\Nam4_HKI\NhaKho_DuLieu\Midterm_Project\Dataset3.csv', index = False)