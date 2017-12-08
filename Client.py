import threading
import socket
import time
import sys, select
from CommonLibrary import serverSetup
from CommonLibrary import clientSetup
from CommonLibrary import Parse
from CommonLibrary import handler
from CommonLibrary import writeToLog
from CommonLibrary import handleInput

dataTokenQueue = []
existedDecision = []
requestQueue = []
localState = [0,0,-1,0,-1,0,0,1,0,0,0,100]
lock = threading.Lock()

def Server1(addressSet):
	global localState, dataTokenQueue, existedDecision, requestQueue	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.bind((addressSet[localState[1]][0],addressSet[localState[1]][1]))  
	sock.listen(100)  
	sock.settimeout(1)  
	heartCount = 0
	while 1:
		try:
			time.sleep(.05)			
			conn1,address = sock.accept()  
			conn1.settimeout(1)
			try:
				data = conn1.recv(1024)
				data = data.decode("utf-8")
				if len(data) > 0 and data[0] == 'h':
					heartCount += 1
					if heartCount % 5 == 0:
						print("received: " + data)
						heartCount = 0
				else:
					print("received: " + data)

				lock.acquire()
				dataTokenQueue = Parse(data)
				handler(addressSet, localState, dataTokenQueue, existedDecision, requestQueue)
				lock.release()

			except socket.error:
				pass
		except socket.error:
			pass
	

def Server2(addressSet):
	global localState, dataTokenQueue, existedDecision, requestQueue	
	count = 1
	while 1:
		time.sleep(.051)	
		if count % 5 == 0:				
			print("round " + str(count/5) )
		count += 1
		lock.acquire()
		handleInput(addressSet, localState, requestQueue)
		#print(len(requestQueue))
		handler(addressSet, localState, dataTokenQueue, existedDecision, requestQueue)
		lock.release()



if len(sys.argv) != 2:
	print("input invalid")
	sys.exit(1)
localState[1] = int(sys.argv[1])
if localState[1] == 3 or localState[1] == 4:
	localState[7] = 2

addressSet = [['',6666],['',7777],['',8888],['',9000],['',9999]]

S1 = threading.Thread(target = Server1, args = (addressSet,))
S2 = threading.Thread(target = Server2, args = (addressSet,))
S1.start()
S2.start()
S1.join()
S2.join()
