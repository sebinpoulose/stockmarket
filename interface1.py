from appJar import gui
import requests
import pandas as pd
import matplotlib.pyplot as plt


key='demo'
datatype='csv'


def toolbar(btn):
    pass
    #print(btn)
    #if btn == "LOGOUT": logout()
    #elif btn == "FILL": app.setTabBg("Tabs", app.getTabbedFrameSelectedTab("Tabs"), app.colourBox())
    #elif btn == "PIE-CHART": app.showSubWindow("Statistics")
    #elif btn == "CALENDAR": app.showSubWindow("DatePicker")
    #elif btn == "ADDRESS-BOOK": app.showSubWindow("AddressBook")
    #elif btn == "MAP": app.showSubWindow("Maps")
    #elif btn == "ACCESS": app.showAccess()
    #elif btn == "EXIT": app.stop()

    
def press(btn):
    optedsymbol=app.getEntry("SYMBOL OF THE EQUITY : ")
    optedgraphsize=app.getEntry("NO OF DATA POINTS : ")
    if(optedgraphsize==''):
        optedgraphsize=None
    else:
        optedgraphsize=int(optedgraphsize)
    optedfunction=app.getOptionBox("function")
    if(optedfunction=="DAILY"):
        optedfunction='TIME_SERIES_DAILY'
    elif(optedfunction=="WEEKLY"):
        optedfunction='TIME_SERIES_WEEKLY'
    elif(optedfunction=="MONTHLY"):
        optedfunction='TIME_SERIES_MONTHLY'
    else:
        optedfunction='TIME_SERIES_INTRADAY'
        optedsymbol+='&interval=5min'
    #url generation
    url='https://www.alphavantage.co/query?function='+optedfunction+'&symbol='+optedsymbol+'&apikey='+key+'&datatype='+datatype
    
    ############################################################
    try:
        csvdata = pd.read_csv(url)
        ytemp=[]
        xtemp=[]
        for row in csvdata.values:
            ytemp.append(row[1])
            xtemp.append(row[0])
    except:
        print 'error, check the symbol '
        return

        
    y=ytemp[0:optedgraphsize]
    x=xtemp[0:optedgraphsize]

    y.reverse()
    x.reverse()

    x_axis = range(len(x))
    plt.xticks(x_axis, x)
    plt.plot(x_axis, y)
    plt.xlabel('Time Stamp')
    plt.ylabel('Values')
    plt.show()
    ############################################################

app = gui('unnamed',"1000x650")

app.addToolbar(["TEMP1", "TEMP2", "TEMP3", "TEMP4", "TEMP5", "TEMP6", "TEMP7","EXIT"], toolbar, findIcon=True)

app.addLabel("u","PROGRAM NAME")
app.addLabelEntry("SYMBOL OF THE EQUITY : ",1,0)
app.addLabelEntry("NO OF DATA POINTS : ",1,1)
app.addLabel("y","TIME SERIES : ",1,2)
app.addOptionBox("function", ["DAILY", "WEEKLY", "MONTHLY", "INTRADAY"],1,3)


app.addButtons(["Submit"], press,2)


app.go()
