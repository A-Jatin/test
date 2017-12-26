# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 22:18:50 2017

@author: JATIN
"""
import zipfile
import pandas as pd
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse

def sec_dataframe():
    #Set variable for page to be open and url to be concatenated 
    url = "https://www.sec.gov"
    page = urllib.request.urlopen('https://www.sec.gov/help/foiadocsinvafoiahtm.html')
    
    #File extension to be looked for. 
    extension = ".zip"
    
    #Use BeautifulSoup to clean up the page
    soup = BeautifulSoup(page)
    soup.prettify()
    zipfiles=[]
    #Find all the links on the page that end in .zip
    for anchor in soup.findAll('a', href=True):
        links = url + anchor['href']
        if links.endswith(extension):
            zipfiles.append(links)
    
    dates=[]
    for line in zipfiles:
        if (line[-10:-4]=='exempt'):
            year='20'+line[-13:-11]
            day=line[-15:-13]
            month=line[-17:-15]
        elif (line[-12:-6]=='exempt'):
            year='20'+line[-15:-13]
            month=line[-19:-17]
            day=line[-17:-15]
        elif (line[-6]=='_'):
            year='20'+line[-8:-6]
            day=line[-10:-8]
            month=line[-12:-10]
        else:
            year='20'+line[-6:-4]
            day=line[-8:-6]
            month=line[-10:-8]
        dates.append(year+'-'+month+'-'+day)
    Type=[]
    for line in zipfiles:
        if (line[-10:-4]=='exempt' or line[-12:-6]=='exempt'):
            Type.append('exempt')
        else:
            Type.append('non-exempt')
    global df
    df=pd.DataFrame(zipfiles)
    df.columns=['File_URL']
    Date = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
    df['Date']=Date
    df['Type']=Type
    
sec_dataframe()    

def get_sec_zip_by_period(period,is_exempt=bool,only_most_recent=bool):
    if(is_exempt is True):
        is_exempt='exempt'
    else:
        is_exempt='non-exempt'
    zips=[]
    zips_date=[]
    for i in df:
        if((i['Date'] in period) and i['Type']==is_exempt):
            zips.append(i['File_URL'])
            zips_date.append(i['Date'])
    zips=pd.DataFrame(zips)
    zips['Date']=zips_date
    if(only_most_recent):
        recent=max(zips['Date']).iloc
        recent=zips[0][recent]
        return zipfile.Zipfile(recent,'r')
    return zipfile.ZipFile(zips[0],'r')
            