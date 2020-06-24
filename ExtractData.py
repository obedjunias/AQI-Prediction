# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:28:07 2020

@author: Obed Junias
"""
from Plotting import avg_data
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys
import csv
import os

def scrape_data(month,year):
    html_file = open("Data/htmlData/{}/{}.html".format(year,month),"rb")
    file_data = html_file.read()
    tempData = []
    finalData = []
    soup = BeautifulSoup(file_data,'lxml')
    for table in soup.findAll("table",{'class':'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                tempData.append(a)
    rows = len(tempData)/15
    
    for times in range(round(rows)):
        newtempD = []
        for i in range(15):
            newtempD.append(tempData[0])
            tempData.pop(0)
        finalData.append(newtempD)

    length = len(finalData)

    finalData.pop(length - 1)
    finalData.pop(0)

    for a in range(len(finalData)):
        finalData[a].pop(6)
        finalData[a].pop(13)
        finalData[a].pop(12)
        finalData[a].pop(11)
        finalData[a].pop(10)
        finalData[a].pop(9)
        finalData[a].pop(0)

    return finalData

def combine_data(year,cs):
    for a in pd.read_csv('Data/realData/' + year + '.csv',chunksize=600):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist

if __name__ == "__main__":
    if not os.path.exists("Data/realData"):
        os.makedirs("Data/realData")
    years = ["2013","2014","2015","2016"]
    pm = getattr(sys.modules[__name__], 'avg_data')(years)
    for key, value in pm.items():
            if len(value) == 364:
                pm[key].insert(364,'-')
    for year in years:
        final_data = []
        with open('Data/realData/' + year + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1, 13):
            temp = scrape_data(str(month), year)
            final_data = final_data + temp

        for i in range(len(final_data)-1):
            final_data[i].insert(8, pm[year][i])
            # print(final_data[0])
            
        with open('Data/realData/' + year + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
    combineddata = []
    for year in years:
        combineddata.extend(combine_data(year,600))
        
    with open('Data/realData/CombinedData.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(combineddata)
        
        
df=pd.read_csv('Data/realData/CombinedData.csv')