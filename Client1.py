import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup
from CommonLibrary import Parse
from CommonLibrary import handler

def Server1(socketSet,first, localState):
	conn = serverSetup('',6666)
	socketSet.append(conn)
	socketSet.append(conn)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)
	conn1 = socketSet[1]
	conn2 = socketSet[2]


	dataTokenQueue = []
	requestQueue = [1,3,5,7,9]
	existedDecision = []
	#finish setting up and start actual work here
	count = 1
	while 1:
		time.sleep(1)

		print("round " + str(count) )
		count += 1
		try:
			

			data = conn1.recv(1024)
			data = data.decode("utf-8")
			print("client2 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
		except socket.timeout: 
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)

		try:
			data = conn2.recv(1024)
			data = data.decode("utf-8")
			print("client3 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
		except socket.timeout: 
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
	conn.close()


def Server2(socketSet,first, localState):
	while first[0] == 1:
		time.sleep(1)
	conn = serverSetup('',7777)
	socketSet.append(conn)
	first[0] = 1


	while 1:
		time.sleep(1)
		#localLock.acquire()
		#localLock.release()

	conn.close()

localState = [0,0,-1,0,-1,0,0,2,0,0,0]

socketSet = []
first = [1]



S1 = threading.Thread(target = Server1, args = (socketSet,first, localState))
S2 = threading.Thread(target = Server2, args = (socketSet,first, localState))
S1.start()
S2.start()
S1.join()
S2.join()
