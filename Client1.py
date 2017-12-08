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


def Server1(socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.bind(('', 6666))  
	sock.listen(1)  
	sock.settimeout(1)  
	while 1:
		try:
			conn,address = sock.accept()  
			break
		except:
			pass

	socketSet.append(conn)
	socketSet.append(conn)
	first[0] = 0
	while first[0] == 0:
		time.sleep(1)
	conn1 = socketSet[1]
	conn2 = socketSet[2]

	#finish setting up and start actual work here
	count = 1
	while 1:
		conn1.settimeout(1)
		time.sleep(1)

		print("round " + str(count) )
		count += 1
		try:
			data = conn1.recv(1024)
			data = data.decode("utf-8")
			if data == "":
				conn1.send("g".encode("utf-8"))
			print("client2 received: " + data)
			dataTokenQueue = Parse(data)
			handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
		except socket.timeout:
			try:
				handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue)
			except:
				pass
		except socket.error: 
			print("\r\nsocket error1,do reconnect ")

			conn1.close()
			while 1:
				try:
					conn1,address = sock.accept()  
					break
				except:
					pass
			socketSet[1] = conn1
def Server2(socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue):
	while first[0] == 1:
		time.sleep(1)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.settimeout(5)  
	sock.bind(('', 7777))  
	sock.listen(1)  
	while 1:
		try:
			conn,address = sock.accept()  
			break
		except:
			pass
	socketSet.append(conn)
	first[0] = 1
	conn2 = socketSet[2]


	while 1:
		conn2.settimeout(1)
		time.sleep(1)
		try:
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
			print("\r\nsocket error2,do reconnect ")
			conn2.close()
			while 1:
				try:
					print("2: try to connect")
					conn2,address = sock.accept()  
					break
				except:
					pass
			socketSet[2] = conn2
		#localLock.acquire()
		#localLock.release()


localState = [0,0,-1,0,-1,0,0,1,0,0,0,100]

socketSet = []
first = [1]



S1 = threading.Thread(target = Server1, args = (socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue))
S2 = threading.Thread(target = Server2, args = (socketSet,first, localState, dataTokenQueue, existedDecision, requestQueue))
S1.start()
S2.start()
S1.join()
S2.join()
