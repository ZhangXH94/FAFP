import Tkinter as tk
from forecast import *
import matplotlib
from matplotlib.figure import  Figure
from numpy import arange,sin,pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from precision import *
import datetime
import pandas as pd 
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
import math


window = tk.Tk()
window.title('Forecast Stock Price')
window.geometry('700x350')

l_start = tk.Label(window,text='StartTime: ').place(x=10,y=50)
l_end = tk.Label(window,text='EndTime:  ').place(x=10,y=100)
l_Company = tk.Label(window,text='Company: ').place(x=10,y=150)

entry_start = tk.Entry(window)
entry_start.place(x=70,y=50)
entry_end = tk.Entry(window)
entry_end.place(x=70,y=100)
entry_company = tk.Entry(window)
entry_company.place(x=70,y=150)

def _forecast():
    global entry_start,entry_end,entry_company
    starttime = entry_start.get()
    endtime = entry_end.get()
    symbol = entry_company.get()
    f = Figure(figsize=(4,3) , dpi=95)
    a = f.add_subplot(111)

    
    df = web.DataReader(symbol,'quandl',starttime,endtime)
    df.to_csv('./temp.csv')

    fsplit = open('./temp.csv','r')
    lines_label = fsplit.readlines()
    fsplit.close()
    close = list()
    for each in lines_label[1:]:
        tokens = each.split(',')
        close.append(tokens[4])
    closed = close[::-1]
    dateX = np.arange(1,len(closed)+1)
    X = np.array(closed,dtype='float32')
    results = {}
    results = forecast(X)
    results = calAccuracy(results)
    accuracy = results['accuracy']
    X = results['history']
    X_pred = results['perdict']
    len1 = len(X)
    len2 = len(X_pred)
    a.scatter(range(0,len1),X,marker='o',color='b',label='truth')
    a.scatter(range(len1-len2,len1),X_pred,marker='X',color='r',label='prediction')
    a.plot(range(0,len1),X,color='b')
    a.plot(range(len1-len2,len1),X_pred,color='r')
    a.legend(loc='lower right')
    a.set_xlabel('time(day)')
    a.set_ylabel('Stock price(USD)')




    canvas = FigureCanvasTkAgg(f,master=window)
    canvas.show()
    canvas.get_tk_widget().place(x=300,y=10)
    

    
btn_forecast = tk.Button(window,text='Forecast',command=_forecast).place(x=30,y=200)
btn_clear = tk.Button(window,text='Clear').place(x=120,y=200)



window.mainloop()
