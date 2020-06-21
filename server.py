import socket
import pickle
import threading
import re 
clients=[]
name=[]
client_id=1
time=6
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
			global time 
			global client_id
			while (True):   
				try:
					if(self.msg==100): 
						self.msg=201  
					elif(self.id==client_id):
						self.msg="wait:"+str(time) 
						client_id=99
						time=60
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
while(True):  
	c, addr = s.accept()
	if(len(clients)==0):
		count=1
	else:	
		x=sorted(clients)
		count=int(x[len(clients)-1])+1
	t=myThread(c,count)
	t.start() 