from appJar import gui
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# tosymbol equates to market.

key='demo'
datatype='csv'
url="https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_INTRADAY&symbol=BTC&market=EUR&apikey=demo&datatype=csv"


def press(btn):
    fromsymbol=app.getEntry("CRYPTO-CURRENCY SYMBOL : ")
    tosymbol=app.getEntry("EXCHANGE MARKET SYMBOL : ")
    optedgraphsize=app.getEntry('NUMBER OF DATA POINTS : ')
    if(optedgraphsize==''):
        optedgraphsize=None
    else:
        optedgraphsize=int(optedgraphsize)
        
    if(fromsymbol=='' or tosymbol==''):
        app.errorBox("error","symbol of currrency must not be blank")
        return
    else:
        optedfunction=app.getOptionBox("function")
        if(optedfunction=="DAILY"):
            optedfunction='DIGITAL_CURRENCY_DAILY'
        elif(optedfunction=="WEEKLY"):
            optedfunction='DIGITAL_CURRENCY_WEEKLY'
        elif(optedfunction=="MONTHLY"):
            optedfunction='DIGITAL_CURRENCY_MONTHLY'
        else:
            optedfunction='DIGITAL_CURRENCY_INTRADAY'                          
        
        url="https://www.alphavantage.co/query?function="+optedfunction+"&symbol="+fromsymbol+"&market="+tosymbol+"&apikey="+key+"&datatype="+datatype

        try:
            csvdata = pd.read_csv(url)
            ytemp=[]
            xtemp=[]
            for row in csvdata.values:
                ytemp.append(row[1])
                xtemp.append(row[0])
        except:
            app.errorBox("error","symbol of currency is incorrect !")
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
                filename=app.saveBox(title=None, fileName=fromsymbol+"_to_"+tosymbol, dirName=None, fileExt=".csv", fileTypes=None, asFile=None)
                csvdata.to_csv(filename)
            except:
                pass
        elif(btn=='Save to Database'): 
            try:
                con = sqlite3.connect('db.sqlite')
                filename=app.saveBox(title=None, fileName=fromsymbol+"_to_"+tosymbol, dirName=None, fileExt=None, fileTypes=None, asFile=None)
                a=filename.split('/')
                filename=a[-1]
                csvdata.to_sql(filename, con)
            except:
                app.errorBox("Error","Database entry failed !")
                return


app = gui('unnamed',"600x600")
app.setFont(18)
app.setBg("grey")

app.addLabelEntry("CRYPTO-CURRENCY SYMBOL : ",1,0)
app.addLabelEntry("EXCHANGE MARKET SYMBOL : ",2,0)
app.addLabelEntry("NUMBER OF DATA POINTS : ",3,0)
app.addLabel("y","TIME SERIES : ",4,0)
app.addOptionBox("function", ["DAILY", "WEEKLY", "MONTHLY", "INTRADAY"],5,0)
app.addButtons(["View Graph","Save to Database","Save as Excel"], press,6,0)

app.go()
