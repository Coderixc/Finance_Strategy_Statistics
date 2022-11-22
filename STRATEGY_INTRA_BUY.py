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


import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
#
# obj = OHLCV.Data_Intraday_EQ()
# obj._main()
# d= obj.df_INTRADAY_NSE_EQ_OHLC_TV
# print(d)


class STRATEGY_INTRA_BUY :

    def __init__(self,df):
        self.df_OHLCV_Local=df
        self.df_distinct_Symbol=pd.DataFrame()
    def Distinct_EQ_Symbol(self):
        self.df_distinct_Symbol=self.df_OHLCV_Local["Symbol"].unique()
        return list(self.df_distinct_Symbol)

    def Calculate_Percentage( self , input1 , totalPeriod ) :
        try :
            res = input1 / totalPeriod * 100
            return round(res,2)
        except :
            res = 0.0
            return res

    def Calculate_Percentage_Day_Change ( self , input1 , input2_base ) :
        try :
            res = (input1 - input2_base) / input2_base * 100
            return round(res,2)
        except :
            res = 0.0
            return res
    def Calculate_Percentage_SMA( self , input1 , input2_base ) :
        try :
            res = input1 / input2_base * 100
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
                        list_percentage.append( self.Calculate_Percentage_Day_Change( closingPrice_Current , closingPrice_Prev ) )

                    elif closingPrice_Current < closingPrice_Prev :
                        list_storeAction.append( "DOWN" )
                        list_percentage.append( self.Calculate_Percentage_Day_Change( closingPrice_Current , closingPrice_Prev ) )

                    else :
                        list_storeAction.append( "Const" )
                        list_percentage.append( self.Calculate_Percentage_Day_Change( closingPrice_Current , closingPrice_Prev ) )

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
    def _Calculate_Conclusion( self,Count_UpSide,Count_DownSide ):
        result = ""
        try:
            if Count_UpSide > Count_DownSide:
                result ="BUY_SIDE"
            elif Count_UpSide < Count_DownSide:
                result= "SELL_SIDE"
            else:
                result ="BothSide"

            return result


        except:
            print("failed to conclude Conclusion")
    def Calulate_Probabilty_On_Trend( self,df_Input_With_Col_UPDOWN_CHANGE ,period):
        try:
            dt_temp = df_Input_With_Col_UPDOWN_CHANGE[ : :-1 ].iloc[0:period]
            length =len(dt_temp)
            count_up = 0
            count_down =0

            for row in dt_temp.iterrows():

                change = row[1]["CHNAGE_%"]
                if change  >=0:
                    count_up = count_up +1
                elif change <0:
                    count_down =count_down +1
            """ Conclusion """
            res = self._Calculate_Conclusion(count_up,count_down)

            dt_temp["Prob"] = res

            return dt_temp

        except:
            print("Failed to Calculate_Probability_On_trend()")
            return pd.DataFrame()
            pass
    def Find_Long_Side_Trades( self,df_Input_With_Col_UPDOWN_CHANGE,period=10,Allowed_Period_InPercentage = 50 ):
        res = "XX"
        try:
            dt_temp = df_Input_With_Col_UPDOWN_CHANGE[::-1].iloc[0:period]
            res = "Bull"
            count_trend_Bull =0
            count_trend_Bear =0
            for row in dt_temp.iterrows():
                trend = row[1]["UP_DOWN"]
                Curr_Trend= trend
                if trend== "UP":
                    res = "Bull"
                    count_trend_Bull =  count_trend_Bull +1
                else:
                    res ="Failed"
                    count_trend_Bear = count_trend_Bear+1

            per = self.Calculate_Percentage(count_trend_Bull,period)
            if per >= Allowed_Period_InPercentage:
                return res
            else :
                res ="Failed"
                return res



        except:
            print("Failed To calcuate Bull")
            res = "failed"
            return res
    def Find_Short_Side_Trades( self,df_Input_With_Col_UPDOWN_CHANGE,period=10,Allowed_Period_InPercentage = 50 ):
        res = "XX"
        try:
            dt_temp = df_Input_With_Col_UPDOWN_CHANGE[::-1].iloc[0:period]
            res = "Bull"
            count_trend_Bull =0
            count_trend_Bear =0
            for row in dt_temp.iterrows():
                trend = row[1]["UP_DOWN"]
                Curr_Trend= trend
                if trend== "DOWN":
                    res = "Bear"
                    count_trend_Bear =  count_trend_Bear +1
                else:
                    res ="Failed"
                    count_trend_Bull = count_trend_Bull+1

            per = self.Calculate_Percentage(count_trend_Bear,period)
            if per >= Allowed_Period_InPercentage:
                return res
            else :
                res ="Failed"
                return res



        except:
            print("Failed To calcuate Bull")
            res = "failed"
            return res
    def SMA_alpha_GreaterThan_beta_And_Less_Than_Theta( self,df_SMA_alpha_beta_theta ,min_period =14):
        """
        alpha = 14 Days SMA
        beta = 50 Day SMA
        Theta = 200 Day SMA

        logic : alpha > beta  && alpha < Theta   --> Possibility to break Theta in coming Next

        Conclusion: Will consider Bull
        """
        try:

            df_temp= df_SMA_alpha_beta_theta
            List_Result = [ ]

            counter = 0
            for row in df_temp.iterrows():

                alpha  =row[1]["SMA_14"]
                beta = row[1]["SMA_50"]
                theta = row[1]["SMA_200"]

                if counter >= min_period:

                    if (alpha >=beta  ) and (alpha < theta):
                        List_Result.append("CROSSED_1_BUT_NOT_2")
                    elif (alpha >=beta  ) and (alpha >= theta):
                        List_Result.append("CROSSED_2")
                    elif (alpha < beta  ) and (alpha < theta):
                        List_Result.append("WILL_CROSS_1")
                    # elif(alpha >= beta) and (beta < theta):
                    #     List_Result.append("BETA_WILL_CROSS_2")
                    else:
                        List_Result.append(0)
                else:
                    List_Result.append( 0 )

                counter = counter +1

            df_temp["ABT_cases"] = List_Result

            return df_temp

            pass
        except:
            print("Failed To calculate SMA on alpha, Beta , Theta")


    def SMA_SELL_ABT_test( self,df_SMA_alpha_beta_theta ,min_period =14):
        """
        alpha = 14 Days SMA
        beta = 50 Day SMA
        Theta = 200 Day SMA

        logic : alpha < beta  && alpha < Theta   --> Possibility to break Beta in coming Next

        Conclusion: Will consider Bull
        """
        try:

            df_temp= df_SMA_alpha_beta_theta
            List_Result = [ ]

            counter = 0
            for row in df_temp.iterrows():

                alpha  =row[1]["SMA_14"]
                beta = row[1]["SMA_50"]
                theta = row[1]["SMA_200"]

                if counter >= min_period:

                    if (alpha >=beta  ) and (alpha > theta):
                        List_Result.append("S_WILL_FALL_1")
                    elif (alpha > theta  ) and (alpha < beta):
                        List_Result.append("S_CROSSED_1_NOT_2")
                    elif (alpha < theta   ) and (alpha < beta):
                        List_Result.append("S_CROSSED_2")
                    # elif(alpha >= beta) and (beta < theta):
                    #     List_Result.append("BETA_WILL_CROSS_2")
                    else:
                        List_Result.append(0)
                else:
                    List_Result.append( 0 )

                counter = counter +1

            df_temp["ABT_cases_Sell"] = List_Result

            return df_temp

            pass
        except:
            print("Failed To calculate SMA on SELL alpha, Beta , Theta")

    def  Apply_SMA_on_Period( self,df_SMA_alpha_beta_theta, trend,period = 22,delta_allowed = 50 ):
        try:
            dt_temp = df_SMA_alpha_beta_theta[ : :-1 ].iloc[ 0 :period ][::-1]

            list_Result =[]
            count_trend =0

            for row in dt_temp.iterrows():
                _trend = row[1]["ABT_cases" ]
                if _trend == trend:
                    count_trend =count_trend+1


            """ 40 /60  """
            res = self.Calculate_Percentage_SMA(count_trend, period)
            if res >= delta_allowed :
                return "P" ,dt_temp
            else :
                return "F" ,pd.DataFrame()

        except:
            print("Failed to Apply Trend on Apply_SMA_On_Period()")
            return pd.DataFrame()

    def  Apply_SMA_on_Period_SELL( self,df_SMA_alpha_beta_theta, trend,period = 22,delta_allowed = 50 ):
        try:
            dt_temp = df_SMA_alpha_beta_theta[ : :-1 ].iloc[ 0 :period ][::-1]

            list_Result =[]
            count_trend =0

            for row in dt_temp.iterrows():
                _trend = row[1]["ABT_cases_Sell" ]
                if _trend == trend:
                    count_trend =count_trend+1


            """ 40 /60  """
            res = self.Calculate_Percentage_SMA(count_trend, period)
            if res >= delta_allowed :
                return "P" ,dt_temp
            else :
                return "F" ,pd.DataFrame()

        except:
            print("Failed to Apply Trend on Apply_SMA_On_Period()")
            return pd.DataFrame()


""" END OF DEFING CLASS WITH ITS PROPERTIES  AND OBJECT  """




if __name__ == '__main__':

    obj=OHLCV.Data_Intraday_EQ()

    obj.Intrady_Data_Universal()

    d=pd.DataFrame()
    df_OHLC_global=obj.df_INTRADAY_NSE_EQ_OHLC_TV
    if d.count != 0:
        SIB=STRATEGY_INTRA_BUY(df_OHLC_global)
        d=SIB.Distinct_EQ_Symbol()
        df_1 = pd.DataFrame()

        List_Bull_Side_CROSSED_1_BUT_NOT_2 = []
        List_Bull_Side_WILL_CROSS_1 =[]
        List_Symbol =[]
        List_Bear_Side = []

        List_SELL_Side_WILL_CROSS_1 =[]

        List_SMA_BELOW_1=[]

        for symbol in d :
            # print ( "Scanning Symbol in df " + symbol )
            """ Extract data of specific Symbol passed  """
            filter_1_Search_Symbol = df_OHLC_global [ ConfigVariable.BhavCopy_EQ.Symbol ] == symbol
            df_1 = df_OHLC_global.where ( filter_1_Search_Symbol , inplace = False )

            if df_1.count != 0:
                """ Data is Ready"""
                df_1.dropna ( inplace = True )
                df_marked_U_D_C=  SIB.Scan_Marking_UP_DOWN_CONST(df_1,350)


                """ Calculating MOVING AVERAGE ON DIFF PERIOD """

                df_marked_U_D_C["SMA_14"]=  df_marked_U_D_C[ConfigVariable.BhavCopy_EQ.CLOSE].rolling(14,min_periods=1).mean()
                df_marked_U_D_C["SMA_21"]=  df_marked_U_D_C[ConfigVariable.BhavCopy_EQ.CLOSE].rolling(21,min_periods=1).mean()
                df_marked_U_D_C["SMA_50"]=  df_marked_U_D_C[ConfigVariable.BhavCopy_EQ.CLOSE].rolling(50,min_periods=1).mean()
                df_marked_U_D_C["SMA_200"]=  df_marked_U_D_C[ConfigVariable.BhavCopy_EQ.CLOSE].rolling(200,min_periods=1).mean()


                # """ CASE 1: ABT testing  """
                df_ABT = SIB.SMA_alpha_GreaterThan_beta_And_Less_Than_Theta(df_marked_U_D_C)

                """Calculate Trend  on specific Period """
                # df_Apply_trend = SIB.Apply_Trend_On_Period(df_marked_U_D_C,"UP",10)

                """Calculate Probability on trend  in a given Period """
                # df_Prob_on_BUY_OR_SELL =SIB.Calulate_Probabilty_On_Trend(df_marked_U_D_C,20)



                """ Calcuate Bear"""
                # res = SIB.Find_Short_Side_Trades(df_marked_U_D_C,3)
                # if res == "Bear":
                #     List_Bear_Side.append(str(symbol)  +"_"+ str(res))
                    # print(str(symbol)  +"_"+ str(res))
                # print( symbol )



                """Calculate BULL USING SMA CONDITION"""
                res_sma,df_SMA_Test =SIB.Apply_SMA_on_Period(df_marked_U_D_C,"CROSSED_1_BUT_NOT_2",23,90)
                if res_sma == "P" :
                    # List_SMA_BELOW_1.append(str(symbol) + "_" +res_sma )
                    """Recursive Using Func: Calcuate BULL"""
                    res = SIB.Find_Long_Side_Trades( df_SMA_Test , 10,70 )
                    if res == "Bull" :
                        List_Bull_Side_CROSSED_1_BUT_NOT_2.append( str( symbol )+" _"+str( res ) )



                res_sma1,df_SMA_Test1 =SIB.Apply_SMA_on_Period(df_marked_U_D_C,"WILL_CROSS_1",23,90)
                if res_sma1 == "P" :
                    # List_SMA_BELOW_1.append( str( symbol )+"_"+res_sma )
                    """Recursive Using Func: Calcuate BULL"""
                    res1 = SIB.Find_Long_Side_Trades( df_SMA_Test1 , 10 , 70 )
                    if res1 == "Bull" :
                        List_Bull_Side_WILL_CROSS_1.append( str( symbol )+" _"+str( res1 ) )



                """ SELL SIDE CONFIGURATION"""
                df_ABT1s = SIB.SMA_SELL_ABT_test(df_marked_U_D_C)

                res_sma_sell,df_SMA_ABT_SELL =SIB.Apply_SMA_on_Period_SELL(df_marked_U_D_C,"S_CROSSED_1_NOT_2",23,90)
                if res_sma_sell == "P" :
                    # List_SMA_BELOW_1.append( str( symbol )+"_"+res_sma )
                    """Recursive Using Func: Calcuate BEAR"""
                    res1 = SIB.Find_Short_Side_Trades( df_SMA_ABT_SELL , 10 , 50 )
                    if res1 == "Bear" :
                        List_SELL_Side_WILL_CROSS_1.append( str( symbol )+" _"+str( res1 ) )






                        # print( str( symbol )+"_"+str( res ) )

                    # """Calculate BULL USING SMA CONDITION  -- > SMA_50_WILL_CROSS_200"""
                    # res_sma , df_SMA_Test = SIB.Apply_SMA_on_Period( df_marked_U_D_C , "BETA_WILL_CROSS_2" , 20 , 70 )
                    # if res_sma == "P" :
                    #     List_SMA_BELOW_1.append( str( symbol )+"_"+res_sma )
                    #     """Recursive Using Func: Calcuate BULL"""
                    #     res = SIB.Find_Long_Side_Trades( df_SMA_Test , 4 )
                    #     if res == "Bull" :
                    #         List_Bull_Side.append( str( symbol )+"_"+str( res ) )
                    #         print("SMA_50_WILL_CROSS_200_"+ str( symbol )+"_"+str( res ) )
                    # print( symbol )

                    # print(str(symbol) + "_" +res_sma)

                    # gfg_csv_data = df_marked_U_D_C.to_csv( symbol+'.csv' , index = True )
                    # print( '\nCSV String:\n' , gfg_csv_data )

                if  symbol == "TORNTPHARM":
                    print("Scanning Ony :" + symbol)
                    # gfg_csv_data = df_marked_U_D_C.to_csv( symbol+'.csv' , index = True )
                #     print( '\nCSV String:\n' , gfg_csv_data )


                # """ Calcuate BULL"""
                # res = SIB.Find_Long_Side_Trades(df_SMA_Test,4)
                # if res == "Bull":
                #     List_Bull_Side.append(str(symbol)  +"_"+ str(res))
                #     print(str(symbol)  +"_"+ str(res))
                # print( symbol )





            else:
                print("No Data is Present for Symbol " + symbol)


        """ Display Conclusion Result"""

        for cond1 in List_Bull_Side_CROSSED_1_BUT_NOT_2:
            mess = cond1 + "_Bull" +"_CROSSED_1_BUT_NOT_2"
            print(mess)

        print( "\n" )
        # print( "\n" )
        # print( "\n" )

        for cond1 in List_Bull_Side_WILL_CROSS_1:
            mess = cond1 + "_Bull" +"_WILL_CROSS_1"
            print(mess)

        print( "\n SELL SIGNAL " )
        print( "\n" )

        for cond1 in List_SELL_Side_WILL_CROSS_1:
            mess = cond1 + "_Bear" +"S_CROSSED_1_NOT_2"
            print(mess)



        print( "Scanning Finsished!" )
#
