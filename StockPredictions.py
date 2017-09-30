# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import os
import time
from datetime import datetime

#obtains path of intraQuater folder holding s&p 500 stock data html files
#via yahoo finance
path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(os.getcwd(), 'data')


#method gathers total debt to equity ratio from
#/intraQuarter/_KeyStats/(stock ticker)/#year$month#day#timecreated.html
def KeyStats(gather="Total Debt/Equity (mrq)"):
    statsPath = path + '/_KeyStats'
    #stockLists contains the path stats path followed by /(ticker symbol)
    stockLists = [x[0] for x in os.walk(statsPath)]
    totalfiles = 0
    totalerrors = 0
    df = pd.DataFrame(columns = {'Date','Unix','Ticker','Ratio'})
    #loops through each stock directory
    for eachdir in stockLists [1:]:
        #eachfile contains an array of the html source in a given folder
        eachfile = os.listdir(eachdir)
        #print(eachdir)
        ticker = eachdir.split("_KeyStats/")[1]
        #time.sleep(2)
        
        #if directory contains anything
        if len(eachfile) > 0:
            for file in eachfile:
                totalfiles+=1
                #extracts date and timestamp from filename
                #e.g 20040130190102.html
                #2004-01-30 19:01:02 1075507262.0
                #creates a unix timestamp
                datestamp = datetime.strptime(file,'%Y%m%d%H%M%S.html')
                unixtime = time.mktime(datestamp.timetuple())
                #print(datestamp,unixtime)
                
                #outputs full path of file, ticker and mrq
                #skips files if error in reading source code
                fullPath = eachdir+'/'+file
                #print(fullPath)
                try:
                    source = open(fullPath,'r').read()
                    #print(source)
                    value = source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]           
                    print(ticker+":",value);    
                except Exception as e:
                    totalerrors+=1
                    continue
                
#    print(totalfiles)
#    print(totalerrors)
#    print(totalerrors/totalfiles)
KeyStats()