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
		while (True):
			if(len(clients)<=3):
				try:
					msg = "server data"
					data = pickle.dumps(msg)
					self.c.send(data)
					msg = pickle.loads(self.c.recv(1024))
				except Exception as e:
					err=1
					print(self.name," disconnected") 
					clients.remove(self.name) 
					break   
			else: 
				clients.remove(self.name)
				msg = -1
				data = pickle.dumps(msg)
				self.c.send(data) 
				break 
s=socket.socket()
port=7398
s.bind(('',port))
s.listen(5)
flag=0
count=0
while(True):  
	c, addr = s.accept()
	count=count+1
	t=myThread(c,count)
	t.start() 