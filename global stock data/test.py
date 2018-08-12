import requests
import pandas as pd
import matplotlib.pyplot as plt

symbol='MSFT'#user input
datatype='csv'
apikey='demo'

function='TIME_SERIES_DAILY'
function='TIME_SERIES_WEEKLY'
function='TIME_SERIES_MONTHLY'

function='TIME_SERIES_INTRADAY'
symbol+='&interval=5min' #grouped


url='https://www.alphavantage.co/query?function='+function+'&symbol='+symbol+'&apikey='+apikey+'&datatype='+datatype

csvdata = pd.read_csv(url)



ytemp=[]
xtemp=[]
for row in csvdata.values:
    ytemp.append(row[1])
    xtemp.append(row[0])
    
ytemp.reverse()
xtemp.reverse()
graphsize=10#user input
y=ytemp[:graphsize]
x=xtemp[:graphsize]


x_axis = range(len(x))
plt.xticks(x_axis, x)
plt.plot(x_axis, y)
plt.xlabel('Time Series')
plt.ylabel('Market Value')
plt.show()
