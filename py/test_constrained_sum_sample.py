# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 17:11:54 2016

@author: Justin.malinchak
"""
import pandas as pd 
class go:
    SymbolsList = ''
    def __init__(self,mySymbolsList):
        
        self.SymbolsList = mySymbolsList
        
        
    # Before allowing negatives
    def constrained_sum_sample_pos(self,n, total):
        """Return a randomly chosen list of n positive integers summing to total.
        Each such list is equally likely to occur."""
        import random
        dividers = sorted(random.sample(xrange(1, total), n - 1))
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
    
    def constrained_sum_sample_nonneg(self,n, total):
        """Return a randomly chosen list of n nonnegative integers summing to total.
        Each such list is equally likely to occur."""
        ser =  [x - 1 for x in self.constrained_sum_sample_pos(n, total + n)]
        return ser
        
    
    def randomweightseries(self, 
                     ):
        #mysymbolslist = self.SymbolsList #['WMT','BAC','JPM','AAPL','GOOG']
    
        #int_list = constrained_sum_sample_pos(len(self.SymbolsList),100) 
        #print 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww'
        numtest = 0
        
        while 1:
            numtest += 1
            testfail = False
            int_list = self.constrained_sum_sample_nonneg(len(self.SymbolsList),100) 
            
            fractions_list = [float(x)/float(100) for x in int_list]
            
            #sums them all to test
            #t = reduce(lambda x,y:x+y,s)
            
            fractions_series = pd.Series(fractions_list, index=self.SymbolsList)
            i = 0
            #print fractions_series
            for alpha in fractions_series.index:
                if fractions_series[alpha] > self.SymbolsList[alpha]:
                    #print 'no good'
                    testfail = True
                    #print fractions_series[alpha]
                i += 1
            if testfail == False:
                break
            if numtest > 100:
                print 'hit 100'
                break
        print 'numtest',numtest        
        print fractions_series
        return fractions_series



if __name__=='__main__':
#    
#    o = perform(['^GSPC','^DJI','^OEX','^RUT']
#                ,  startdate_string = '2012-12-31'
#                ,  enddate_string = ''#'2013-12-31'
#                ,  period='daily'
#                ,  pctchangeorlogreturn = 'pctchange'
#                ,  source='Yahoo') 
                
                
    o = go(mySymbolsList={'a':0.5,'b':0.5,'c':0.50,'d':0.5})
    for i in range(100):
        rws = o.randomweightseries()
        #print rws