#演示系统，主要利用Tkitnter包，作可视化页面的开发
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

#建立一个窗口，规定标题和尺寸
window = tk.Tk()
window.title('Forecast Stock Price')
window.geometry('700x350')

#建立开始时间，结束时间，公司名称的标签
l_start = tk.Label(window,text='StartTime: ').place(x=10,y=50)
l_end = tk.Label(window,text='EndTime:  ').place(x=10,y=100)
l_Company = tk.Label(window,text='Company: ').place(x=10,y=150)

#建立开始时间，结束时间，公司名称的输入框
entry_start = tk.Entry(window)
entry_start.place(x=70,y=50)
entry_end = tk.Entry(window)
entry_end.place(x=70,y=100)
entry_company = tk.Entry(window)
entry_company.place(x=70,y=150)

#预测按钮的响应函数
def _forecast():
    global entry_start,entry_end,entry_company
    #获取输入框的值，得到开始时间，结束时间，公司名称
    starttime = entry_start.get()
    endtime = entry_end.get()
    symbol = entry_company.get()
    f = Figure(figsize=(4,3) , dpi=95)
    a = f.add_subplot(111)
    #利用条件，动态发送数据请求
    df = web.DataReader(symbol,'quandl',starttime,endtime)
    #将返回的数据存到CSV文件中
    df.to_csv('./temp.csv')
    #打开存储数据的文件
    fsplit = open('./temp.csv','r')
    #按行读取文件
    lines_label = fsplit.readlines()
    fsplit.close()
    #声明一个数组，用于存储收盘价格序列
    close = list()
    #提取每条记录中的收盘价，保存在close数组中
    for each in lines_label[1:]:
        tokens = each.split(',')
        close.append(tokens[4])
    #将close的时间逆序改成时间顺序
    closed = close[::-1]
    #定义一个表示天数的序列
    dateX = np.arange(1,len(closed)+1)
    #用close数组，定一个收盘价序列
    X = np.array(closed,dtype='float32')
    #声明一个用于存储预测结果的对象
    results = {}
    #调用forecast函数，进行预测，返回的结果存在result对象中
    results = forecast(X)
    #调用calAccuracy函数，计算预测的准确率（误差）,结果存在result对象中
    results = calAccuracy(results)
    #依次从results对象中获取准确率，历史值和预测值，用于绘图展示
    accuracy = results['accuracy']
    X = results['history']
    X_pred = results['perdict']
    len1 = len(X)
    len2 = len(X_pred)
    #将历史值，预测值进行绘图展示
    a.scatter(range(0,len1),X,marker='o',color='b',label='truth')
    a.scatter(range(len1-len2,len1),X_pred,marker='X',color='r',label='prediction')
    a.plot(range(0,len1),X,color='b')
    a.plot(range(len1-len2,len1),X_pred,color='r')
    #设置图例，坐标标注
    a.legend(loc='lower right')
    a.set_xlabel('time(day)')
    a.set_ylabel('Stock price(USD)')
    #显示绘图内容
    canvas = FigureCanvasTkAgg(f,master=window)
    canvas.show()
    canvas.get_tk_widget().place(x=300,y=10)
    

#预测按钮    
btn_forecast = tk.Button(window,text='Forecast',command=_forecast).place(x=30,y=200)
#清空按钮
btn_clear = tk.Button(window,text='Clear').place(x=120,y=200)



window.mainloop()
