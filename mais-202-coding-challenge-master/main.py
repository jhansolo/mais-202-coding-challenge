# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 17:50:16 2018

@author: jh

MAIS 202 Application Coding Challenge-extracting and calculating average loan interest rates 
according to loan purposes

Uses pandas to read csv data, identify unique loan purposes, create temporary dataframe views
according to purposes instances, tally up mean valus of the interest column, and collects the 
result in a separate pandas Series object.

Plotting of the bar graph was simply through the built-in bar graph function of the pandas Series
Plotting the table was more involved and was achieved with matplotlib.

Good exercise in using gridspec from matplotlib for laying out different shaped subplots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


"""parsing the csv data with pandas"""

loadPath=r"data.csv"
data=pd.read_csv(loadPath)
data=data.set_index("purpose")          #setting the purpose column as the dataframe index
purpose=(data.index.unique())           #find unique instances within the purpose entries
sortKey=np.argsort(purpose)             #alphabetical sorting, not necessary, but useful
purpose=purpose[sortKey]                #implement alphabetical sorting

average=[]                              #declare empty array for appending average interest of each purpose
                                        #more efficient to convert this list later to pd Series rather than Series right away

"""tallying the average interest rate for each purpose"""
for i in purpose:
    tempFrameView=data.loc[i]           #temporary view of the dataframe with only rows corrsponding to a particular instance in the purpose list
    mean_int=tempFrameView["int_rate"].mean()   #talling up the mean interest rate for that purpose
    average.append(mean_int)                    #append onto the average list

average=pd.Series(average)              #convert python list to pandas Series
average.set_axis(purpose,inplace=True)  #set Series axis to the list of purposes


"""prepping to plot the bar graph and table"""
gs=gridspec.GridSpec(4,10, wspace=5)               #3x6 subplots layout

axGraph=plt.subplot(gs[0:3,0:7])         #allocating subplot spans for the bar graph
axTable=plt.subplot(gs[0:1,9:10])          #allocating subplot spans for the table
axTable.set_axis_off()                  #no need for axis on the table subplot

average=average.round(decimals=2)       #round to 2 decimals for interest rate


"""plotting the bar graph, easy"""
average.plot(                           #using pandas Series built-in plotting
            kind='bar',
            ax=axGraph,
            title='Average Interest Rate vs Purpose of Loan')


"""plotting the output table, long"""
interest=[]                             #container for holding the str values of the interests
row=[]                                  #container for holding the corresponding purposes of each interest
for i in range(len(average.values)):    #reading each interest and purpose value from the Series object to the plain Python lists
    temp1=[]
    temp2=[]
    temp1.append(str(average.values[i]))
    interest.append(temp1)
    temp2.append(str(average.index[i]))
    row.append(temp2)
label=["average interest"]              #table title
axTable.table(cellText=interest,rowLabels=row,colLabels=label,cellLoc='center',colWidths=[10]) #matplotlib table in the subplot
plt.show()


