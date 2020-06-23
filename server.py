import socket
import pickle
import threading
import re 
from random import randint
import time
from tkinter import * 
from tkinter import font
import os
clients=[] 
name=[]
client_id=-1
timer=-1
root = Tk()
signal=""
signal_disconnected=""
class random_select(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 
    def run(self):
        x=10
        global client_id
        global timer
        while(True): 
            if(len(name)!=0):
                x=x-1
                if(x==0): 
                    index=randint(0,len(clients)-1)
                    client_id=clients[index]
                    timer=randint(3,9)
                    global signal
                    # signal="Wait signal sent to "+str(name[index])+" to wait for "+str(timer)
                    # print("Wait signal sent to ",name[index]," to wait for ",timer)
                    x=10
                # print("Next wait signal in",x)
                time.sleep(1)
class handle_client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        s=socket.socket()
        port=7398
        s.bind(('',port))
        s.listen(5)
        flag=0
        count=0
        while(True):  
            c, addr = s.accept()
            if(len(clients)==0):
                count=1
            else:   
                x=sorted(clients)
                count=int(x[len(clients)-1])+1
            t=myThread(c,count)
            t.start() 
class myThread(threading.Thread):
    def __init__(self,c,id):
        threading.Thread.__init__(self)
        self.c=c
        self.id=id
        self.n="" 
        self.msg=100
    def run(self): 
        err=0  
        clients.append(self.id) 
        global signal_disconnected
        if(len(clients)==4):
            clients.remove(self.id)
            self.msg = 404
            data = pickle.dumps(self.msg)
            self.c.send(data)   
        else:
            global timer 
            global client_id
            while (True):    
                try:
                    if(self.msg==100): 
                        signal_disconnected=""
                        self.msg=201  
                    elif(self.id==client_id):
                        self.msg="wait:"+str(timer)  
                        client_id=-1
                    else:
                        self.msg=200
                    data = pickle.dumps(self.msg)
                    self.c.send(data)
                    rdata = pickle.loads(self.c.recv(1024))
                    if(rdata!=200 and self.msg!=201):
                        display=self.n+" "+rdata
                        global signal
                        signal=self.n+" "+rdata
                        print(display)
                    if(self.msg==201): 
                        if(rdata in name):
                            self.msg=400
                            data = pickle.dumps(self.msg)
                            self.c.send(data)
                            raise("Name is already taken")
                        else: 
                            self.n=rdata 
                            name.append(self.n)
                            self.msg=200
                except Exception as e: 
                    err=1 
                    if(self.n!=""): 
                        signal_disconnected=self.n+" disconnected"
                        print(self.n," disconnected")
                    clients.remove(self.id) 
                    if(self.n!=""):
                        name.remove(self.n)
                    break  
t1=random_select()
t1.start()
def close_window(): 
    root.destroy()
    os._exit(0)
myFont = font.Font(size=20)
myFont1 = font.Font(size=40)
Label(root).pack()
Label(root).pack()
btn=Button(root,text="Close server",command=close_window)
btn['font']=myFont
btn.pack()
root.geometry("600x600")  
Label(root).pack()
Label(root).pack()
status=Label(root)
status['font']=myFont
status.pack()
Label(root).pack()
Label(root).pack()
head=Label(root,text="Currently connected client")
head['font']=myFont
head.pack()
Label(root).pack()
Label(root).pack()
cstatus=Label(root)
cstatus['font']=myFont
cstatus.pack()
Label(root).pack()
Label(root).pack()
dstatus=Label(root)
dstatus['font']=myFont
dstatus.pack()
Label(root).pack()
Label(root).pack() 
def update():
    status.config(text=signal)
    c=""
    if(len(name)==0):
        c="No one is connected"
    else:
        for i in name:
            c=c+i+"\n"
    cstatus.config(text=c)
    dstatus.config(text=signal_disconnected)
    root.after(100, update)
update()  
main_t=handle_client()
main_t.start()
root.mainloop()

