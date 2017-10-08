#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 14:49:53 2017

@author: KingDono
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
from sklearn.svm import SVC
import pandas as pd
from matplotlib import style
import time
import sys

FEATURES =  ['DE Ratio',
             'Trailing P/E',
             'Price/Sales',
             'Price/Book',
             'Profit Margin',
             'Operating Margin',
             'Return on Assets',
             'Return on Equity',
             'Revenue Per Share',
             'Market Cap',
             'Enterprise Value',
             'Forward P/E',
             'PEG Ratio',
             'Enterprise Value/Revenue',
             'Enterprise Value/EBITDA',
             'Revenue',
             'Gross Profit',
             'EBITDA',
             'Net Income Avl to Common ',
             'Diluted EPS',
             'Earnings Growth',
             'Revenue Growth',
             'Total Cash',
             'Total Cash Per Share',
             'Total Debt',
             'Current Ratio',
             'Book Value Per Share',
             'Cash Flow',
             'Beta',
             'Held by Insiders',
             'Held by Institutions',
             'Shares Short (as of',
             'Short Ratio',
             'Short % of Float',
             'Shares Short (prior ']

# all values at 0th row data_df.loc[:0]

#import entire CSV
data_df = pd.DataFrame.from_csv("key_stats.csv")


#train data down to ticker klac
train_data = data_df[:1403]

#test data from kmb to the end of csv
test_data = data_df[1404:]


def trainDataSet():
    X = np.array(train_data[FEATURES].values)
    y = (   train_data["Status"]
            .replace("underperform",0)
            .replace("outperform",1)
            .values.tolist())
    
    X = preprocessing.scale(X)
    
    return X,y

def testDataSet():
    Xtest = np.array(test_data[FEATURES].values)
    ytest = (   test_data["Status"]
                .replace("underperform",0)
                .replace("outperform",1)
                .values.tolist())
    
    Xtest = preprocessing.scale(Xtest)
    
    return Xtest,ytest
    
print()

#gather training data
X, y = trainDataSet();
#Train cpu using linearSVC 
clf = SVC(kernel="linear", verbose=True)
clf.fit(X, y) 

#Gather testing data
Xtest,ytest = testDataSet()
#Gather y[] predictions from testing data
ypred = clf.predict(Xtest)

#errors in data set
errors = np.sum(np.abs(ytest - ypred))
perc_error = errors / np.shape(test_data)[0]

print()
errordata_df = pd.DataFrame
num = 1404
for i in ypred:
    if i == 1:
        prediction = "Buy"
        if (data_df["Status"][num] == 'underperform'):
            print(data_df["Ticker"][num],"\t", data_df["Price"][num],"\t",data_df["Status"][num],"\t", prediction)
    if i == 0:
        prediction = "Sell"
        if (data_df["Status"][num] == 'outperform'):
            print(data_df["Ticker"][num],"\t", data_df["Price"][num],"\t",data_df["Status"][num],"\t", prediction)
        
    
    #print(data_df["Ticker"][num],"\t", data_df["Price"][num],"\t", data_df["Status"][num],"\t", prediction)
    num+=1
#    time.sleep(.09)
    
#sys.exit("Error message")

#plt.figure(1)
#plt.imshow([yPred[:10].transpose(), ytest[:10]])

print("\ntest error: ", perc_error)
print()
