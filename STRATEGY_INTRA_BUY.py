# 1. Take Intraday Data  for specific symbol or Universal  which is allowed.
import ConfigVariable
import INTRADAY_NSE_EQ_OHLCV_TV as OHLCV
import pandas as pd

from ConfigVariable import BhavCopy_EQ as ConfigVar

#
# obj = OHLCV.Data_Intraday_EQ()
# obj._main()
# d= obj.df_INTRADAY_NSE_EQ_OHLC_TV
# print(d)

class STRATEGY_INTRA_BUY:

    def __init__(self,df):
        self.df_OHLCV_Local=df
        self.df_distinct_Symbol=pd.DataFrame()

    def Distinct_EQ_Symbol(self):
        self.df_distinct_Symbol=self.df_OHLCV_Local["Symbol"].unique()
        return list(self.df_distinct_Symbol)

    def Scan_Uptrend(self, df_input ,period):
        """ Copy Data in Dataframe """
        df_temp =df_input
        df_temp_2 = pd.DataFrame()

        for OnedayData in (df_temp.iterrows()):
            sym = OnedayData[ConfigVar.Symbol] + "_"+OnedayData[ConfigVar.TIMESTAMP]
            closeprice =OnedayData[ConfigVar.CLOSE]
            print(sym,closeprice)

        # print("pass")



if __name__ == '__main__':

    obj=OHLCV.Data_Intraday_EQ()

    obj.Intrady_Data_Universal()

    d=pd.DataFrame()
    df_OHLC_global=obj.df_INTRADAY_NSE_EQ_OHLC_TV
    if d.count != 0:
        SIB=STRATEGY_INTRA_BUY(df_OHLC_global)
        d=SIB.Distinct_EQ_Symbol()
        df_1 = pd.DataFrame()

        for symbol in d :
            print ( "Scanning Symbol in df " + symbol )
            """ Extract data of specific Symbol passed  """
            filter_1_Search_Symbol = df_OHLC_global [ ConfigVariable.BhavCopy_EQ.Symbol ] == symbol
            df_1 = df_OHLC_global.where ( filter_1_Search_Symbol , inplace = False )

            if df_1.count != 0:
                """ Data is Ready"""
                df_1.dropna ( inplace = True )
                SIB.Scan_Uptrend(df_1,5)

                print(1)

            else:
                print("No Data is Present for Symbol " + symbol)


#
