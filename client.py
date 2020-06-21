import socket
import pickle
s=socket.socket()
port=7398
conn=0 
while(True):
	if(conn==0):
		try:
			s.connect(("127.0.0.1",port))
			conn=1
		except Exception as e:
			conn=0
			print("Server is not available at this moment")
	try:
		msg=pickle.loads(s.recv(1024))
		print(msg)
		if(msg==-1):
			print("server is full") 
		msg = "client data"
		data = pickle.dumps(msg)
		s.send(data)
	except Exception as e:
		print("Server is not available at this moment") 
		conn=0
	
