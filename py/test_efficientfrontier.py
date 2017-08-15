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


import outputefficientfrontier as oef
#               # Use this one to test Yahoo
#    o = output(      list_of_symbols = ['WMT','NKE','T','MCD','JPM','^RUT'] 
#                     ,  startdate_string = '2014-12-31'
#                     ,  enddate_string = '2016-03-31'
#                     ,  period = 'monthly'
#                     ,  pctchangeorlogreturn = 'pctchange'
#                     ,  source = 'Yahoo'
#              )

o = oef.output(['Mellon Capital Large Cap Core','Boston Co US Mid Cap Growt','Harding Loevner Glob Eq ADR','Logan Capital Concentrated Val']
            ,  startdate_string = '2012-12-31'
            ,  enddate_string = '2016-03-31' #'2013-12-31'
            ,  period='Monthly'
            ,  pctchangeorlogreturn = 'pctchange'
            ,  source='local'
            ) 