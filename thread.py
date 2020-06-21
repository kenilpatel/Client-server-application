import threading
import time
class myThread(threading.Thread):
    def __init__(self,s,name):
        threading.Thread.__init__(self)
        self.s=s
        self.name=name
    def run(self):
        c, addr = self.s.accept()
        while (True):
            try:
                msg = "server data"
                data = pickle.dumps(msg)
                c.send(data)
                msg = pickle.loads(c.recv(1024))
                print(msg)
            except Exception as e:
                print(e)

def handle_client(str):
    count=0
    while True:
        print(str)
t=myThread("kp","client2")
t.start()
t=myThread("kp","client3")
t.start()
t=myThread("kp","client1")
t.start()