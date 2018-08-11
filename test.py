import json
import requests
import pandas as pd
import matplotlib.pyplot as plt


url_csv="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo&datatype=csv"

pd_data = pd.read_csv(url_csv)
print(pd_data.values)
y=[]
x=[]
for i in pd_data.values:
    y.append(i[1])
    x.append(i[0])
    
y.reverse()
x.reverse()


x_axis = range(len(x))
plt.xticks(x_axis, x)
plt.plot(x_axis, y)
plt.xlabel('Time Stamp')
plt.ylabel('Values')
plt.show()
