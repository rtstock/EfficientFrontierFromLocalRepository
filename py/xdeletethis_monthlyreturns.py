# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 14:40:39 2015

@author: justin.malinchak
"""

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

def bysymbol(symbol,startdate_string='1980-01-01'):
    # Parameters
    #startdate_string = '1980-01-01'
    #symbol = '^GSPC'  ^GSPC   ^OEX    ^VIX    ^OEX    ^MID   ^RUT

    # ##########
    # Date setup
    import datetime
    #today_datetime = datetime.datetime.today()
    today_date = datetime.date.today()
    yesterday_date = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
    #print str(today_date)
    
    import pullprices as pp
    df_00 = pp.stockhistorybackfilledtodatframeofstockhistoryinstancesusingcache(symbol,startdate_string,str(yesterday_date)) #,str(today_date))
    #print list(df_00)#['Close','Adj Close']
    #print df_00[['Close','Adj Close']]
    
    import pandas as pd
    dates1 = pd.date_range('1910-01', str(today_date)[:7], freq='M')
    
    dummy_date = datetime.datetime.strptime("1801-01-01", "%Y-%m-%d")
    prev_date = dummy_date
    prev_value = float('Nan')
    
    rows_monthlyreturns = []        
    #rows_optionpricescurrent.append(['optionsymbol','stockprice','strike','pdeltapct_to_sell_price','cumprob_to_sell_price','bid','ask','last'])
    rows_monthlyreturns.append(['a_symbol','b_monthend','e_pctchange','d_end'])
    
    
    for dt in dates1:
        if str(dt.date()) in df_00.index:
            #print dt.date()
            myobj = df_00.loc[str(dt.date())]
            #print myobj
            curr_date = dt.date()
            curr_value = myobj['Adj Close']
            if prev_date != dummy_date:
                change_pct = (curr_value - prev_value)/prev_value
                #print symbol,prev_date,prev_value,curr_date,curr_value,change_pct
                rows_monthlyreturns.append([symbol,curr_date,change_pct,curr_value])
                #'{percent:.2%}'.format(percent=pdeltapct_to_sell_price)
                #print symbol,curr_date,change_pct
                
            prev_date = dt.date()
            prev_value = myobj['Adj Close']
    
    
    headers = rows_monthlyreturns.pop(0)
    df_monthlyreturns = pd.DataFrame(rows_monthlyreturns,columns=headers)
    import numpy as np
    df_monthlyreturnsfinite = df_monthlyreturns[np.isfinite(df_monthlyreturns['e_pctchange'])]
    #print df_monthlyreturnsfinite
    #print df_00
    
    stock_dataframe = pp.stock_dataframe(symbol)
    myobj = df_00.loc[str(prev_date)]
    prev_ending = myobj['Adj Close']
    curr_price = stock_dataframe['last'][0]
    curr_pctchange = (curr_price - prev_ending) / prev_ending
    
    #df_curr = pd.DataFrame([symbol,today_date,curr_pctchange], columns=['a_symbol','b_monthend','e_pctchange'])
    #newrow = np.array([symbol,today_date,curr_pctchange])
    #columns=['a_symbol','b_monthend','e_pctchange','d_end']
    
    #import numpy as np
    
    mydict = {}
    mydict[0] = {'a_symbol':symbol,'b_monthend':str(today_date),'e_pctchange':curr_pctchange,'d_end':curr_price}
    df_curr = pd.DataFrame(mydict).T
    #print df_curr.T
    
    
    df_monthlyreturnstotoday = df_monthlyreturnsfinite.append(df_curr, ignore_index=True)
    #print df_monthlyreturns
    print str(today_date)[:7]
    return df_monthlyreturnstotoday
    #index = np.arange(1) # array of numbers for the number of samples
    #df_curr = pd.DataFrame(columns=columns, index = index)
    #df.ix[0] = item
    #df_curr = pd.DataFrame(columns=columns)
    #df_curr.add(newrow,axis=columns)
    #print df_curr
    #data=newrow, index=[str(today_date)], 
    #DataFrame.add(other, axis='columns', level=None, fill_value=None)¶
    #s = df_curr.xs(0)
    #s.name = str(today_date)
    #print s
    
    #df_monthlyreturnsfinite.append(s)
    #print df_monthlyreturnsfinite
    
    #print ls_00
    
    
    #import datetime
    #
    #start = datetime.datetime.strptime("2014-01-01", "%Y-%m-%d")
    #end = datetime.datetime.strptime("2015-07-31", "%Y-%m-%d")
    #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    #
    #for date in date_generated:
    #    print date.strftime("%d-%m-%Y")


if __name__=='__main__':
    df = monthlyreturns('^GSPC')
    print df
    print 'there was no method from library mydata chosen'