import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup

def Client1(socketSet,first):
	s = clientSetup('',7777)
	socketSet.append(s)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)

	conn1 = socketSet[0]
	conn2 = socketSet[1]



	#finish setting up and start actual work here
	while 1:
		try:
			data = conn1.recv(1024)
			print("client3 received: " + data)
		except socket.timeout: 
			conn1.send("From client3: good")

		try:
			data = conn2.recv(1024)
			print("client3 received: " + data)
		except socket.timeout: 
			conn2.send("From client3: good")


	#end actual work here

	s.close()





def Client2(socketSet,first):
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





first = [1]
socketSet = []

Store = [0]




	
print 'Client3'


C1 = threading.Thread(target = Client1, args = (socketSet,first))
C2 = threading.Thread(target = Client2, args = (socketSet,first))
C1.start()
C2.start()
C1.join()
C2.join()
