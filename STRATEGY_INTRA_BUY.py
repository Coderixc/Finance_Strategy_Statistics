# 1. Take Intraday Data  for specific symbol or Universal  which is allowed.





import INTRADAY_NSE_EQ_OHLCV_TV as OHLCV
import pandas as pd

#
# obj = OHLCV.Data_Intraday_EQ()
# obj._main()
# d= obj.df_INTRADAY_NSE_EQ_OHLC_TV
# print(d)

class STRATEGY_INTRA_BUY:

    def __init__(self,df):
        self.df_OHLCV_Local=df
        self.df_distinct_Symbol = pd.DataFrame()

    def Distinct_EQ_Symbol(self):

        self.df_distinct_Symbol = self.df_OHLCV_Local["Symbol"].unique()
        return  list(self.df_distinct_Symbol)


    def Scan_Uptrend(self,period):
        print("pass")




if __name__ == '__main__':

    obj = OHLCV.Data_Intraday_EQ()

    obj.Intrady_Data_Universal()


    d = pd.DataFrame()
    df_OHLC_global= obj.df_INTRADAY_NSE_EQ_OHLC_TV
    if d.count !=0:

        SIB=STRATEGY_INTRA_BUY(df_OHLC_global)
        d =SIB.Distinct_EQ_Symbol()
        print(d)






