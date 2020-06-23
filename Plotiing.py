# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:56:25 2020

@author: Taurus
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def avg_data(years):
    
    completeData = {}
    for year in years:
        average = []
        for rows in pd.read_csv("Data/AQI/aqi{}.csv".format(year),chunksize=24):
            s = 0
            avg = 0.0
            data = []
            df = pd.DataFrame(rows)
            for index, row in df.iterrows():
                data.append(row["PM2.5"])
            for i in data:
                if type(i) is float or type(i) is int:
                    s+=i
                elif type(i) is str:
                    if i != "NoData" and i != "PwrFail" and i!= "---" and i!="InVld":
                        temp  = float(i)
                        s += temp
            avg = s/24
            average.append(avg)
            
        completeData[year] = average
    return completeData
            
        
if __name__ == "__main__":
    years = ["2013","2014","2015","2016","2017","2018"]
    data = avg_data(years)
    for year in years:
        plt.plot(range(0,len(data[year])),data[year],label=year)
        

    plt.xlabel('Day')
    plt.ylabel('PM 2.5')
    plt.legend(loc='upper right',mode = "expand", ncol = 5)
    plt.show()