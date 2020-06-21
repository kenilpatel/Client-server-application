import socket
import pickle
import threading
import re 
from random import randint
import time
clients=[]
name=[]
client_id=-1
timer=-1
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
					print("Wait signal sent to ",name[index]," to wait for ",timer)
					x=10
				# print("Next wait signal in",x)
				time.sleep(1)

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
					print(self.n," disconnected")
					clients.remove(self.id) 
					if(self.n!=""):
						name.remove(self.n)
					break  
s=socket.socket()
port=7398
s.bind(('',port))
s.listen(5)
flag=0
count=0
t1=random_select()
t1.start()
while(True):  
	c, addr = s.accept()
	if(len(clients)==0):
		count=1
	else:	
		x=sorted(clients)
		count=int(x[len(clients)-1])+1
	t=myThread(c,count)
	t.start() 