#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 14:49:53 2017

@authors: Donovan Colton
          Faisal Almansour
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
from sklearn import svm, preprocessing,datasets
from sklearn.svm import SVC
import pandas as pd
import time
from mpl_toolkits.mplot3d import Axes3D

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

# all values 0th row:    data_df.loc[:0]

#import entire CSV
data_df = pd.DataFrame.from_csv("key_stats.csv")

#train data down to ticker klac
train_data = data_df[:1403]

#test data from kmb to the end of csv
test_data = data_df[1404:]

tdp = plt2.figure().add_subplot(111, projection='3d')

def createDataSet(d):
    Xtest = np.array(d[FEATURES].values)
    ytest = (   d["Status"]
                .replace("underperform",0)
                .replace("outperform",1)
                .values.tolist())
    Xtest = preprocessing.scale(Xtest)
    return Xtest,ytest
print()

#gather training data
X, y = createDataSet(train_data);
                    
#Train cpu using linearSVC 
clf = SVC(kernel="rbf", verbose=True)
clf.fit(X, y) 

#Gather testing data
#1260 values in test
Xtest,ytest = createDataSet(test_data)
#Gather y[] predictions from testing data
ypred = clf.predict(Xtest)

#errors in data set
errors = np.sum(np.abs(ytest - ypred))
perc_error = errors / np.shape(test_data)[0]

print()

csvnum = 1404
num = 0

for i in ypred:
    if i == 1:
        prediction = "Buy"
        if (data_df["Status"][csvnum] == 'underperform'):
            print(data_df["Ticker"][csvnum],"\t", data_df["Price"][csvnum],"\t",data_df["Status"][csvnum],"\t", prediction)
            #add errors into a new numpy array?
            tdp.scatter(data_df["DE Ratio"][csvnum], data_df["Profit Margin"][csvnum], data_df["Price"][csvnum], c='r', marker='o')
            
    elif i == 0:
        prediction = "Sell"
        if (data_df["Status"][csvnum] == 'outperform'):
            print(data_df["Ticker"][csvnum],"\t", data_df["Price"][csvnum],"\t",data_df["Status"][csvnum],"\t", prediction)
            tdp.scatter(data_df["DE Ratio"][csvnum], data_df["Profit Margin"][csvnum], data_df["Price"][csvnum], c='r', marker='o')     
   
    #print all tickers along w predictions
    #print(data_df["Ticker"][csvnum],"\t", data_df["Price"][csvnum],"\t", data_df["Status"][csvnum],"\t", prediction)
    csvnum+=1
    num+=1

tdp.set_xlabel('DE Ratio')
tdp.set_ylabel('Profit Margin')
tdp.set_zlabel('Price')

plt.show()

nr_to_show = 1500
#purple = good
plt.figure(1)
plt.imshow(np.array([np.abs(ypred[:nr_to_show] - ytest[:nr_to_show])]), aspect='auto')

print("\ntest error: ", perc_error)
print()
