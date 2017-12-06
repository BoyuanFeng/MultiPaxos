import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup
from CommonLibrary import Parse
from CommonLibrary import handler

def Client1(socketSet,first, localState):
	s = clientSetup('',7777)
	socketSet.append(s)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)
	socketSet.append(s)

	conn1 = socketSet[0]
	conn2 = socketSet[1]

	existedDecision = []

	count = 1
	dataTokenQueue = []
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
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)

		try:
			data = conn2.recv(1024)
			data = data.decode("utf-8")
			print("client2 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
		except socket.timeout: 
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)


	#end actual work here

	s.close()





def Client2(socketSet,first, localState):
	while first[0] == 1:
		time.sleep(1)
	s = clientSetup('',8888)
	socketSet.append(s)
	first[0] = 1



	#finish setting up and start actual work here
	while 1:
		#localLock.acquire()
		time.sleep(1)
		#localLock.release()
		# end actual work here


	s.close()




socketSet = []
first = [1]
localState = [0,2,-1,0,-1,0,0,2,0,0,0]

requestQueue = [1,3,5,7,9]

C1 = threading.Thread(target = Client1, args = (socketSet,first, localState))
C2 = threading.Thread(target = Client2, args = (socketSet,first, localState))
C1.start()
C2.start()
C1.join()
C2.join()
