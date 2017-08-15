# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 15:51:18 2016

@author: Justin.malinchak
"""

import json    # or `import simplejson as json` if on Python < 2.6

json_string = '{ "a":["123456789", "aaa","bbbb"],"b":["1111","222","3333"] }'
obj = json.loads(json_string)    # obj now contains a dict of the data
print obj