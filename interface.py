from appJar import gui

app = gui('unnamed',"800x600")

app.addStatusbar(fields=3, side="RIGHT")
app.setStatusbar('ready', field=2)
app.showSplash('unnamed\nloading..', fill='red', stripe='black', fg='yellow', font=44)
app.go()
