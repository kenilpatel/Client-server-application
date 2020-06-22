from tkinter import *
import datetime
import time
import threading 
import sys
import os
from tkinter import font 
timer=0
exit=0
root = Tk()
nts=""	
conn=0
name=StringVar()
class random_select(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self): 
		global timer
		global conn
		while(True): 
			timer=timer+1
			print(timer)
			if(timer%10==0):
				conn=0
			time.sleep(1) 
def close_window(): 
    root.destroy()
    os._exit(0)
def enter_data():
	global conn
	nts=name.get()
	if(nts!=""):
		conn=1	
	else:
		conn=0
myFont = font.Font(size=20)
myFontt = font.Font(size=40)
Label(root).pack()
Label(root).pack()
btn=Button(root,text="Close connection",command=close_window)
btn['font']=myFont
btn.pack()
en=Entry(root,textvariable=name)
en['font']=myFont
submit=Button(root,text="Connect",command=enter_data)
submit['font']=myFont
tlab=Label(root,text="Wait timer")
tlab['font']=myFont
Label(root).pack()
Label(root).pack()
tlab.pack()
lab = Label(root)
lab['font']=myFontt
Label(root).pack()
Label(root).pack()
lab.pack() 
Label(root).pack()
Label(root).pack()
status=Label(root)
status['font']=myFont
status.pack()
Label(root).pack()
Label(root).pack()
root.geometry("500x600") 
btn=Button(root,text="Close connection",command=close_window)
def clock(): 
    lab.config(text=str(timer))
    root.after(10, clock) 
    if(conn==1):
    	status.config(text="Connected")
    	en.pack_forget()
    	submit.pack_forget() 
    if(conn==0):
    	status.config(text="Not connected")
    	en.pack()
    	submit.pack()  
clock()  
r=random_select()
r.start()
root.mainloop()


