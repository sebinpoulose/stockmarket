from appJar import gui
import requests
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import json
import pickle
import os

#############################################################################################################

key=''
key='demo'
datatype='csv'
with open('filename.pickle', 'rb') as handle:
    settingsfile = pickle.load(handle)
base=settingsfile['currentdatabase']
conn = sqlite3.connect(base)
cur = conn.cursor()
global graphtype
graphtype=settingsfile['graphtype']

#############################################################################################################

def toolbar(btn):
    if btn == "Exit": app.stop()
    elif btn=='About': app.showSubWindow("About")
    elif btn == "Full Screen":
        if app.exitFullscreen():
            app.setGeometry("600x600")
        else:
            app.setGeometry("fullscreen")
            
#############################################################################################################

def globalstockdata(btn):
    optedsymbol=app.getEntry("SYMBOL  OF  THE  EQUITY : ")
    if(optedsymbol==''):
        app.errorBox("Error","symbol of equity must not be blank")
        return        
    optedgraphsize=app.getEntry("NUMBER OF DATA POINTS : ")
    if(optedgraphsize==''):
        optedgraphsize=None
    else:
        optedgraphsize=int(optedgraphsize)
    optedfunction=app.getOptionBox("functionpane1")
    if(optedfunction=="DAILY"):
        optedfunction='TIME_SERIES_DAILY'
    elif(optedfunction=="WEEKLY"):
        optedfunction='TIME_SERIES_WEEKLY'
    elif(optedfunction=="MONTHLY"):
        optedfunction='TIME_SERIES_MONTHLY'
    else:
        optedfunction='TIME_SERIES_INTRADAY'
        optedsymbol+='&interval=5min'
    url='https://www.alphavantage.co/query?function='+optedfunction+'&symbol='+optedsymbol+'&apikey='+key+'&datatype='+datatype        
    try:
        csvdata = pd.read_csv(url)
        ytemp=[]
        xtemp=[]
        for row in csvdata.values:
            ytemp.append(row[1])
            xtemp.append(row[0])
    except:
        app.errorBox("Error","Symbol of equity is incorrect !")
        return
    if(btn=='View Graph'):
        y=ytemp[0:optedgraphsize]
        x=xtemp[0:optedgraphsize]
        y.reverse()
        x.reverse()
        x_axis = range(len(x))
        plt.xticks(x_axis, x)
        plt.plot(x_axis, y,graphtype)
        plt.xlabel('Time Stamp')
        plt.ylabel('Values')
        plt.show()        
    elif(btn=='Save as Excel'):
        try:            
            filename=app.saveBox(title=None, fileName=optedsymbol, dirName=None, fileExt=".csv", fileTypes=None, asFile=None)
            csvdata.to_csv(filename)
        except:
            pass
    elif(btn=='Save to Database'):  
        try:
            filename=app.saveBox(title=None, fileName=optedsymbol, dirName=None, fileExt=None, fileTypes=None, asFile=None)
            a=filename.split('/')
            filename=a[-1]
            csvdata.to_sql(filename, conn)
        except:
            app.errorBox("Error","Database entry failed !")
            return
##############################################################################################################

def exchange(btn):
    fromsymbol=app.getEntry("FROM : ")
    tosymbol=app.getEntry("TO : ")
    optedgraphsize=app.getEntry("NUMBER OF DATA POINTS - ")
    if(optedgraphsize==''):
        optedgraphsize=None
    else:
        optedgraphsize=int(optedgraphsize)            
    if(fromsymbol=='' or tosymbol==''):
        app.errorBox("error","symbol of currrency must not be blank")
        return
    elif(btn=='Get Exchange Rate'):
        url="https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency="+fromsymbol+"&to_currency="+tosymbol+"&apikey="+key        
        try:
            jsonfile = json.loads(requests.get(url).text)
            curcode= jsonfile['Realtime Currency Exchange Rate']['1. From_Currency Code']
            curname= jsonfile['Realtime Currency Exchange Rate']['2. From_Currency Name']
            curname+=" ("+curcode+")"
            toname= jsonfile['Realtime Currency Exchange Rate']['4. To_Currency Name']
            tocode= jsonfile['Realtime Currency Exchange Rate']['3. To_Currency Code']
            toname+=" ("+tocode+")"
            rate= jsonfile['Realtime Currency Exchange Rate']['5. Exchange Rate']
            refresh= jsonfile['Realtime Currency Exchange Rate']['6. Last Refreshed']
            timezone= jsonfile['Realtime Currency Exchange Rate']['7. Time Zone']
            try:
                app.setLabel("l3",curname+" to "+toname)
                app.setLabel("l4","Exchange rate : "+rate)
                app.setLabel("l5","Last refreshed : "+refresh)
                app.setLabel("l6","Time Zone : "+timezone)
                app.showSubWindow("Exchange Rates")
            except:
                pass
        except:
            app.errorBox("Error","Invalid symbol of currency")        
        return
    else:
        optedfunction=app.getOptionBox("functionpane2")
        if(optedfunction=="DAILY"):
            optedfunction='FX_DAILY'
        elif(optedfunction=="WEEKLY"):
            optedfunction='FX_WEEKLY'
        elif(optedfunction=="MONTHLY"):
            optedfunction='FX_MONTHLY'
        else:
            optedfunction='FX_INTRADAY'
            tosymbol+='&interval=5min'        
        url="https://www.alphavantage.co/query?function="+optedfunction+"&from_symbol="+fromsymbol+"&to_symbol="+tosymbol+"&apikey="+key+"&datatype="+datatype
        try:
            csvdata = pd.read_csv(url)
            ytemp=[]
            xtemp=[]
            for row in csvdata.values:
                ytemp.append(row[1])
                xtemp.append(row[0])
        except:
            app.errorBox("Error","symbol of currency is incorrect !")
            return
        if(btn=='Visualize'):
            y=ytemp[0:optedgraphsize]
            x=xtemp[0:optedgraphsize]
            y.reverse()
            x.reverse()
            x_axis = range(len(x))
            plt.xticks(x_axis, x)
            plt.plot(x_axis,y,graphtype)
            plt.xlabel('Time Stamp')
            plt.ylabel('Values')
            plt.show()
        elif(btn=='Save As Excel'):
            try:            
                filename=app.saveBox(title=None, fileName=fromsymbol+"_to_"+tosymbol, dirName=None, fileExt=".csv", fileTypes=None, asFile=None)
                csvdata.to_csv(filename)
            except:
                pass
        elif(btn=='Save To Database'): 
            try:
                filename=app.saveBox(title=None, fileName=fromsymbol+"_to_"+tosymbol, dirName=None, fileExt=None, fileTypes=None, asFile=None)
                a=filename.split('/')
                filename=a[-1]
                csvdata.to_sql(filename, conn)
            except:
                app.errorBox("Error","Database entry failed !")
                return

###############################################################################################################

def crypto(btn):
    fromsymbol=app.getEntry("CRYPTO-CURRENCY SYMBOL : ")
    tosymbol=app.getEntry("EXCHANGE MARKET SYMBOL : ")
    optedgraphsize=app.getEntry('NUMBER OF DATA POINTS: ')
    if(optedgraphsize==''):
        optedgraphsize=None
    else:
        optedgraphsize=int(optedgraphsize)        
    if(fromsymbol=='' or tosymbol==''):
        app.errorBox("Error","symbol of currrency must not be blank")
        return
    else:
        optedfunction=app.getOptionBox("functionpane3")
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
            xaddon=[]
            for row in csvdata.values:
                ytemp.append(row[1])
                xtemp.append(row[0])
                xaddon.append(row[5])
        except:
            app.errorBox("Error","symbol of currency is incorrect !")
            return
        if(btn=='View Graph '):
            y=ytemp[0:optedgraphsize]
            x=xtemp[0:optedgraphsize]
            xadd=xaddon[0:optedgraphsize]
            y.reverse()
            x.reverse()
            xadd.reverse()
            x_axis = range(len(x))
            plt.xticks(x_axis, x)
            plt.plot(x_axis, y,graphtype)
            plt.plot(x_axis,xadd,graphtype)
            plt.xlabel('Time Stamp')
            plt.ylabel('Values')
            plt.legend([fromsymbol,tosymbol])
            plt.show()
        elif(btn=='Save as Excel '):
            try:            
                filename=app.saveBox(title=None, fileName=fromsymbol+"_to_"+tosymbol, dirName=None, fileExt=".csv", fileTypes=None, asFile=None)
                csvdata.to_csv(filename)
            except:
                pass
        elif(btn=='Save to Database '): 
            try:
                filename=app.saveBox(title=None, fileName=fromsymbol+"_to_"+tosymbol, dirName=None, fileExt=None, fileTypes=None, asFile=None)
                a=filename.split('/')
                filename=a[-1]
                csvdata.to_sql(filename, conn)
            except:
                app.errorBox("Error","Database entry failed !")
                return
            
###############################################################################################################

def compare(btn):
    optedsymbol=app.getEntry("SYMBOLS  OF  EQUITYS : ")
    if(optedsymbol=='' or ',' not in optedsymbol):
        app.errorBox("Error","Enter atleast 2 equities !")
        return
    optedgraphsize=app.getEntry("NUMBER OF DATA POINTS :  ")
    if(optedgraphsize==''):
        optedgraphsize=None
    else:
        optedgraphsize=int(optedgraphsize)
    techterm=app.getOptionBox("function2pane4")        
    optedfunction=app.getOptionBox("functionpane4")
    if(optedfunction=="DAILY"):
        optedfunction='daily'
    elif(optedfunction=="WEEKLY"):
        optedfunction='weekly'
    elif(optedfunction=="MONTHLY"):
        optedfunction='monthly'
    equity=optedsymbol.split(',')
    for i in equity:    
        url="https://www.alphavantage.co/query?function="+techterm+"&symbol="+i+"&interval="+optedfunction+"&time_period=10&series_type=open&apikey="+key+"&datatype="+datatype
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
        y=ytemp[0:optedgraphsize]
        x=xtemp[0:optedgraphsize]
        y.reverse()
        x.reverse()
        x_axis = range(len(x))
        plt.xticks(x_axis, x)
        plt.plot(x_axis, y,graphtype)
        plt.xlabel('Time Stamp')
        plt.ylabel('Values')
    plt.legend(equity)    
    plt.show()

###############################################################################################################

def tech(btn):
    optedsymbol=app.getEntry(" SYMBOL  OF  THE  EQUITY : ")
    if(optedsymbol==''):
        app.errorBox("error","symbol of equity must not be blank")
        return        
    optedgraphsize=app.getEntry(" NUMBER OF DATA POINTS : ")
    if(optedgraphsize==''):
        optedgraphsize=None
    else:
        optedgraphsize=int(optedgraphsize)
    techterm=app.getOptionBox("function2pane5")        
    optedfunction=app.getOptionBox("functionpane5")
    if(optedfunction=="DAILY"):
        optedfunction='daily'
    elif(optedfunction=="WEEKLY"):
        optedfunction='weekly'
    elif(optedfunction=="MONTHLY"):
        optedfunction='monthly'
    url="https://www.alphavantage.co/query?function="+techterm+"&symbol="+optedsymbol+"&interval="+optedfunction+"&time_period=10&series_type=open&apikey="+key+"&datatype="+datatype
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
    if(btn==' View Graph '):
        y=ytemp[0:optedgraphsize]
        x=xtemp[0:optedgraphsize]
        y.reverse()
        x.reverse()
        x_axis = range(len(x))
        plt.xticks(x_axis, x)
        plt.plot(x_axis, y,graphtype)
        plt.xlabel('Time Stamp')
        plt.ylabel('Values')
        plt.show()
    elif(btn==' Save as Excel '):
        try:            
            filename=app.saveBox(title=None, fileName=optedsymbol, dirName=None, fileExt=".csv", fileTypes=None, asFile=None)
            csvdata.to_csv(filename)
        except:
            pass
    elif(btn==' Save to Database '): 
        try:
            filename=app.saveBox(title=None, fileName=optedsymbol, dirName=None, fileExt=None, fileTypes=None, asFile=None)
            a=filename.split('/')
            filename=a[-1]
            csvdata.to_sql(filename, conn)
        except:
            app.errorBox("Error","Database entry failed !")
            return

###############################################################################################################

def emulator(btn):
    try:
        sub=gui("secondary")
        sub.removeGrid('g1')
    except:
        pass
    tablename=app.getEntry("Enter The Table Name : ")    
    if(btn=='Show Table Info'):
        if(tablename==''):
            app.errorBox("error","tablename must not be blank")
            return
        cur.execute('PRAGMA table_info('+tablename+')')
        a=cur.fetchall()
        if(len(a)==0):
            app.errorBox("error","table doesnot exist !")
        else:
            header=('column_id','column_name','datatype','notnull','default_value','primarykey')
            a=[header]+a
            sub.addGrid("g1",a,action=None, addRow=None)
            sub.go()
    elif(btn=='Delete Table'):
        if(tablename==''):
            app.errorBox("error","tablename must not be blank")
            return
        try:
            cur.execute('drop table '+tablename)
        except:
            app.errorBox("error","table doesnot exist !")             
    elif(btn=='Show Table'):
        if(tablename==''):
            app.errorBox("error","tablename must not be blank")
            return
        try:
            cur.execute('select * from '+tablename)
            a=cur.fetchall()
            cur.execute('PRAGMA table_info('+tablename+')')
            info=cur.fetchall()
            listheader=list()
            for p in info:
                 listheader.append(p[1])
            q=tuple(listheader)
            listheader=[q]+a
            sub.addGrid("g1",listheader,action=None, addRow=None)
            sub.go()            
        except:
            app.errorBox("error","table doesnot exist !")
    elif(btn=='Execute Query'):
        query=app.getEntry("Enter Custom Query : ")
        if(query==''):
            app.errorBox("error","query must not be blank")
            return
        try:
            cur.execute(query)
            a=cur.fetchall()
            sub.addGrid("g1",a,action=None, addRow=None)
            sub.go()
        except:
            app.errorBox("error","error executing the query") 
            
###############################################################################################################

def settings(btn):
       if(btn=='Create New Database'):
              dbname=app.saveBox(title="Enter new Database Name", fileName=None, dirName=None, fileExt='sqlite', fileTypes=None, asFile=None)
              conn = sqlite3.connect(dbname)
              cur = conn.cursor()
              app.setLabel("title2","Current Database : "+dbname)
              settingsfile['currentdatabase']=dbname
       elif(btn=='Attach a Database'):
              a=app.openBox(title="Select the Database",dirName=None)
              if('.sqlite' not in a):
                     app.errorBox("error","please select a sqlite file")
                     return
              conn = sqlite3.connect(a)
              cur = conn.cursor()
              app.setLabel("title2","Current Database : "+a)
              settingsfile['currentdatabase']=a
       elif(btn=='Delete a Database'):
              try:
                     a=app.openBox(title="Select the Database",dirName=None)
                     if('db.sqlite' in a):
                            app.errorBox("Error","Bulitin database cannot be deleted !")
                            return
                     elif('.sqlite' not in a):
                            app.errorBox("Error","please select a sqlite file")
                            return
                     elif(a in settingsfile['currentdatabase']):
                            app.setLabel("title2","Current Database : db.sqlite")### default undeleteable database
                            conn = sqlite3.connect('db.sqlite')
                            cur = conn.cursor()
                            settingsfile['currentdatabase']='db.sqlite'
                     os.remove(a)
              except:
                     pass
       elif(btn=='Save'):
           gtype=app.getOptionBox("gt")
           app.setLabel("title3", "Current Graph type : "+gtype)
           if(gtype=="line graph"):
                gtype='-'
           elif(gtype=="stripped graph"):
                gtype='--'
           elif(gtype=="strip-dot graph"):
                gtype='-.'
           elif(gtype=="dot graph"):
                gtype=':'
           elif(gtype=='Points'):
                gtype='ro'
       settingsfile['graphtype']=gtype
       global graphtype
       graphtype=gtype
       with open('filename.pickle', 'wb') as handle:
                  pickle.dump(settingsfile, handle)

###############################################################################################################

app = gui("UNNAMED")
app.setBg("lightBlue")
app.setGeom ( "fullscreen" )
app.setFont(20)
app.addToolbar(["TEMP1", "TEMP2", "TEMP3", "TEMP4", "About", "Full Screen","Exit"], toolbar, findIcon=True)
app.addStatusbar(header="STATUS ",fields=1, side="RIGHT")
app.setStatusbarWidth(20, field=0)
app.setStatusbar("ready", field=0)

app.startTabbedFrame("VIEW")

app.startTab("Portfolio Management")

app.stopTab()

app.startTab("Global Stock Data Managment")
app.addLabelEntry("SYMBOL  OF  THE  EQUITY : ")
app.addLabelEntry("NUMBER OF DATA POINTS : ")
app.addLabel("pane1","TIME SERIES : ")
app.addOptionBox("functionpane1", ["DAILY", "WEEKLY", "MONTHLY", "INTRADAY"])
app.addButtons(["View Graph","Save to Database","Save as Excel"], globalstockdata)
app.stopTab()

app.startTab("Foreign Exchange Management")
app.addLabelEntry("FROM : ")
app.addLabelEntry("TO : ")
app.addButton("Get Exchange Rate",exchange)
app.addLabel("pane2","TIME SERIES - ")
app.addOptionBox("functionpane2", ["DAILY", "WEEKLY", "MONTHLY", "INTRADAY"])
app.addLabelEntry("NUMBER OF DATA POINTS - ")
app.addButtons(["Visualize","Save To Database","Save As Excel"], exchange)
app.stopTab()

app.startTab("Digital & Crypto Currency Management") 
app.addLabelEntry("CRYPTO-CURRENCY SYMBOL : ")
app.addLabelEntry("EXCHANGE MARKET SYMBOL : ")
app.addLabelEntry("NUMBER OF DATA POINTS: ")
app.addLabel("pane3","TIME SERIES : ")
app.addOptionBox("functionpane3", ["DAILY", "WEEKLY", "MONTHLY", "INTRADAY"])
app.addButtons(["View Graph ","Save to Database ","Save as Excel "],crypto)
app.stopTab()

app.startTab("Compare Stock Prices")
app.addLabelEntry("SYMBOLS  OF  EQUITYS : ")
app.addLabelEntry("NUMBER OF DATA POINTS :  ")
app.addLabel("pane4","TIME SERIES : ")
app.addOptionBox("functionpane4", ["DAILY", "WEEKLY", "MONTHLY", ])
app.addOptionBox("function2pane4", ["SMA", "EMA", "WMA","DEMA","TEMA","TRIMA","KAMA","MIDPOINT","MIDPRICE"])
app.addButton(" Visualize ",compare)
app.stopTab()

app.startTab("Stock Technical Indicators")
app.addLabelEntry(" SYMBOL  OF  THE  EQUITY : ")
app.addLabelEntry(" NUMBER OF DATA POINTS : ")
app.addLabel("pane5","TIME SERIES : ")
app.addOptionBox("functionpane5", ["DAILY", "WEEKLY", "MONTHLY", ])
app.addOptionBox("function2pane5", ["SMA", "EMA", "WMA","DEMA","TEMA","TRIMA","KAMA","MIDPOINT","MIDPRICE"])
app.addButtons([" View Graph "," Save to Database "," Save as Excel "], tech)
app.stopTab()

app.startTab("Database Emulator")
app.addLabel("pane6", "database management")
app.addLabelEntry("Enter The Table Name : ")
app.addButtons(["Show Table Info","Delete Table","Show Table"], emulator)
app.addLabelEntry("Enter Custom Query : ")
app.addButton("Execute Query", emulator)
app.stopTab()

app.startTab("External Resources")
app.addLabel("externallink","Links")
app.addWebLink ( "Google Finanace", "https://www.google.com/finance")
app.addWebLink ( "NSE India", "https://www.nseindia.com")
app.addWebLink ( "BSE India", "https://www.bseindia.com")
app.addWebLink ( "NASDAQ", "https://www.nasdaq.com")
app.addWebLink ( "Investopedia", "https://www.investopedia.com")
app.stopTab()

app.startTab("Settings")
app.addLabel("title","Database Settings")
app.addLabel("title2","Current Database : "+settingsfile['currentdatabase'])
app.addButtons(["Create New Database","Attach a Database","Delete a Database"],settings)
app.addLabel("title3", "Current Graph type : "+settingsfile['graphtype'])
app.addLabel("title4","Change graph type")
app.addOptionBox("gt", ["line graph","stripped graph", "strip-dot graph","dot graph",'Points'])
app.addButton("Save", settings)
app.stopTab()

app.stopTabbedFrame()

##############################################################################################################

app.startSubWindow("Exchange Rates")
app.addLabel("l2", "Realtime Exchange Rate")
app.addLabel("l3","")
app.addLabel("l4","")
app.addLabel("l5","")
app.addLabel("l6","")
app.stopSubWindow()

##############################################################################################################

app.setTabBg('VIEW',"Portfolio Management","LightCoral")
app.setTabBg('VIEW',"Global Stock Data Managment","PaleVioletRed")
app.setTabBg('VIEW',"Foreign Exchange Management","LightCoral")
app.setTabBg('VIEW',"Digital & Crypto Currency Management","SandyBrown")
app.setTabBg('VIEW',"Compare Stock Prices","LightCoral")
app.setTabBg('VIEW',"Stock Technical Indicators","LightSalmon")
app.setTabBg('VIEW',"Database Emulator","DarkSalmon")
app.setTabBg('VIEW',"External Resources","LightCoral")
app.setTabBg('VIEW',"Settings","SIlver")

##############################################################################################################

app.startSubWindow("About")
app.addLabel("aboutpopup", "info about the pgm")
app.stopSubWindow()

##############################################################################################################

app.go()
