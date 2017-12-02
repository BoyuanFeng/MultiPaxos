import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup

def Server1(socketSet,first):
	conn = serverSetup('',6667)
	socketSet.append(conn)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)

	conn1 = socketSet[0]
	conn2 = socketSet[1]

	#finish setting up and start actual work here
	while 1:
		try:
			data = conn1.recv(1024)
			print("client1 received: " + data)
		except socket.timeout: 
			conn1.send("From client1: good")

		try:
			data = conn2.recv(1024)
			print("client1 received: " + data)
		except socket.timeout: 
			conn2.send("From client1: good")

	# end actual work
	




	conn.close()
















def Server2(socketSet,first):
	while first[0] == 1:
		time.sleep(1)
	conn = serverSetup('',7777)
	socketSet.append(conn)
	first[0] = 1


	# work is done in server1. Nonsense here.
	while 1:
		time.sleep(1)
		#localLock.acquire()
		#localLock.release()	


	#end actual work here

	
	conn.close()



























socketSet = []
first = [1]

print 'Client1'

S1 = threading.Thread(target = Server1, args = (socketSet,first))
S2 = threading.Thread(target = Server2, args = (socketSet,first))
S1.start()
S2.start()
S1.join()
S2.join()
