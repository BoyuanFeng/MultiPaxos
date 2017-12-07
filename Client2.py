import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup
from CommonLibrary import Parse
from CommonLibrary import handler
from CommonLibrary import doConnect


dataTokenQueue = []
existedDecision = []
requestQueue = [1,3,5,7,9]



def Server(socketSet,first, localState,dataTokenQueue,existedDecision,requestQueue):
	while first[0] == 1:
		time.sleep(1)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.settimeout(1)  
	sock.bind(('', 8888))  
	sock.listen(5)  
	sock.settimeout(1)  
	while 1:
		try:
			conn,address = sock.accept()  
			break
		except:
			pass
			
	socketSet.append(conn)
	first[0] = 1
	conn2 = socketSet[2]

	#finish setting up and start actual work here
	while 1:
		time.sleep(1)
		try:
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
			data = conn2.recv(1024)
			data = data.decode("utf-8")
			if data == "":
				conn2.send("g".encode("utf-8"))
			print("client3 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
		except socket.timeout:
			try:
				handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
			except:
				pass
		except socket.error: 
			print("\r\nsocket error1,do reconnect ")
			conn2.close()
			while 1:
				try:
					conn2,address = sock.accept()  
					break
				except:
					pass
			socketSet[2] = conn2
		





def Client(socketSet,first, localState,dataTokenQueue,existedDecision,requestQueue):
	host,port = '',6666
	s = doConnect(host,port)   
	socketSet.append(s)
	socketSet.append(s)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)

	conn1 = socketSet[0]

	count = 1
	#finish setting up and start actual work here
	while 1:
		time.sleep(1)

		print("round " + str(count) )
		count += 1
		try:
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
			data = conn1.recv(1024)
			data = data.decode("utf-8")
			print("client1 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
		except socket.timeout:
			try:
				handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
			except:
				pass
		except socket.error: 
			print("\r\nsocket error2,do reconnect ")
			time.sleep(3)
			conn1 = doConnect(host,port)   
			socketSet[0] = conn1
		

	# end actual work here




socketSet = []
first = [1]
localState = [0,1,-1,0,-1,0,0,1,0,0,0,100]

S = threading.Thread(target = Server, args = (socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue))
C = threading.Thread(target = Client, args = (socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue))
S.start()
C.start()
S.join()
C.join()
