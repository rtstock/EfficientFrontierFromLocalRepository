# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 14:40:39 2015

@author: justin.malinchak
"""

def geometric_mean(nums):
    ''' 
        Return the geometric average of nums
        @param    list    nums    List of nums to avg
        @return   float   Geometric avg of nums 
    '''
    return (reduce(lambda x, y: x*y, nums))**(1.0/len(nums))

import datetime
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        #raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return False
        
 
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def test_builddataframe():
    import pandas as pd
    import numpy as np
    
    df = pd.DataFrame({'a':np.random.randn(5),
                        'b':np.random.randn(5),
                        'c':np.random.randn(5),
                        'd':np.random.randn(5)})
    cols_to_keep = ['a', 'c', 'd']
    dummies = ['d']
    not_dummies = [x for x in cols_to_keep if x not in dummies]
    data = df[not_dummies]
    print(data)

class perform:
    def set_Symbol(self,Symbol):
        self._Symbol = Symbol
    def get_Symbol(self):
        return self._Symbol
    Symbol = property(get_Symbol, set_Symbol)

    def set_StartDateString(self,StartDateString):
        self._StartDateString = StartDateString
    def get_StartDateString(self):
        return self._StartDateString
    StartDateString = property(get_StartDateString, set_StartDateString)

    def set_EndDateString(self,EndDateString):
        self._EndDateString = EndDateString
    def get_EndDateString(self):
        return self._EndDateString
    EndDateString = property(get_EndDateString, set_EndDateString)

    def set_Period(self,Period):
        self._Period = Period
    def get_Period(self):
        return self._Period
    Period = property(get_Period, set_Period)



    def set_ReturnsDataframe(self,ReturnsDataframe):
        self._ReturnsDataframe = ReturnsDataframe
    def get_ReturnsDataframe(self):
        return self._ReturnsDataframe
    ReturnsDataframe = property(get_ReturnsDataframe, set_ReturnsDataframe)

    #FirstDateOfPriceHistory
    def set_FirstDateOfPriceHistory(self,FirstDateOfPriceHistory):
        self._FirstDateOfPriceHistory = FirstDateOfPriceHistory
    def get_FirstDateOfPriceHistory(self):
        return self._FirstDateOfPriceHistory
    FirstDateOfPriceHistory = property(get_FirstDateOfPriceHistory, set_FirstDateOfPriceHistory)

    
    def __init__(self
                    , symbol
                    , startdate_string='2004-12-31'
                    , enddate_string=''
                    , period = 'monthly' #or daily
                ):
        print('Initialized class pullreturns.perform')

        #today_date = datetime.date.today()
        
        self.Symbol = symbol
        self.StartDateString = startdate_string
        self.EndDateString = enddate_string
        self.Period = period
        
        import datetime
        #today_datetime = datetime.datetime.today()
        
        
        startdate_date = datetime.datetime.strptime(startdate_string, "%Y-%m-%d")
        my_enddate_string = enddate_string
        yesterday_date = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        if len(my_enddate_string) == 0:
            my_enddate_string = str(yesterday_date)

        enddate_date = datetime.datetime.strptime(my_enddate_string, "%Y-%m-%d")
        
        if enddate_date <= startdate_date:
            my_enddate_string = str(yesterday_date)
            
        print '--- about to run'
        self.ReturnsDataframe = self.getreturnsfromlocaldatabase(period=period)
        
        self.PriceHistoryDataframe = self.ReturnsDataframe
        self.FirstDateOfPriceHistory = self.PriceHistoryDataframe.index.tolist()[0]
        
        #print self.ReturnsDataframe
        

    def getreturnsfromlocaldatabase(self,period='Monthly',appendtodaysprice=True):
        symbol = self.Symbol
        import datetime
        today_date = datetime.date.today()
        
        import pandas as pd
        #dates1 = pd.date_range('1910-01', str(today_date)[:7], freq=self.MonthDayCharacter)
        if period == '':
            period = self.Period
        if period == 'monthly':
            dates1 = pd.date_range('1910-01', str(today_date)[:7], freq='M')
        else:
            dates1 = pd.date_range('1910-01-01', str(today_date), freq='D')
            
        dummy_date = datetime.datetime.strptime("1801-01-01", "%Y-%m-%d")
        prev_date = dummy_date
        prev_value = float('Nan')
        
        
        rows_calculatereturns = []        

        rows_calculatereturns.append(['a_symbol','b_periodend','e_pctchange','e_logreturn','d_end'])
        
        import pyodbc
        import datetime
        import calendar
        cnxn = pyodbc.connect(r'Driver={SQL Server};Server=ipc-vsql01;Database=DataAgg;Trusted_Connection=yes;')
        cursor = cnxn.cursor()
        cursor.execute("SELECT * from ProductValues where ProductName = '" + symbol + "' and Measure = 'Returns " + period + "' and SourceName = 'PSN' and Period >= '" + self.StartDateString[:7] + "' and Period <= '" + self.EndDateString[:7] + "' order by Period")
        
        print "SELECT * from ProductValues where ProductName = '" + symbol + "' and Measure = 'Returns " + period + "' and SourceName = 'PSN' and Period >= '" + self.StartDateString[:7] + "' and Period <= '" + self.EndDateString[:7] + "' order by Period"
        
        while 1:
            row = cursor.fetchone()
            
            if not row:
                break
            
            #print self.StartDateString[:7]
            
            i = 0
            a_symbol=''
            b_periodend=''
            e_pctchange=''
            e_logreturn=''
            d_end=''
            for r1 in row:
                i += 1
                if i==1:
                    a_symbol = r1
                if i==3:
                    
                    d1 = datetime.datetime.strptime(r1+'-01', '%Y-%m-%d')
                    year1 = int(d1.strftime("%Y"))
                    month1 = int(d1.strftime("%m"))
                    d2 = calendar.monthrange(year1,month1)
                    #print r1+str(d2[1])
                    d3 =  datetime.datetime.strptime(r1+'-'+str(d2[1]), '%Y-%m-%d')
                    b_periodend = d3.date()
                if i==4:
                    e_pctchange = float(r1)/100.0
                    e_logreturn = float(r1)/100.0
                    d_end = 0.0
            
                #print '-------',r1
            rows_calculatereturns.append([a_symbol,b_periodend,e_pctchange,e_logreturn,d_end])
            #rows_calculatereturns.append(row)
        cnxn.close()


        headers = rows_calculatereturns.pop(0)
        df_calculatereturns = pd.DataFrame(rows_calculatereturns,columns=headers)
        import numpy as np
        df_calculatereturnsfinite = df_calculatereturns[np.isfinite(df_calculatereturns['e_pctchange'].astype(np.float64))]
        df_calculatereturnstotoday = df_calculatereturnsfinite
        df_calculatereturnstotoday.set_index(['b_periodend'], inplace=True)
        #print df_calculatereturns
        #print str(today_date)[:7]
        return df_calculatereturnstotoday


    #ttttttt
    def annualizedreturn(self,logreturnorpctchange):
        # =PRODUCT(F85:F155)^(1/($B85/12))-1
        # [(1.13)*(0.98)*(1.15)*(1.08)]^(12/42)-1
        
        #df_calculatereturns = self.calculatereturns()
        #df_calculatereturns = df_calculatereturns.dropna()
        
        df_returns = self.ReturnsDataframe
        #print '********************************************************'
        #print df_returns
        
        df_returns.sort_index(inplace = True)
        
        #print '-------- df_returns--------'
        #print df_returns
        
        #ttttt
        #firstdate = df_returns.loc[0]['b_periodend']
        ls_indexes = df_returns.index.get_values()
        
        #print 'first index=',ls_indexes[0]
        #print 'last index=',ls_indexes[len(ls_indexes)-1]
        firstdate = self.StartDateString # ls_indexes[0]
        #print 'firstdate',firstdate
        lastdate = ls_indexes[len(ls_indexes)-1] #df_returns.loc[len(df_returns)-1]['b_periodend']
        #print 'lastdate',lastdate
        #print df_returns
        df_returns['e_returnunitized'] = df_returns['e_'+logreturnorpctchange] + float(1.0)

        #print ' --------------------- df_returns-----------------'
        #print df_returns['e_returnunitized']
        #print 'first date changed to:',str(df_returns.index.tolist()[0])
        #firstdate = str(df_returns.index.tolist()[0])
        firstdate = str(self.FirstDateOfPriceHistory)
        print 'self.FirstDateOfPriceHistory',str(self.FirstDateOfPriceHistory)
        
        ls_calculatereturns = df_returns['e_returnunitized'].values.tolist()
        listmultiplied = reduce(lambda x, y: x*y, ls_calculatereturns)
        
        print ' --------------------- df_returns listmultiplied -----------------'
        print listmultiplied
        print ' --------------------- ========================= -----------------'

        #years between
        import datetime
        time1 = datetime.datetime.strptime(str(firstdate) + ' 09:30', "%Y-%m-%d %H:%M")
        #print time1
        time2 = datetime.datetime.strptime(str(lastdate) + ' 16:00', "%Y-%m-%d %H:%M") #datetime.datetime.now() 
        elapsedTime = time2 - time1
        yrs = float(divmod(elapsedTime.total_seconds(), 60.0)[0]/60.0/24.0/365.0)
        print 'time1',time1
        print 'time2',time2
        print 'yrs',yrs

        
        annualizedreturn = listmultiplied ** (float(1)/(yrs)) - 1.0
#        annualizedreturn = listmultiplied ** (float(1)/(float(len(ls_calculatereturnsusingyahoosymbol)/float(12)))) - 1.0
        return annualizedreturn



#    def standarddeviationofcalculatereturns(self,):
#        df_returnsusingyahoosymbol = df_returnsusingyahoosymbol = self.MonthlyReturnsDataframe
#        std_float = float(df_calculatereturnsusingyahoosymbol['e_pctchange'].std())
#        return std_float
    
if __name__=='__main__':
    #symbol = '^DJI' # ,'^RUT','^DJI','AAPL','^GSPC','^OEX','^MID'

    #import datetime
    today_datetime = datetime.datetime.today()
    today_datetime_string_forfilename = today_datetime.strftime('%Y%m%d%H%M%S')

    o = perform( symbol='Mellon Capital Large Cap Core' #,'^DJI','AAPL','^GSPC','^OEX','^MID'
                ,startdate_string='1994-01-01'
                ,enddate_string='2016-04-26'
                ,period='Monthly'
                )
    
    pctchange = o.annualizedreturn('pctchange')
    print 'annualizedreturn pctchange', pctchange
    firstday = o.FirstDateOfPriceHistory
    print 'first day', firstday
    print o.ReturnsDataframe