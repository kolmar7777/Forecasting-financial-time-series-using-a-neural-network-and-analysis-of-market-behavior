import data
import numpy as np
import pandas as pd

class test_data:
    def __init__(
            self,
            df: pd.core.frame.DataFrame,
            My_data: data.Data
    ):
        self.df = df
        self.My_data = My_data
        

    def test_correctness_df(self):
        print("===========================Start_testing_for_df_correctness!===========================")
        assert len(self.df) == 3175084, 'df length is not stable'
        assert len(self.My_data.Tickers_list) == 2983, 'List of tickers is not full'
        tickers_to_test = [
            'AAL',
            'MSFT',
            'RCL'
            ]
        for ticker in tickers_to_test:
            assert ticker in self.My_data.Tickers_list, 'test ticker is not in list of tickers'
        assert list(self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//2]].to_dict())[4] == 'Close' , 'Tested column is not Close, but must to be'
        assert pd.Timestamp(2021, 11, 24, 00, 00, 00) in list(self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//2]].to_dict()[list(self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//2]].to_dict())[4]]), 'Timestamp 2021-11-24 00:00:00 not in this Close dict'
        values_for_test_df = [
            self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//2]].to_dict()[list(self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//2]].to_dict())[4]][pd.Timestamp(2021, 11, 24, 00, 00, 00)],
            self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//4]].to_dict()[list(self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//4]].to_dict())[4]][pd.Timestamp(2021, 11, 24, 00, 00, 00)],
            self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//8]].to_dict()[list(self.df.loc[self.My_data.Tickers_list[len(self.My_data.Tickers_list)//8]].to_dict())[4]][pd.Timestamp(2021, 11, 24, 00, 00, 00)]
        ]
        answers_for_df = [
            12.95,
            74.9,
            1.84    
        ]
        assert np.allclose(values_for_test_df, answers_for_df, atol=0.0001), 'answers for df is not correct'
        assert len(self.My_data.Tickers_list) == len(self.My_data.Time_series_space), 'tickers and matrix sizes are not equal'
        assert len(self.My_data.dates_cutted) - 2 == len(self.My_data.Key_ticker_values_list), 'dates aren\'t equal to cutted one'
        #assert self.My_data.Key_ticker_values_list ==  ,'Key ticker has not correct values'
        print("============================End_testing_for_df_correctness!============================")
        print("========================================Success========================================")
        return