# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:50:17 2020

@author: Obed Junias
"""

import os
import sys
import time
import requests


def retrieve_page():
    for year in range(2013,2019):
        for month in range(1,13):
            if month < 10:
                url = "https://en.tutiempo.net/climate/0{}-{}/ws-432950.html".format(month,year)
            else:
                url = "https://en.tutiempo.net/climate/{}-{}/ws-432950.html".format(month,year) 
            
            data = requests.get(url)
            encoded_data = data.text.encode('utf-8')
            
            
            if not os.path.exists("Data/htmlData/{}".format(year)):
                os.makedirs("Data/htmlData/{}".format(year))
            
            with open("Data/htmlData/{}/{}.html".format(year,month),"wb") as op:
                op.write(encoded_data)
        
        
        sys.stdout.flush()
        
        
if __name__ == "__main__":
    start_time = time.time()
    retrieve_page()
    stop_time = time.time()
    print("Time Taken: {}".format((stop_time-start_time)))
    