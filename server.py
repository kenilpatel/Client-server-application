import socket
import pickle
import threading
class data(object):
	def __init__(self,client=None,count=0):
		self.client=client
		self.count=-1
		self.client=-1
clients=[]
class myThread(threading.Thread):
	def __init__(self,c,name):
		threading.Thread.__init__(self)
		self.c=c
		self.name=name
	def run(self):
		err=0  
		clients.append(self.name)
		print(clients)
		if(len(clients)==4):
			clients.remove(self.name)
			msg = 404
			data = pickle.dumps(msg)
			self.c.send(data)   
		else:
			while (True): 
				try:
					msg = 200
					data = pickle.dumps(msg)
					self.c.send(data)
					msg = pickle.loads(self.c.recv(1024))
				except Exception as e:
					err=1
					print(self.name," disconnected") 
					clients.remove(self.name) 
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