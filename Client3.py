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


def Client1(socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue):
	host,port = '',7777
	s = doConnect(host,port)   
	socketSet.append(s)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)
	socketSet.append(s)

	conn1 = socketSet[0]

	count = 1
	#finish setting up and start actual work here
	while 1:
		time.sleep(1)
		print("round " + str(count) )
		count += 1
		try:
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
			print("\r\nsocket error1,do reconnect") 
			time.sleep(3)
			conn1 = doConnect(host,port)   
			socketSet[0] = conn1


	#end actual work here





def Client2(socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue):
	while first[0] == 1:
		time.sleep(1)
	host,port = '',8888
	s = doConnect(host,port)   
	socketSet.append(s)
	first[0] = 1

	conn2 = socketSet[1]


	#finish setting up and start actual work here
	while 1:
		#localLock.acquire()
		time.sleep(1)
		#localLock.release()
		try:
			data = conn2.recv(1024)
			data = data.decode("utf-8")
			print("client2 received: " + data)
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
			conn2 = doConnect(host,port)   
			socketSet[0] = conn2




socketSet = []
first = [1]
localState = [0,2,-1,0,-1,0,0,1,0,0,0,100]


C1 = threading.Thread(target = Client1, args = (socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue))
C2 = threading.Thread(target = Client2, args = (socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue))
C1.start()
C2.start()
C1.join()
C2.join()
