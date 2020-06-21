import socket
import pickle
import re
import threading
import time
timer=0
class timer_display(threading.Thread):
	def __init__(self,t):
		threading.Thread.__init__(self) 
		self.t=t 
	def run(self):
		global timer
		while(True):
			if(timer>0):
				while(timer>=0):
					print(timer)
					if(timer==4):
						timer=0
					timer=timer-1
					time.sleep(1) 
				timer=0 
class myThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self) 
		self.s=None
		self.port=7398
		self.conn=0 
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
					self.conn=0
			else:
				try: 
					msg=pickle.loads(self.s.recv(1024)) 
					# print("recieved message",msg)
					if(msg==404):
						print("server is full please try after some time") 
						self.conn=0
					elif(msg==201):
						d = input("Enter your name")
						data = pickle.dumps(d)
						self.s.send(data)
						self.conn=1
					elif(msg==400):
						print("Name is already taken please try another name")
						self.conn=0 
					elif(re.search("^wait:*",str(msg))!=None):
						# print(re.search("^wait:*",str(msg))!=None)
						x,t=msg.split(":")
						global timer
						timer=int(t)
						t=int(t)
						# print("Gonna wait for ",t) 
						waiting=0 
						while timer>=0:
							waiting=waiting+1
							time.sleep(1) 
						print("waited this time")
						d = "Waited for "+str(waiting)+" seconds" 
						data = pickle.dumps(d)
						self.s.send(data)
						self.conn=1 
					elif(msg==200):
						d=200
						data = pickle.dumps(d)
						self.s.send(data) 
						self.conn=1
				except Exception as e:  
					# print(e)
					self.conn=0
t=myThread()
t.start()
wait_timer=timer_display(t)
wait_timer.start() 