# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 17:31:47 2015

@author: justin.malinchak
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 17:18:11 2015

@author: justin.malinchak
"""

class output:

    def set_PermutationsDataframe(self,PermutationsDataframe):
        self._PermutationsDataframe = PermutationsDataframe
    def get_PermutationsDataframe(self):
        return self._PermutationsDataframe
    PermutationsDataframe = property(get_PermutationsDataframe, set_PermutationsDataframe)

    def set_EfficientFrontierObject(self,EfficientFrontierObject):
        self._EfficientFrontierObject = EfficientFrontierObject
    def get_EfficientFrontierObject(self):
        return self._EfficientFrontierObject
    EfficientFrontierObject = property(get_EfficientFrontierObject, set_EfficientFrontierObject)

    def set_DictionaryOfSymbols(self,DictionaryOfSymbols):
        self._DictionaryOfSymbols = DictionaryOfSymbols
    def get_DictionaryOfSymbols(self):
        return self._DictionaryOfSymbols
    DictionaryOfSymbols = property(get_DictionaryOfSymbols, set_DictionaryOfSymbols)

    def myfunc(self,x, pos=0): 
        return '%1.1f%%'%(100*x)
  
    
    def __init__(self,
                     json_string_of_symbols_and_weights 
                     ,  startdate_string = '2005-01-01'
                     ,  enddate_string = ''#'2013-12-31'
                     ,  period = 'monthly'
                     ,  pctchangeorlogreturn = 'pctchange'
                     ,  source = 'Yahoo'
                     ):
        print 'initializing outputefficientfrontier...'
        print 'json_string_of_symbols_and_weights', json_string_of_symbols_and_weights
        import json
        print 'setting up a dictionary from the string...'
        mySymbolsDict = json.loads(json_string_of_symbols_and_weights)
        self.DictionaryOfSymbols = mySymbolsDict
        print '++++++++++++++++++++++++++++++++'
        print '  here it is as a dict'
        print '++++++++++++++++++++++++++++++++'
        print type(mySymbolsDict)
        print 'ok looks like it worked...'
        self._setup(mySymbolsDict
                     ,  startdate_string
                     ,  enddate_string 
                     ,  period
                     ,  pctchangeorlogreturn
                     ,  source
                     )

    def _setup(self
                 ,  mySymbolsDict 
                 ,  startdate_string
                 ,  enddate_string 
                 ,  period
                 ,  pctchangeorlogreturn
                 ,  source
                 ):
        print('Initialized def _setup')
        import efficientfrontier as ef   

        print mySymbolsDict
        
        o = ef.perform(mySymbolsDict,startdate_string,enddate_string,period,pctchangeorlogreturn,source) 
        
        self.EfficientFrontierObject = o
        
    def permutationstodataframe(self,iterations):
        import pandas as pd
        df_permutations = self.EfficientFrontierObject.permutationstodataframe(iterations)
        
        #print df_permutations
        mydf = pd.DataFrame(columns=('portfolioreturn', 'portfoliostandarddeviation','weightstring'))
        
        #Do map here to make quicker
        for index, row in df_permutations.iterrows():
            randomweightseries = row['value']['randomweightseries']
            
            weightstring = ''
            for idx in randomweightseries.iteritems():
                weightstring = weightstring + str(idx[0])+'='+ str(idx[1]*100)+'%'+chr(10)
            weightstring = weightstring[:-1]
            #print weightstring
            #print '---'
            portfolioreturn = row['value']['portfolioreturn']
            portfoliostandarddeviation = row['value']['portfoliostandarddeviation'] 
            mydf.loc[index] = [portfolioreturn,portfoliostandarddeviation,weightstring]
        mydf['returnoverrisk'] = mydf.portfolioreturn / mydf.portfoliostandarddeviation
        self.PermutationsDataframe = mydf
        return mydf

    def drawsail(self,numberofpermutations = 1000,optimalpctasdecimal = 0.90):
        df = self.permutationstodataframe(numberofpermutations)
        #df['returnoverrisk'] = df.portfolioreturn / df.portfoliostandarddeviation
        maxreturnoverriskseries = df.ix[df['returnoverrisk'].idxmax()]
        df['maxreturnoverrisk'] = maxreturnoverriskseries['returnoverrisk']
        #print df
        print 'the max returnoverrisk is:',maxreturnoverriskseries['returnoverrisk']
        #df.apply(lambda row: min([row['A'], row['B']])-row['C'], axis=1)
        #df.plot(title='Title Here')
        import matplotlib.pylab as plt
        #import numpy as np
        #import pandas as pd
        #import numpy as np
        #df = pd.DataFrame(np.random.randn(10,2), columns=['col1','col2'])
        #df['col3'] = np.arange(len(df))**2 * 100 + 100
        #print df
        #plt.scatter(df.col1, df.col2, s=df.col3)
        #colors = np.where(df.col3 > 300, 'r', 'k')

        #fig = plt.figure()
        fig = plt.figure(figsize=(11.0, 8.0)) # in inches!

        print 'DictionaryOfSymbols Count',len(self.DictionaryOfSymbols)
        
        ax = fig.add_subplot(111, position=[0.07, 0.07, 0.90, 0.95 - ((len(self.DictionaryOfSymbols)*5)/100.0)]) # calculates a height for the chart frame
        cond = df.returnoverrisk > df.maxreturnoverrisk * optimalpctasdecimal
        subset_a = df[cond].dropna()
        subset_b = df[~cond].dropna()
        plt.scatter(subset_a.portfoliostandarddeviation, subset_a.portfolioreturn, s=7, c='red', label='frontier >' + str(int(optimalpctasdecimal*100))+'%',marker='s', edgecolors='none')
        plt.scatter(subset_b.portfoliostandarddeviation, subset_b.portfolioreturn, s=7, c='dodgerblue', label='suboptimal',marker='s', edgecolors='none') 
        
        from matplotlib.ticker import FuncFormatter 
        #ax = plt.subplot(111)
        
        ax.xaxis.set_major_formatter(FuncFormatter(self.myfunc)) 
        ax.yaxis.set_major_formatter(FuncFormatter(self.myfunc)) 
        
        plt.legend(fontsize=12)    
        fig.suptitle('Efficient Frontier Optimal Weights  (' + self.EfficientFrontierObject.StartDateString +' to ' + self.EfficientFrontierObject.EndDateString +')' +
            chr(10) + 
            maxreturnoverriskseries['weightstring'] + 
            chr(10) +
            'N=' + str(numberofpermutations) + '   '
            'Annualized Return=' + str(round(maxreturnoverriskseries['portfolioreturn']*100,2)) + '%   ' +
            'StDev=' + str(round(maxreturnoverriskseries['portfoliostandarddeviation']*100,2)) + '%', fontsize=12)
        plt.xlabel('Risk (StDev)', fontsize=12)
        plt.ylabel('Return (%)', fontsize=12)
        #fig, ax = plt.subplots(figsize=(50,50))
        #for item in [fig, ax]:
        #    item.patch.set_visible(False)
            
        #plt.text(30,10,'hello')
        import datetime
        today_datetime = datetime.datetime.today()
        today_datetime_string_forfilename = today_datetime.strftime('%Y%m%d%H%M%S')
        import config
        cachefilename = config.mycachefolder + '\\drawsail '+today_datetime_string_forfilename+'.jpg'
        fig.savefig(cachefilename)

        csvfilename = config.mycachefolder + '\\drawsail '+today_datetime_string_forfilename+'.csv'
        self.PermutationsDataframe.to_csv(csvfilename,',')
        return cachefilename
        
        # To get a list of colors        
#        import matplotlib        
#        for name, hex in matplotlib.colors.cnames.iteritems():
#            print(name, hex)

        

if __name__=='__main__':
    
#               # Use this one to test Yahoo
#    o = output(      mySymbolsDict = ['WMT','NKE','T','MCD','JPM','^RUT'] 
#                     ,  startdate_string = '2014-12-31'
#                     ,  enddate_string = '2016-03-31'
#                     ,  period = 'monthly'
#                     ,  pctchangeorlogreturn = 'pctchange'
#                     ,  source = 'Yahoo'
#              )
    #mySymbolsDict={'Mellon Capital Large Cap Core':[0.5,0.2],'Boston Co US Mid Cap Growt':[0.5,0.1],'Harding Loevner Glob Eq ADR':[0.5,0.1],'Logan Capital Concentrated Val':[0.5,0.1]}
    #mySymbolsDict={'Granite Partners Small Core Plus':[0.5,0.2],'Harding Loevner Glob Eq ADR':[0.5,0.1],'Logan Capital Concentrated Val':[0.5,0.1],'Hilton Capital YP':[0.4,0.05]}
    #mySymbolsDict={'WMT':[0.5,0.1],'NKE':[0.5,0.1],'T':[0.5,0.1],'MCD':[0.5,0.1]}
    #mySymbolsDict={'Granite Partners Small Core Plus':[0.5,0.2],'Harding Loevner Glob Eq ADR':[0.5,0.1],'Logan Capital Concentrated Val':[0.5,0.1],'Hilton Capital YP':[0.4,0.05]}
    #print mySymbolsDict
    
    #json_string = '{ "a":["123456789", "aaa","bbbb"],"b":["1111","222","3333"] }'
    #obj = json.loads(json_string)    # obj now contains a dict of the data
    #import json
    #json_string = '{"Granite Partners Small Core Plus":[0.5,0.2],"Harding Loevner Glob Eq ADR":[0.5,0.1],"Logan Capital Concentrated Val":[0.5,0.1],"Hilton Capital YP":[0.4,0.05]}'
    #json_string = '{"Blue Shores Capital Global Long/Short Equity":[0.5,0.2],"Logan Capital Management Inc. Logan Core 60/40":[0.5,0.2],"Logan Capital Management Inc. Logan Growth":[0.5,0.2],"Harding Loevner LP Global Equity ADR":[0.5,0.2]}'
    #json_string = '{"Granite Partners Small Core Plus":[max:0.5,min:0.1],"Harding Loevner Glob Eq ADR":[max:0.5,min:0.1],"Logan Capital Concentrated Val":[max:0.5,min:0.1],"Hilton Capital YP":[max:0.5,min:0.3]}'
    #mySymbolsDict = json.loads(json_string)    # obj now contains a dict of the data
    #print mySymbolsDict
    json_string = '{"Blue Shores Capital|Global Long/Short Equity":[0.4,0.1],"Logan Capital Management Inc.|Logan Growth":[0.4,0.1],"Carl Domino Inc.|Large Cap Value Equity":[0.4,0.05],"Logan Capital Management Inc.|Logan International Dividend ADR":[0.4,0.05],"Hays Advisory LLC|International ETF":[0.4,0.05]}'
    # "Blue Shores Capital|Global Long/Short Equity":[0.5,0.1],
    #
    o = output(    json_string
                ,  startdate_string = '2010-12-31'
                ,  enddate_string = '2016-05-31' #'2013-12-31'
                ,  period='Monthly'
                ,  pctchangeorlogreturn = 'pctchange'
                ,  source='local'
                ) 

    print o.drawsail(1000,0.92)

    #o.PermutationsDataframe

    # 'LNG','AGN','LVNTA','SPR','ALLE','VALE','P','JD','ALNY','CDK','FB','DAL','DOOR','ICPT','ABUS','AXON' 

    # 'WMT','NKE','T','MCD','JPM','^RUT','XOM','MSFT','YHOO','QQQ','HD','GS','BAC','LEO'
    # '^GSPC','^OEX','^MID','^RUT','^DJI','^IXIC','^GSPC','^DJI','^OEX','^RUT'
    #'WMT','NKE','T','MCD','JPM','^RUT'
    #'^GSPC','^OEX','^MID','^RUT','^DJI'
    
    #print o.EfficientFrontierObject.correlationmatrix()
    #print o.EfficientFrontierObject.covariancematrix
    #print o.EfficientFrontierObject.ReturnsDataframe

    #print ' ---- here is just one random weight Series... ----'
    #print o.EfficientFrontierObject.portfolioriskreturnrandomweight()
    


'''
40% S&P 500 / 60% BIGC|40% S&P 500 / 60% BIGC
80% S&P500 / 20% MSCI EAFE Net|80% S&P500 / 20% MSCI EAFE Net
BAML 1-Yr US Treasury Note -USDU|BAML 1-Yr US Treasury Note -USDU
Barclays  1-10Y Muni|Barclays 1-10 Year Municipal
Barclays 1-3Y Govt|Barclays 1-3 Year Government
Barclays 1-3Y Gv/Crd|Barclays 1-3 Year Govt/Credit
Barclays 15Y Muni|Barclays 15 Year Municipal
Barclays 1Y Muni|Barclays 1 Year Municipal
Barclays 3Y Muni|Barclays 3 Year Municipal
Barclays Aggregate|Barclays Aggregate
Barclays Govt/Credit|Barclays Government/Credit
Barclays Int Gv/Crd|Barclays Intermediate Govt/Credit
Barclays Municipal|Barclays Municipal
Blue Shores Cap|GMSI
Blue Shores Capital|Global Long/Short Equity
Carl Domino Inc.|Large Cap Value Equity
Crawford Investment Counsel Inc.|Core Bond
Crawford Investment Counsel Inc.|Dividend Growth
Crawford Investment Counsel Inc.|Dividend Yield
Crawford Investment Counsel Inc.|National Intermediate Municipal Bond
Cumberland Advisors Inc.|Fixed Income and Cash Portfolios
Cumberland Advisors Inc.|Municipal Bonds Total Return
Cyrus J. Lawrence LLC|Cyrus J. Lawrence U.S. Equity
Granite Investment Partners LLC|Small Core Equity
Granite Investment Partners LLC|Small Core Plus Equity
Harding Loevner LP|Global Equity ADR
Harding Loevner LP|International Equity ADR
Hays Advisory LLC|Global ETF
Hays Advisory LLC|International ETF
Hays Advisory LLC|Long Term Growth
HFRX Equity Hedge|HFRX Equity Hedge Index
Hilton Capital Management|Hilton Tactical Income
John Hancock Asset Management|Fundamental Large Cap Core Wrap
John Hancock Asset Management|International Value ADR Wrap
John Hancock Asset Management|Sovereign Dividend Performers Wrap
Logan Capital Management Inc.|Logan Concentrated Value
Logan Capital Management Inc.|Logan Core 60/40
Logan Capital Management Inc.|Logan Growth
Logan Capital Management Inc.|Logan International Dividend ADR
MPI Investment Management|MPI Tax-Free Fixed Income (Muni)
MPI Investment Management|MPI-Fixed
MSCI ACWI Net|MSCI AC World Index Net
MSCI ACWI x US Net|MSCI AC World Index ex US Net
MSCI EAFE Net|MSCI EAFE Net
MSCI Emerging Mkt|MSCI Emerging Markets
MSCI World x US Net|MSCI World ex US Net
NAREIT All Equity|NAREIT All Equity
Northern Trust Asset Management|Northern Trust Large Cap Value EQ
Northern Trust Asset Management|Northern Trust Thematic Equity
Rothschild Asset Management Inc.|Rothschild U.S. Large-Cap Core
RUS 1000 Growth|Russell 1000 Growth
RUS 1000 Value|Russell 1000 Value
RUS 2000 Growth|Russell 2000 Growth
RUS 2000|Russell 2000
RUS 2500|Russell 2500
RUS Mid Cap|Russell Mid Cap
RUS Mid Growth|Russell Mid Cap Growth
RUS Top 200 Value|Russell Top 200 Value
S&P 500|Standard & Poors 500
Sage Advisory Services Ltd. Co.|ACE+ Tactical ETF
Sage Advisory Services Ltd. Co.|Core Plus Tactical ETF
Smith Asset Management Group|Large Cap Focused Growth
Smith Asset Management Group|Small Cap Focused Growth
Smith Group|REIT
SouthernSun Asset Management|SMID Cap
The Boston Company Asset Mgmt. LLC|US Mid Cap Growth Equity
The Boston Company Asset Mgmt. LLC|US Mid Cap Opportunistic Value
Tributary Capital Management|Small Cap Equity
Wasmer - Long Muni|Wasmer - Long Muni
Wasmer - Long Term Taxable|Wasmer - Long Term Taxable
Wasmer Schroeder & Co|Short Term Muni
Wasmer Schroeder & Co|Taxable Short Term
Wasmer Schroeder & Company Inc.|Intermediate Tax-Exempt Fixed Income
Wasmer Schroeder & Company Inc.|Intermediate Taxable Fixed Income
Wasmer Schroeder & Company Inc.|Strategic Tax Exempt Fixed Income
'''
