# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 17:27:27 2016

@author: Justin.malinchak
"""



if __name__ == "__main__":
    import sys
    print '-----------------------'

    json_string_of_symbols_and_weights = sys.argv[1]
    print '---------------------------------------'
    print json_string_of_symbols_and_weights
    print '---------------------------------------'
    #import ast
    #json_string_of_symbols_and_weights_eval = ast.literal_eval(json_string_of_symbols_and_weights)
    #import urllib
    #json_string_of_symbols_and_weights_unquoted = urllib.unquote(json_string_of_symbols_and_weights)
    #print 'json_string_of_symbols_and_weights_unquoted',json_string_of_symbols_and_weights_unquoted
    startdate_string = sys.argv[2]
    print 'startdate_string', startdate_string
    enddate_string = sys.argv[3]
    print 'enddate_string',enddate_string
    period = sys.argv[4]
    print 'period', period
    
    pctchangeorlogreturn = sys.argv[5]
    print 'pctchangeorlogreturn',pctchangeorlogreturn
    source = sys.argv[6]
    print 'source', source
    permutations = sys.argv[7]
    print 'permutations', permutations

    import outputefficientfrontier as oef
    oef.output(json_string_of_symbols_and_weights=json_string_of_symbols_and_weights
                ,startdate_string=startdate_string
                ,enddate_string=enddate_string
                ,period=period
                ,pctchangeorlogreturn=pctchangeorlogreturn
                ,source=source
            )
    print oef.drawsail(permutations,0.92)

#
#    json_string = '{"Granite Partners Small Core Plus":[0.5,0.2],"Harding Loevner Glob Eq ADR":[0.5,0.1],"Logan Capital Concentrated Val":[0.5,0.1],"Hilton Capital YP":[0.4,0.05]}'
#    #mySymbolsDict = json.loads(json_string)    # obj now contains a dict of the data
#    #print mySymbolsDict
#    import outputefficientfrontier
#    o = outputefficientfrontier.output(    json_string
#                ,  startdate_string = '2013-12-31'
#                ,  enddate_string = '2016-03-31' #'2013-12-31'
#                ,  period='Monthly'
#                ,  pctchangeorlogreturn = 'pctchange'
#                ,  source='local'
#                ) 
#
#    print o.drawsail(1000,0.92)