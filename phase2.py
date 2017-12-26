# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:35:20 2017

@author: JATIN
"""

import json
import pandas as pd
import urllib.request


#phase 2
page=urllib.request.urlopen('https://doppler.finra.org/doppler-lookup/api/v1/search/firms?hl=true&nrows=99000&query=Blackstone&r=2500&wt=json')
jsondata=json.load(page)
jsondata=jsondata['results']['BROKER_CHECK_FIRM']['results'] 
AUM=[]
for i in jsondata:    
     if((i['fields']['bc_firm_name'] is 'BLACKSTONE' or 'BREP') and (i['fields']['score']>0.4)):
          AUM.append(i['fields'])
AUM=pd.DataFrame(AUM)       
AUM=AUM[['bc_firm_name','bc_source_id']]
