from appJar import gui
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


key='demo'
datatype='csv'


def toolbar(btn):
    #print(btn)
    #if btn == "LOGOUT": logout()
    #elif btn == "FILL": app.setTabBg("Tabs", app.getTabbedFrameSelectedTab("Tabs"), app.colourBox())
    #elif btn == "PIE-CHART": app.showSubWindow("Statistics")
    #elif btn == "CALENDAR": app.showSubWindow("DatePicker")
    #elif btn == "ADDRESS-BOOK": app.showSubWindow("AddressBook")
    #elif btn == "MAP": app.showSubWindow("Maps")
    if btn == "SETTINGS": pass
    elif btn == "EXIT": app.stop()

    
def press(btn):
    optedsymbol=app.getEntry("SYMBOL OF THE EQUITY : ")
    if(optedsymbol==''):
        app.errorBox("error","symbol of equity must not be blank")
        return
        
    optedgraphsize=app.getEntry("NO  OF   DATA  POINTS   : ")
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
        app.errorBox("error","symbol of equity is incorrect !")
        return

    if(btn=='View Graph'):
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
    elif(btn=='Save as Excel'):
        try:            
            filename=app.saveBox(title=None, fileName=optedsymbol, dirName=None, fileExt=".csv", fileTypes=None, asFile=None)
            csvdata.to_csv(filename)
        except:
            pass
    elif(btn=='Save to Database'):  ################     under    test
        try:
            con = sqlite3.connect('db.sqlite')
            filename=app.saveBox(title=None, fileName=optedsymbol, dirName=None, fileExt=None, fileTypes=None, asFile=None)
            a=filename.split('/')
            filename=a[-1]
            csvdata.to_sql(filename, con)
        except:
            print "error sql convertion"
            return

app = gui('unnamed',"600x600")
app.setFont(18)
app.setBg("grey")

app.addToolbar(["TEMP1", "TEMP2", "TEMP3", "TEMP4", "TEMP5", "TEMP6", "SETTINGS","EXIT"], toolbar, findIcon=True)
app.addStatusbar(header="STATUS ",fields=1, side="RIGHT")
app.setStatusbarWidth(20, field=0)
app.setStatusbar("ready", field=0)

app.addLabelEntry("SYMBOL OF THE EQUITY : ",1,0)
app.addLabelEntry("NO  OF   DATA  POINTS   : ",2,0)
app.addLabel("y","TIME SERIES : ",3,0)
app.addOptionBox("function", ["DAILY", "WEEKLY", "MONTHLY", "INTRADAY"],4,0)
app.addButtons(["View Graph","Save to Database","Save as Excel"], press,5,0)
app.go()
