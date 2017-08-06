# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 14:39:07 2017

@author: Comac
"""

from pandas import Series,DataFrame
import pandas as pd
import sys
import time

datafilepath=input("Input the filepath of the data:\neg:\"c:/data/gss.csv\"\n")
lstcolumns=[]
period=0
outputdf=pd.DataFrame()

def view_bar(num,total):
    rate=num/total
    rate_num=int(rate*100)+1
    r="\r{0}{1}{2}%".format("#"*rate_num," "*(100-rate_num),rate_num)
    sys.stdout.write(r)
    sys.stdout.flush()

try:
    gssdata=pd.read_csv(datafilepath,delimiter=',',nrows=100000)
    datafilename="P-"+datafilepath.split('/')[-1]
    l_rootpath=datafilepath.split('/')[0:-1]
    l_rootpath.append(datafilename)    
    pdatafilepath="/".join(l_rootpath)
    gssdatafna=gssdata.fillna(' ')
    
    lstcolumns=list(gssdatafna.columns)
    
    #find the location of start frames
    firstcolumn=gssdatafna[lstcolumns[1]][gssdatafna[lstcolumns[1]]!=' ']#.astype(float)
    framestartloc=list(firstcolumn.index)
    
    #set the period
    period=len(gssdatafna.columns)-1

    print("processing...")
    
    starttime=time.clock()
              
    for i in range(len(framestartloc)):
        tempdf=gssdatafna[framestartloc[i]:framestartloc[i]+period]
        resultdf=tempdf[0:1].copy()
        #foreach each item in tempdf
        for trow in range(1,len(tempdf)):
            for tcol in range(1,len(tempdf.columns)):
                if tempdf.iloc[trow,tcol]!=' ':
                    resultdf.iloc[0,tcol]=tempdf.iloc[trow,tcol]
        #add some judge here
        outputdf=outputdf.append(resultdf)
        #process bar
        view_bar(i,len(framestartloc))
    
    endtime=time.clock()
    print("\nfor loop used time:{0}".format(endtime-starttime))
    #write file
    starttime=time.clock()
    outputdf.to_csv(pdatafilepath,index=False)
    endtime=time.clock()
    print("\nWrite file successfully.\nLocated in {0}\nTime Used:{1}".format(pdatafilepath,endtime-starttime))
        
except OSError:
    print("Initializing from file failed\nData file does not exist")
    
