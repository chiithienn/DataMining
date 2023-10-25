from spmf import Spmf
import pandas as pd
pd.set_option('display.max_columns', None)

class FOSHU_SPMF:
    def __init__(self):
        self.df_result = None
    def Run_SPMF(self,name_input, name_output, arg):
        spmf = Spmf("FOSHU", input_filename=name_input,
                    output_filename=name_output, arguments=[arg])
        spmf.run()
        return spmf

    def get_df_result(self):
        if self.df_result is None:
            spmf = self.Run_SPMF('Dataset_SPMF_Format.txt','output.txt',0.03)
            self.df_result = spmf.to_pandas_dataframe_for_FOSHU(pickle=True)
        return self.df_result

    def get_df_result_each_year(self, name_input, name_output, arg):
        spmf = self.Run_SPMF(name_input, name_output, arg)
        df_result = spmf.to_pandas_dataframe_for_FOSHU()
        return df_result

if __name__ == '__main__':
    foshu = FOSHU_SPMF()
    print(foshu.get_df_result())
    print(foshu.get_df_result_each_year('Dataset_2011.txt', 'output_2011.txt', 0.055))
    print(foshu.get_df_result_each_year('Dataset_2012.txt', 'output_2012.txt', 0.064))
    print(foshu.get_df_result_each_year('Dataset_2013.txt', 'output_2013.txt', 0.0674))
    print(foshu.get_df_result_each_year('Dataset_2014.txt', 'output_2014.txt', 0.03))