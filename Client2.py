import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup
from CommonLibrary import Parse
from CommonLibrary import handler





def Server(socketSet,first, localState):
	while first[0] == 1:
		time.sleep(1)
	conn = serverSetup('',8888)
	socketSet.append(conn)
	first[0] = 1

	#finish setting up and start actual work here
	while 1:
		time.sleep(1)
	# end actual work here
	




	conn.close()








def Client(socketSet,first, localState):
	s = clientSetup('',6666)
	socketSet.append(s)
	socketSet.append(s)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)

	conn1 = socketSet[0]
	conn2 = socketSet[2]
	existedDecision = []

	dataTokenQueue = []
	count = 1
	#finish setting up and start actual work here
	while 1:
		print("round " + str(count) )
		count += 1
		try:
			data = conn1.recv(1024)
			data = data.decode("utf-8")
			print("client1 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision)
		except socket.timeout: 
			handler(socketSet, localState, dataTokenQueue, existedDecision)

		try:
			data = conn2.recv(1024)
			data = data.decode("utf-8")
			print("client3 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision)
		except socket.timeout: 
			handler(socketSet, localState, dataTokenQueue, existedDecision)



	# end actual work here




	s.close()


socketSet = []
first = [1]
localState = [0,1,-1,0,-1,0,0,2,0]


S = threading.Thread(target = Server, args = (socketSet,first, localState))
C = threading.Thread(target = Client, args = (socketSet,first, localState))
S.start()
C.start()
S.join()
C.join()
