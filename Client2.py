import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup





def Server(socketSet,first):
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








def Client(socketSet,first):
	s = clientSetup('',6666)
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
			print("client2 received: " + data)
		except socket.timeout: 
			conn1.send("From client2: good")

		try:
			data = conn2.recv(1024)
			print("client2 received: " + data)
		except socket.timeout: 
			conn2.send("From client2: good")

	# end actual work here




	s.close()












Store = [0]





print 'Client2'
first = [1]


S = threading.Thread(target = Server, args = (socketSet,first))
C = threading.Thread(target = Client, args = (socketSet,first))
S.start()
C.start()
S.join()
C.join()
