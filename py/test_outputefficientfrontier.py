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

o = oef.output(['Hilton Capital YP','Blue Shores Cap GLSE']
            ,  startdate_string = '2012-12-31'
            ,  enddate_string = '2016-03-31' #'2013-12-31'
            ,  period='Monthly'
            ,  pctchangeorlogreturn = 'pctchange'
            ,  source='local'
            ) 
            
print o.EfficientFrontierObject.correlationmatrix()
print o.EfficientFrontierObject.covariancematrix
print o.EfficientFrontierObject.ReturnsDataframe
#print ' ---- here is just one random weight Series... ----'
#print o.EfficientFrontierObject.portfolioriskreturnrandomweight()
print o.drawsail(5000,0.90)


'''
1919 Inv Csl Institutional Eq
1919 Inv Csl SRI SRI Equity
1919 Inv Csl SRI SRI Growth Eq
1919 Inv Csl SRI SRI Intl ADR EQ
AMI Asset Mgmt Large Cap Growth
AMI Asset Mgmt Small Cap Growth
Barclays 1-3Y Gv/Crd&
Barclays 5Y Muni&
Barclays Aggregate&
Barclays Govt/Credit&
Barclays Int Gv/Crd&
Barclays LTGv/Crd&
Blue Shores Cap GLSE
Boston Co Mid Cap Opport
Boston Co US Mid Cap Growt
Carl Domino Inc Large Cap Value
Crawford Invt Dividend Growth
Crawford Invt Dividend GrwthMA
Crawford Invt Dividend Yield
Crawford Invt Nat Int Muni Bd
Cumberland Adv Fixed & Cash Por
Cumberland Adv GLB Traded Funds
Cumberland Adv Intn'l ETFs
Cumberland Adv Muni Bds Tot Ret
Cumberland Adv Xch Traded Funds
Cyrus J Lawrence CJL Equity
Eaton Vance TABS Lad1020 MA
Eaton Vance TABS Ladd-Inter
Eaton Vance TABS Ladd-Long
Eaton Vance TABS Ladd-Short
Eaton Vance TABS Limited
Granite Partners Small Core
Granite Partners Small Core Plus
Harding Loevner Glob Eq ADR
Harding Loevner Intl Equity ADR
Hays Advisory Global ETF
Hays Advisory Int'l ETF
Hays Advisory Long Term Growth
Hilton Capital YP
J Hancock Invt JH FLCC
John Hancock AM Fndmtl LCC NW
John Hancock AM Intl ValADR Wrap
John Hancock AM Sov Div Perf NW
John Hancock AM Sov Div Perf Wr
Logan Capital Concentrated Val
Logan Capital Int'l ADR
Logan Capital Logan Core 60/40
Logan Capital Logan Growth
Mellon Capital Large Cap Core
Mellon Capital Mid Cap Core
MPI Investment MPI-Fixed
MPI Investment Tax Free Fi Muni
MSCI EAFE Net&
MSCI Emerging Mkt&
NT Asset Mgmt Balanced
NT Asset Mgmt NT Value Equity
NT Asset Mgmt NTTE
RETURNS MONTHLY&
Rothschild Asset RAM Large-Cap C
Rothschild Asset RAM LC Value
RUS 2000&
S&P 100&
S&P 400 Mid Cap&
S&P 500&
Sage Advisory ACE+ Tact ETF
Sage Advisory Core Agg Fixed
Sage Advisory Mod Gr Tact ETF
Smith Asset LgCpFocusedGr
Smith Asset SmCpFocusedGr
SouthernSun SMID Cap
Tributary Cap Small Cap Equity
WasmerSchroeder Int. Tax Exempt
WasmerSchroeder Int. Taxable
WasmerSchroeder Strategic Tax Ex
'''