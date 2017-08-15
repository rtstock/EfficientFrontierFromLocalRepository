# -*- coding: utf-8 -*-
"""
Created on Tue May 03 14:28:41 2016

@author: Justin.malinchak
"""

import json
from pprint import pprint

with open('data.json') as data_file:    
    data = json.load(data_file)
pprint(data)