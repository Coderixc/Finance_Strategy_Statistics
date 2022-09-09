#INTRADY_NSE_EQ_OHLC_TV

# Prepare Connection
# Fetch Intraday Data

# Proxy Function or Main Function
# def INIT()  ---- act as a constructor
# def _main() ---- act as a interface/medium by which any object wasnt to call any function of this script ,can interact with Proxy main (_main())
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
import MySQLdb
import pandas as pd



class Data_Intraday_EQ:

    def __init__ ( self, KEY = 1 ) :
        self.IP = "127.0.0.1"
        self.User = "root"
        self.PassWord = "123456"
        self.Schema = "pricedata"
        self.Key = KEY

        self.df_INTRADAY_NSE_EQ_OHLC_TV =""
        self.Data_One_Symbol =""

        # self.Creating_a_Database()
    #
    # def INIT ( self ) :
    # Creating a Database
    def Creating_a_Database ( self  ) :
        try :

            # print ( "Credential :" + self.IP + "," + self.User + "," + self.PassWord + ",SCHEMA " + self.Schema )
            self.db_connection = MySQLdb.connect ( self.IP , self.User , self.PassWord , self.Schema )
            print ( "Sucessfully connected to Mysql" )
            return True

        except Exception as E1 :
            print ( "Failed to connect Mysql with mentioned credential : " + E1 )
            return False

    def PrepareMysql(self):

        query="SELECT * FROM pricedata.bhavcopyprice  order  by Timestamp ASC   ;"

        self.df_INTRADAY_NSE_EQ_OHLC_TV=pd.read_sql(query,con=self.db_connection)

    #     Request One Symbol Data from DB
    def Intrady_Data_OneSymbol(self,symbol):

        query="SELECT * FROM pricedata.bhavcopyprice  where Symbol = '"+symbol+"' order  by Timestamp ASC   ;"

        self.Data_One_Symbol=pd.read_sql(query,con=self.db_connection)

    def _main ( self ) :
        if(self.Creating_a_Database()):
            self.PrepareMysql()
            print("passed")








obj =Data_Intraday_EQ()
obj._main()
d=obj.df_INTRADAY_NSE_EQ_OHLC_TV
print(d.info())
