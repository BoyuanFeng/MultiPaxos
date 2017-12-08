import threading
import socket
import time
import sys, select
import random

#layout of localState:
#   [0,			0,    0,      		   0,       	     0,           0, 		
#	 ballotNum. myId. accepted ballot. accepted value.   leaderId.    time slience	
#	 0          1      2       	       3        	     4            5       
#
#	 0,        						0,
#    current acknowledge number		number of majority
#	 6		   						7
#

# socketSet = [s1, s2, s3, ..., sn]

def broadcast(socketSet, myId, message):
	myId = int(myId)
	for i in range(len(socketSet)):
		if i != myId:
			try:
				socketSet[i].send(message.encode('utf-8'))
			except:
				pass


def applyForLeader(socketSet, localState):
	print("apply for leader")
	writeToLog(localState,"apply for leader")

	localState[0] += random.randint(1,10)  #ballotNum += 1
	message = "p,"+str(localState[0])+","+str(localState[1])
	broadcast(socketSet, localState[1], message)

def respondPrepare(socketSet, localState, potentialLeader, bal):
	potentialLeader = int(potentialLeader)
	bal = int(bal)
	if bal > localState[0]:
		localState[4] = potentialLeader
		localState[0] = bal
		message = "ac,"+str(bal)+","+str(localState[3])+","+str(localState[2])
		message = message.encode('utf-8')
		socketSet[potentialLeader].send(message)

#existedDecision = [[bal, val],[bal, val],[bal, val],[bal, val]]



def leaderRespondAck(socketSet, localState, theirBal, existedDecision):
	print("enter ack")
	theirBal = int(theirBal)
	s111 = "leaderRespondAck: myBal is " + str(localState[0]) + ", theirBal is " + str(theirBal) + "\n"
	writeToLog(localState,s111)

	if theirBal != localState[0]:
		print("clear previous leader bal")
		localState[6] = 0
		return
	localState[6] += 1		# ls[6]: current acknowledge number
	s111 = "current acknowledge number is " + str(localState[6]) + "\n"
	writeToLog(localState,s111)
	print("localState[6] is " + str(localState[6]) + ", localState[7] is " + str(localState[7]))
	if localState[6] < localState[7]:	# ld[7]: number of majority
		return
	else:
		print("I am THE leader!!!, my bal is " + str(localState[0]))
		s111 = "I am THE leader!!!, my bal is " + str(localState[0]) + "\n"
		writeToLog(localState,s111)		
		localState[4] = localState[1]	# ls[4]: current leader id, ls[1] is myId
		localState[6] = 0

def leaderSuggest(socketSet, localState, existedDecision, requestQueue):
	
	if localState[9] >= len(requestQueue):
		time.sleep(1)
		return
	myValue = requestQueue[localState[9]]


	if localState[4] != localState[1]:
		return
	s111 = "requestCount is " + str(localState[9]) + ", myValue is " + str(myValue) + "\n"
	writeToLog(localState,s111)		
	
	myValue = int(myValue)

	if localState[10] != 0:
		return
	else:
		localState[10] = 1


	flag = 0
	for i in range(len(existedDecision)):
		#print("existedDecision[i]")
		if int(existedDecision[i][1]) != -1:
			flag = 1
			break
	
	if flag == 0:
		# no decision already
		message = "a1,"+str(localState[0])+","+str(myValue)
		broadcast(socketSet, localState[1], message)
	else:
		# has decision now
		val = existedDecision[0][1]
		bal = existedDecision[0][0]
		for decision in existedDecision:
			if decision[0] > bal:
				bal = decision[0]
				val = decision[1]
		myValue = val
		message = "a1,"+str(localState[0])+","+str(myValue)
		broadcast(socketSet, localState[1], message)
	s111 = "leaderRespondAck: the message is " + message + "\n"
	writeToLog(localState,s111)		
	existedDecision.clear()


def followerRespondAc(socketSet, localState, receivedBal, receivedVal, leaderId):
	receivedBal = int(receivedBal)
	leaderId = int(leaderId)
	if receivedBal >= localState[0]:
		localState[0] = receivedBal
		localState[5] = 0
		localState[2] = receivedVal
		localState[4] = leaderId
		s111 = "leader is " + str(localState[4]) + "\n"
		writeToLog(localState,s111)				
		message = "a2,"+str(receivedBal)+","+str(receivedVal)
		message = message.encode('utf-8')
		socketSet[leaderId].send(message)
	
def writeToLog(localState,s1):
		if localState[1] == 0:
			with open("log0.txt", "a") as myfile:
				myfile.write(s1)
		if localState[1] == 1:
			with open("log1.txt", "a") as myfile:		
				myfile.write(s1)
		if localState[1] == 2:
			with open("log2.txt", "a") as myfile:
				myfile.write(s1)
		if localState[1] == 3:
			with open("log3.txt", "a") as myfile:
				myfile.write(s1)
		if localState[1] == 4:
			with open("log4.txt", "a") as myfile:
				myfile.write(s1)

def leaderDecide(socketSet, localState, bal, val, requestQueue):
	bal = int(bal)
	val = int(val)
	if localState[4] != localState[1]:
		return # I am not a leader now
	localState[8] += 1
	if localState[9] >= len(requestQueue):
		return
	if localState[8] >= localState[7] and val == requestQueue[localState[9]]:
		localState[2] = val
		localState[3] = val
		broadcast(socketSet, localState[1],"a3,"+str(bal)+","+str(val))
		s111 = "leader decided: final value is " + str(val) + ", final bal is " + str(bal) + "\n"
		writeToLog(localState, s111)
		print(s111)
		localState[11] -= val
		localState[10] = 0
		localState[8] = 0
		localState[9] += 1
		s1 = "val: " + str(val) + ", bal: " + str(bal) + ", ticket is: " + str(localState[11]) + "\n"
		writeToLog(localState,s1)


	else:
		localState[8] = 0


def participantDecide(localState, bal, val):
	bal = int(bal)
	val = int(val)
	if bal >= localState[0]:
		localState[2] = val
		localState[3] = bal
		s111 = "decided: final value is " + str(val) + ", final bal is " + str(bal) + "\n"
		writeToLog(localState, s111)
		print(s111)
		localState[11] -= val
		s1 = "val: " + str(val) + ", bal: " + str(bal) + ", ticket is: " + str(localState[11]) + "\n"
		writeToLog(localState,s1)


def heartBeat(socketSet, localState):
	if localState[4] == localState[1]:
		#print("send heart beat, myId is " + str(localState[1]) + ", myBal is " + str(localState[0]))
		broadcast(socketSet, localState[1], "h,"+str(localState[1])+","+str(localState[0]))

def receiveHeart(localState, leaderId, leaderBal):
	#print("received heart beat, leaderId = " + str(leaderId) + ", leaderBal = " + str(leaderBal) )
	leaderId = int(leaderId)
	leaderBal = int(leaderId)
	if leaderBal >= localState[0]:
		localState[4] = leaderId
		localState[5] = 0
	
def receiveRequest(suggestedVal,requestQueue, localState):
	print("enter receive request")
	suggestedVal = int(suggestedVal)
	if localState[4] == localState[1]:
		requestQueue.append(suggestedVal)

# applyForLeader: non-leader now. want to become leader. DO: receive nothing, send "p"
# (socketSet, localState)

# respondPrepare: non-leader now. DO: receive "p", reply "ac"
# (socketSet, localState, potentialLeader, bal)

# leaderRespondAck: non-leader now. Become leader now. DO: receive "ac", calculate current # of "ac". send "a1"
# (socketSet, localState, existedDecision, myValue)
# existedDecision = [[bal, val],[bal, val],[bal, val],[bal, val]]

# followerRespondAc: non-leader now. agree with the value proposed by leader DO: receive "a1", send "a2"
# (socketSet, localState, receivedBal, receivedVal, leaderId)

# leaderDecide: leader now. received ("accept",b,c) from majority, decide value now.
# DO: receive "a2", send "a3"
# (socketSet, localState, bal, val)

# participantDecide: participant now. received ("a3", bal, num) from majority, decide value now


def handler(socketSet, localState, dataTokenQueue, existedDecision, requestQueue):
	localState[5] += 1
	if localState[4] != localState[1]:
		requestQueue.clear()
	if localState[4] == localState[1]:
		localState[5] = 0
	if localState[1] == 0 and localState[5] > 10 and localState[5] < 40:
		#print("silence time is " + str(localState[5]) + ", ballotNum is " + str(localState[0]))
		localState[5] = 0
		applyForLeader(socketSet, localState)
	if localState[1] == 1 and localState[5] >= 40 and localState[5] < 70:
		#print("silence time is " + str(localState[5]) + ", ballotNum is " + str(localState[0]))
		localState[5] = 0
		applyForLeader(socketSet, localState)
	if localState[1] == 0 and localState[5] >= 70:
		#print("silence time is " + str(localState[5]) + ", ballotNum is " + str(localState[0]))
		localState[5] = 0
		applyForLeader(socketSet, localState)



	heartBeat(socketSet, localState)
	leaderSuggest(socketSet, localState, existedDecision, requestQueue)
	for tokens in dataTokenQueue:
		if tokens == '':
			pass
		if tokens[0] == 'p':
			respondPrepare(socketSet, localState, tokens[2], tokens[1])
		elif tokens[0] == 'ac':
			existedDecision.append([tokens[2],tokens[3]])
			# here 0 could be replaced by any value proposed by client
			leaderRespondAck(socketSet, localState, tokens[1], existedDecision)#1 is leader's choice
			if localState[9] >= len(requestQueue):
				continue
			print("here")
			leaderSuggest(socketSet, localState, existedDecision, requestQueue)
		elif tokens[0] == 'a1':
			followerRespondAc(socketSet, localState, tokens[1], tokens[2], localState[4])
		elif tokens[0] == 'a2':
			leaderDecide(socketSet, localState, tokens[1], tokens[2], requestQueue)
		elif tokens[0] == 'a3':
			participantDecide(localState, tokens[1], tokens[2])
		elif tokens[0] == 'h':
			receiveHeart(localState, tokens[1], tokens[2]);
		elif tokens[0] == 'r':
			receiveRequest(tokens[1],requestQueue, localState)
	dataTokenQueue.clear()



def separateData(data,dataQueue):
	begin = 0	
	for i in range(len(data)):
		if data[i] == 'p':
			begin = i
			i += 1
			while i < len(data) and data[i] != 'p' and data[i] != 'a' and data[i] != 'h' and data[i] != 'g' and data[i] != 'r':
				i += 1
			dataQueue.append(data[begin:i])
			i -= 1
		if data[i] == 'a':
			begin = i
			i+=1
			while i < len(data) and data[i] != 'p' and data[i] != 'a' and data[i] != 'h' and data[i] != 'g' and data[i] != 'r':
				i += 1
			dataQueue.append(data[begin:i])
			i -= 1
		if data[i] == 'h':
			begin = i
			i+=1
			while i < len(data) and data[i] != 'p' and data[i] != 'a' and data[i] != 'h' and data[i] != 'g' and data[i] != 'r':
				i += 1
			dataQueue.append(data[begin:i])
			i -= 1
		if data[i] == 'g':
			pass
		if data[i] == 'r':
			begin = i
			i+=1
			while i < len(data) and data[i] != 'p' and data[i] != 'a' and data[i] != 'h' and data[i] != 'g' and data[i] != 'r':
				i += 1
			dataQueue.append(data[begin:i])
			i -= 1


def extractData(s):
	tokens = []
	if s[0] == 'p':
		tokens.append("p")
		begin = 2		
		i = 2
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])	
		return tokens


	elif s[0] == 'a' and s[1] == '1':
		tokens.append("a1")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])	
		return tokens


	elif s[0] == 'a' and s[1] == '2':
		tokens.append("a2")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])	
		return tokens


	elif s[0] == 'a' and s[1] == '3':
		tokens.append("a3")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])	
		return tokens

	elif s[0] == 'a' and s[1] == 'c':
		tokens.append("ac")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])	
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])	
		return tokens
	elif s[0] == 'h':
		tokens.append("h")
		begin = 2
		i = 2
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])	
		return tokens
	elif s[0] == 'r':
		tokens.append("r")
		begin = 2
		i = 2
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(s[begin:i])
		i += 1
		return tokens


def Parse(data):
	dataQueue = []
	separateData(data,dataQueue)
	dataQueue1 = []
	for s in dataQueue:
		dataQueue1.append(extractData(s))
	return dataQueue1






def serverSetup(host,port):
	#print "enter server"
	HOST = host
	PORT = port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST,PORT))	
	s.listen(1)
	conn,addr = s.accept()
	conn.settimeout(1)
	#print "server setup"
	return conn

def clientSetup(host,port):
	#print "enter client"

	HOST = host
	PORT = port
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.settimeout(1)

	#print "client setup"
	return s


def doConnect(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  
    try :         
        sock.connect((host,port))
    except :
        pass 
    return sock

def requestToLeader(socketSet, localState, suggestedVal):
	message = "r,"+str(suggestedVal)
	broadcast(socketSet, localState[1], message)
	print("sent request " + str(message))


def handleInput(socketSet, localState, requestQueue):
	i, o, e = select.select( [sys.stdin], [], [], 1 )
	if (i):
		MyWord = sys.stdin.readline().strip()
		print(MyWord)
		if len(MyWord) == 0:
			return
		if MyWord == "show":
			print("current ticket number is " + str(localState[11]))
		elif MyWord[0] == 'b' and MyWord[1] == 'u' and MyWord[2] == 'y':
			print("enter buy")
			num = ""
			wordI = 4
			while wordI < len(MyWord):
				num += MyWord[wordI]
				wordI += 1
			num = int(num)
			if localState[1] == localState[4]:
				requestQueue.append(num)
			else:
				requestToLeader(socketSet, localState, num)		



