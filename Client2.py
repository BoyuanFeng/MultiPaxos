import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup
from CommonLibrary import Parse
from CommonLibrary import handler
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout)





def Server(socketSet,first, localState, requestQueue):
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








def Client(socketSet,first, localState, requestQueue):
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
			print("client3 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
		except socket.timeout: 
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)



	# end actual work here




	s.close()


socketSet = []
first = [1]
localState = [0,2,-1,0,-1,0,0,2,0,0,0,100]

requestQueue = [[1,1],[3,1],[5,2],[7,1],[9,3]]


S = threading.Thread(target = Server, args = (socketSet,first, localState, requestQueue))
C = threading.Thread(target = Client, args = (socketSet,first, localState, requestQueue))
S.start()
C.start()
S.join()
C.join()
