import socket
import pickle
import re
import threading
import time
from tkinter import *  
import sys
import os
from tkinter import font 
root = Tk()
timer=0
name=StringVar()
class timer_display(threading.Thread):
    def __init__(self,t):
        threading.Thread.__init__(self) 
        self.t=t 
    def run(self):
        global timer
        while(True):
            if(timer>0):
                while(timer>=0):  
                    timer=timer-1
                    time.sleep(1) 
                timer=0 
class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
        self.s=None
        self.port=7398
        self.conn=0 
        self.status=""
        self.code=0
        self.name_client=""
    def run(self): 
        while(True): 
            if(self.conn==0):
                # print("new connection")
                try:
                    self.s=socket.socket()
                    self.s.connect(('127.0.0.1',self.port)) 
                    self.conn=1
                except:
                    # print("can not reach server")
                    self.status="Server is not available"
                    self.conn=0
                    self.code=403
            else:
                try: 
                    msg=pickle.loads(self.s.recv(1024))  
                    if(msg==404): 
                        self.status="server is full please try after some time"
                        self.conn=0
                        self.code=404
                    elif(msg==201):
                        self.code=201
                        self.status="Connected"
                        while(self.name_client==""):
                            pass
                        data = pickle.dumps(self.name_client)
                        self.s.send(data)
                        self.conn=1
                    elif(msg==400):  
                        self.name=""
                        self.conn=0 
                        self.code=400
                    elif(re.search("^wait:*",str(msg))!=None): 
                        x,t=msg.split(":")
                        global timer
                        timer=int(t)
                        t=int(t) 
                        waiting=0 
                        while timer>=0:
                            # print(waiting)
                            waiting=waiting+1
                            if(waiting==t):
                                break
                            time.sleep(1) 
                        # print("waited this time")
                        d = "Waited for "+str(waiting)+" seconds" 
                        data = pickle.dumps(d)
                        self.s.send(data)
                        self.conn=1 
                        self.status="Connected"
                    elif(msg==200):
                        d=200
                        data = pickle.dumps(d)
                        self.s.send(data) 
                        self.conn=1
                        self.status="Connected" 
                        self.code=200
                except Exception as e:  
                    # print(e)
                    self.name_client=""
                    self.status="Server is not available"
                    self.conn=0
                    self.code=403
t=myThread()
t.start()
def close_window(): 
    root.destroy()
    os._exit(0)
def skiptimer():
    global timer
    timer=0
def enter_data(): 
    nts=name.get() 
    if(nts!=""):
      t.name_client=nts  
    else:
      t.name_client=""
wait_timer=timer_display(t)
wait_timer.start() 
myFont = font.Font(size=20)
myFont1 = font.Font(size=40)
Label(root).pack()
Label(root).pack()
warning=Label(root)
warning['font']=myFont
warning.pack()
Label(root).pack()
Label(root).pack()
btn=Button(root,text="Close connection",command=close_window)
btn['font']=myFont
btn.pack()
en=Entry(root,textvariable=name)
en['font']=myFont
root.geometry("600x800")  
submit=Button(root,text="Connect",command=enter_data)
submit['font']=myFont
Label(root).pack()
Label(root).pack()
tlab=Label(root,text="Wait timer")
tlab['font']=myFont
tlab.pack()
Label(root).pack()
Label(root).pack()
lab = Label(root)
lab['font']=myFont1
Label(root).pack()
Label(root).pack()
lab.pack() 
Label(root).pack()
skip=Button(root,text="Skip timer",command=skiptimer)
skip['font']=myFont
skip.pack()
Label(root).pack()
Label(root).pack()
status=Label(root)
status['font']=myFont
status.pack()
Label(root).pack()
Label(root).pack() 
def update(): 
    if(timer>=0):
        lab.config(text=str(timer))
    else:
        lab.config(text=str(0)) 
    if(t.code==400):
        warning.config(text="Name is already taken")
    elif(t.code==404): 
        warning.config(text="")
        status.config(text=t.status)
        en.pack_forget()
        submit.pack_forget() 
    elif(t.code==201):
        warning.config(text="")
        status.config(text=t.status)
        en.pack()
        submit.pack()  
    elif(t.code==200):
        warning.config(text="") 
        status.config(text=t.status) 
        en.pack_forget()
        submit.pack_forget()
    elif(t.code==403):
        warning.config(text="")
        status.config(text=t.status) 
        en.pack_forget()
        submit.pack_forget()
    root.after(100, update)
update()  
root.mainloop()