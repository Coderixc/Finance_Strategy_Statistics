"""



1. Take Intraday Data  for specific symbol or Universal  which is allowed.
2. Created 2 Coloum "UP_DOWN","CHANGE_%",
    UP_DOWN : compare prev Closing Price With Current Closing  and marked "UP" ,"DOWN","Consts"
    CHANGE_% : Calculate Percentage Change With Previus Closing price with Current Closing

    this Above calculation is Triggered by Function  Scan_Marking_UP_DOWN_CONST()


3.Calculate Coloumn "Check_trend_XX" , XX  belongs  {"UP","DOWN"}
    Func: It will check if , "If Trend(argument passed) matches with values with Column "UP_DOWN "
            It this Matches , it will  insert "XX_P" where P denotes Passed,
            if it doesn't matches with with the value present in "UP_DOWN", it will insert XX_F, wher F denotes passed


"""


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

    def Calculate_Percentage ( self , input1 , input2_base ) :
        try :
            res = (input1 - input2_base) / input2_base * 100
            return round(res,2)
        except :
            res = 0.0
            return res

    def Scan_Marking_UP_DOWN_CONST( self , df_input , period = 50 ) :
        """ Copy Data in Dataframe """
        df_temp = df_input[ : :-1 ].iloc[ 0 :period ][ : :-1 ]
        closingPrice_Prev = 0.0
        closingPrice_Current = 0.0

        list_storeAction = [ ]
        list_percentage = [ ]
        try :
            for OnedayData in (df_temp.iterrows( )) :

                # sym = str(OnedayData [ ConfigVar.Symbol ]) + "_" + str(OnedayData [ ConfigVar.TIMESTAMP ])
                closeprice = float( OnedayData[ 1 ][ ConfigVar.CLOSE ] )

                closingPrice_Current = closeprice

                if closingPrice_Prev != 0 :
                    if closingPrice_Current > closingPrice_Prev :
                        list_storeAction.append( "UP" )
                        list_percentage.append( self.Calculate_Percentage( closingPrice_Current , closingPrice_Prev ) )

                    elif closingPrice_Current < closingPrice_Prev :
                        list_storeAction.append( "DOWN" )
                        list_percentage.append( self.Calculate_Percentage( closingPrice_Current , closingPrice_Prev ) )

                    else :
                        list_storeAction.append( "Const" )
                        list_percentage.append( self.Calculate_Percentage( closingPrice_Current , closingPrice_Prev ) )

                else :
                    list_storeAction.append( "-" )
                    list_percentage.append( "0" )

                # Update Previous Closing Price Variable
                closingPrice_Prev = closeprice

                # print ( sym , closeprice )
            df_temp[ "UP_DOWN" ] = list_storeAction
            df_temp[ "CHNAGE_%" ] = list_percentage
        except :
            print( "Failed to Process function :" )

        finally :
            return df_temp


    def Apply_Trend_On_Period( self,df_Input_With_Col_UP_DOWN_CHNAGE,trend, period=5 ):


        try:
            dt_temp = df_Input_With_Col_UP_DOWN_CHNAGE[ : :-1 ].iloc[ 0 :period ][::-1]

            list_Result =[]

            for row in dt_temp.iterrows():
                updown = row[1]["UP_DOWN" ]
                if(updown == trend):
                    list_Result.append(trend +"_P")
                else:
                    list_Result.append(trend +"_F")

            dt_temp["Check_Trend_"+trend] = list_Result

            return dt_temp

        except:
            print("Failed to Apply Trend on Apply_Trend_On_Period()")

            return pd.DataFrame()



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
                df_marked_U_D_C=  SIB.Scan_Marking_UP_DOWN_CONST(df_1,200)

                """Calculate Trend  on specific Period """
                df_Apply_trend = SIB.Apply_Trend_On_Period(df_marked_U_D_C,"UP",10)




            else:
                print("No Data is Present for Symbol " + symbol)


#
