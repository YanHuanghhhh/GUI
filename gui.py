import tkinter as tk  # 使用Tkinter前需要先导入
import numpy as np
import os
from typing import Counter, Sized
import cv2
import random
import time
import tkinter.ttk
from math import *
from tkinter.constants import *

from numpy.lib.function_base import angle 


class GUI():
    def  __init__(self, photo_path, pic_height=1000, pic_width=800):
        #创建初始基站坐标点
        self.baseA = {'x':100+pic_width, 'y':pic_height/2+30, 'angle':0}
        self.baseB = {'x':100+pic_width/2, 'y':30, 'angle':0}
        #创建初始窗口
        self.window = tk.Tk()
        self.window.title('大创展示框架')
        self.window.geometry('1000x1000')
        #self.window.resizable(False, False)
        #创建幕布
        self.canvas = tk.Canvas(self.window, bg='white', height=pic_height, width=200+pic_width)
        #幕布上画出图像
        self.photo_file = tk.PhotoImage(file=photo_path)
        self.photo = self.canvas.create_image(100, 0, anchor='nw', image=self.photo_file)
        self.canvas.place(x=50,y=0)
        #将基站所在的位置用椭圆和坐标表示出
        self.plot_oval(self.baseA,text='A')
        self.plot_oval(self.baseB,text='B')
        #描绘出基站天线的初始方向(朝右边)
        self.arrow_options={'width':9, 'length':80, 'format':'last'}
        self.arrowA = self._init_arrow_direction(self.baseA)
        self.arrowB = self._init_arrow_direction(self.baseB)

        ''' 创建我们所需的按键(我们用最粗糙的办法，每个选项造个按键)'''
        #运行代码按键
        self.RunButton = tk.Button(self.window,text='RUN',font=('Verdana', 15, 'bold'),
                                    bd=5,command=self.run, activeforeground= 'blue') 
        self.RunButton.place(x=100,y=680,width=120,height=40)
        #运行代码终止按键
        self.QuitButton = tk.Button(self.window,text='QUIT',font=('Verdana', 15, 'bold'),
                                    bd=5,command=self.quit, activeforeground= 'blue') 
        self.QuitButton.place(x=240,y=680,width=120,height=40)
        self.NoQuit=True

        #A上下左右按键
        self.AText = tk.StringVar()
        self.ALabel = tk.Label(self.window, textvariable=self.AText, width=10, height=2, 
                        font=('Arial', 15),bg='white', fg='red')
        self.AText.set('天线A的方向')
        self.ALabel.place(x=100,y=740,width=150,height=40)
        self.ARightButton = tk.Button(self.window,text='右',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowA_right, activeforeground= 'blue',width=15)
        self.ARightButton.place(x=270,y=740,width=120,height=40)
        self.AUpButton = tk.Button(self.window,text='上',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowA_up, activeforeground= 'blue',width=15)
        self.AUpButton.place(x=400,y=740,width=120,height=40)
        self.ALeftButton = tk.Button(self.window,text='左',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowA_left, activeforeground= 'blue',width=15)
        self.ALeftButton.place(x=530,y=740,width=120,height=40)
        self.ADownButton = tk.Button(self.window,text='下',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowA_down, activeforeground= 'blue',width=15)
        self.ADownButton.place(x=660,y=740,width=120,height=40)

        #B上下左右按键
        self.BText = tk.StringVar()
        self.BLabel = tk.Label(self.window, textvariable=self.BText, width=10, height=2, 
                        font=('Arial', 15),bg='white', fg='red')
        self.BText.set('天线B的方向')
        self.BLabel.place(x=100,y=800,width=150,height=40)
        self.BRightButton = tk.Button(self.window,text='右',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowB_right, activeforeground= 'blue',width=15)
        self.BRightButton.place(x=270,y=800,width=120,height=40)
        self.BUpButton = tk.Button(self.window,text='上',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowB_up, activeforeground= 'blue',width=15)
        self.BUpButton.place(x=400,y=800,width=120,height=40)
        self.BLeftButton = tk.Button(self.window,text='左',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowB_left, activeforeground= 'blue',width=15)
        self.BLeftButton.place(x=530,y=800,width=120,height=40)
        self.BDownButton = tk.Button(self.window,text='下',font=('Verdana', 10, 'bold'),
                                    bd=5,command=self.arrowB_down, activeforeground= 'blue',width=15)
        self.BDownButton.place(x=660,y=800,width=120,height=40)
        ''' 按键结束区域 '''
        #初始化我们要找的坐标
        self.baseC={'x':300, 'y':100, 'angle':0}
        self.ovalc,self.indexc=self.plot_oval(self.baseC,color='blue')
        self.line_ac = self.canvas.create_line(self.baseA['x'],self.baseA['y'],self.baseC['x'],
                                    self.baseC['y'],arrow='none',width=5)
        self.line_bc = self.canvas.create_line(self.baseB['x'],self.baseB['y'],self.baseC['x'],
                                    self.baseC['y'],arrow='none',width=5)
        #设立界限
        self.MINX=0
        self.MAXX=200+pic_width
        self.MINY=0
        self.MAXY=pic_height

        #self.window.after(2000,self.run)
        #主窗口循环表示
        self.window.mainloop()

    # 初始化基站天线方向
    def _init_arrow_direction(self,base):
        arrow=self.canvas.create_line((base['x'],base['y'],base['x']+self.arrow_options['length'],
                                        base['y']) ,arrow=self.arrow_options['format'],
                                        width=self.arrow_options['width'])
        return arrow

    def plot_oval(self,base,color='pink',text=''): #画出相应点的椭圆和坐标
        oval=self.canvas.create_oval((base['x']-10, base['y']-10, base['x']+10, base['y']+10),fill=color)
        index=self.canvas.create_text(base['x']+25, base['y']+25, text="({} x:{} y:{})".format(text,base['x'],base['y'])
                        , font=("Purisa", 20))
        return oval,index
    
    def adjust_point(self,oval,index,line_ac,line_bc):
        self.canvas.coords(oval,self.baseC['x']-10, self.baseC['y']-10, self.baseC['x']+10, self.baseC['y']+10)
        self.canvas.coords(index,self.baseC['x']+25,self.baseC['y']+25)
        #self.canvas.itemconfig(index,text="(x:{} y:{})".format(self.baseC['x'],self.baseC['y']))
        self.canvas.itemconfig(index,text="(x:%.2f y:%.2f)"%(self.baseC['x'],self.baseC['y']))
        self.canvas.coords(line_ac,self.baseA['x'],self.baseA['y'],self.baseC['x'],self.baseC['y'])
        self.canvas.coords(line_bc,self.baseB['x'],self.baseB['y'],self.baseC['x'],self.baseC['y'])

    def plot_base_line(self,base,arrow,num): #调整基站箭头方向
        if num==0: #指向右边
            self.canvas.coords(arrow,base['x'],base['y'],base['x']+self.arrow_options['length'],base['y'])
            base['angle']=0
        elif num==1: #指向上方
            self.canvas.coords(arrow,base['x'],base['y'],base['x'],base['y']-self.arrow_options['length'])
            base['angle']=90
        elif num==2: #指向左边
            self.canvas.coords(arrow,base['x'],base['y'],base['x']-self.arrow_options['length'],base['y'])
            base['angle']=180
        else: #指向下方
            self.canvas.coords(arrow,base['x'],base['y'],base['x'],base['y']+self.arrow_options['length'])
            base['angle']=270

    #天线方向改变函数集合
    def arrowA_right(self):
        self.plot_base_line(base=self.baseA,arrow=self.arrowA,num=0)
    def arrowA_up(self):
        self.plot_base_line(base=self.baseA,arrow=self.arrowA,num=1)
    def arrowA_left(self):
        self.plot_base_line(base=self.baseA,arrow=self.arrowA,num=2)
    def arrowA_down(self):
        self.plot_base_line(base=self.baseA,arrow=self.arrowA,num=3)
    def arrowB_right(self):
        self.plot_base_line(base=self.baseB,arrow=self.arrowB,num=0)
    def arrowB_up(self):
        self.plot_base_line(base=self.baseB,arrow=self.arrowB,num=1)
    def arrowB_left(self):
        self.plot_base_line(base=self.baseB,arrow=self.arrowB,num=2)
    def arrowB_down(self):
        self.plot_base_line(base=self.baseB,arrow=self.arrowB,num=3)
    
    ''' 数学函数部分 '''
    def run(self):
        self.NoQuit=True
        while self.NoQuit:
            self.point_display()
            time.sleep(0.1)
            #self.window.update()
            #self.window.after(2000,self.point_display)

    def quit(self):
        self.NoQuit=False

    def point_display(self): #RUN按钮触发的函数
        # file_path1='/home/yanhhh201203/Desktop/r1_file/angles.dat'
        # file_path2='/home/yanhhh201203/Desktop/r2_file/angles.dat'
        file_path1='./data/dataA.txt'
        file_path2='./data/dataB.txt'
        theta1= self.get_actual_base(base=self.baseA,file_path=file_path1)
        theta2= self.get_actual_base(base=self.baseB,file_path=file_path2)
        print('theta1={},theta2={}'.format(theta1,theta2))
        #得到两条直线的斜率
        k1=tan(theta1)
        k2=tan(theta2)
        b1=self.baseA['y']-k1*self.baseA['x']
        b2=self.baseB['y']-k2*self.baseB['x']
        #print('k1={}  k2={}'.format(k1,k2))
        if abs(k2-k1)>1e-5:
        #if TRUE:
            x3=(b2-b1)/(k1-k2)
            y3=k1*x3+b1
            #print('x={}  y={}'.format(x3,y3))
            if (x3>self.MINX)and (x3<self.MAXX) and (y3>self.MINY) and (y3<self.MAXY):
                self.baseC['x']=x3
                self.baseC['y']=y3
                self.adjust_point(oval=self.ovalc,index=self.indexc,line_ac=self.line_ac,
                                 line_bc=self.line_bc)
        self.window.update()
        #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    def angle2rad(self,x):
        return (x*2*pi/360)

    def  get_actual_base(self,base,file_path):
        theta=self.read_data(file_path=file_path)
        theta=self.angle2rad(theta)
        if (base['angle']==0) or (base['angle']==180):
            return pi/2-theta
        else:
            return -theta
        
    
    def read_data(self,file_path):
        n=30
        offset = -2000
        data=np.zeros(n)
        ii=0
        with open(file_path,'rb') as f:
            f.seek(0,2)
            f.seek(offset,2)
            for row in f.readlines()[1:n]:
                data[ii]=float(row.decode().split(' ')[1])
                ii+=1
        # f=open(file_path,'rb')
        # f.seek(0,2)
        # f.seek(offset,2)
        # for row in f.readlines()[1:n]:
        #     data[ii]=float(row.decode().split(' ')[1])
        #     ii+=1
        #数据清洗
        mean= np.mean(data)
        std= np.std(data)
        #print((data>(mean-3*std)) & (data<(mean+3*std)))
        data=data[(data>(mean-3*std)) & (data<(mean+3*std))]
        return np.mean(data)

photo_path=os.getcwd()+'/data/map.gif' #gif格式
img = cv2.imread('./data/map.png')     #png格式

mygui = GUI(photo_path=photo_path, pic_height=img.shape[0], pic_width=img.shape[1])
