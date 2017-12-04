
# socketSet = [s1, s2, s3, ..., sn]

def broadcast(socketSet, myId, message):
	for i in range(len(socketSet):
		if i != myId:
			socketSet[i].send(message)
	


def applyForLeader(socketSet, localState):
	localState[0] += 1  #ballotNum += 1
	message = "p,"+str(localState[0])+","+str(localState[1])
	broadcast(socketSet, myId, message)

def respondPrepare(socketSet, localState, potentialLeader, bal):
	if bal >= localState[0]:
		localState[4] = potentialLeader
		localState[0] = bal
		socketSet[potentialLeader].send("ac,"+str(bal)+","+str(localState[3])+","+str(localState[2]))

#existedDecision = [[bal, val],[bal, val],[bal, val],[bal, val]]



def leaderRespondAck(socketSet, localState, existedDecision, myValue):
	localState[6] += 1		# ls[6]: current acknowledge number
	if localState[6] < localState[7]:	# ld[7]: number of majority
		return
	else:
		localState[4] = localState[1]	# ls[4]: current leader id, ls[1] is myId
		int flag = 0
		for i in range(len(existedDecision)):
			if existedDecision[i] != -1:
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


def followerRespondAc(socketSet, localState, receivedBal, receivedVal, leaderId):
	if receivedBal >= localState[0]:
		localState[0] = receivedBal
		localState[1] = receivedVal
		socketSet[leaderId].send("a2,"+str(receivedBal)+","+str(receivedVal))
		

def leaderDecide(socketSet, localState, bal, val):
	broadcast(socketSet, localState[1],"a3,"+str(bal)+","+str(val))


def heartBeat(socketSet, localState):
	if localState[5] == 1:
		broacast(socketSet, localState[1], "h,"+str(localState[1]))

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



def handler(socketSet, localState, dataTokenQueue):
	if localState[1] == localState[4]:
		# I am leader
		
	else:
		# I am non-leader
		
		# Part I: process all data in dataTokenQueue
		for tokens in dataTokenQueue:
			if tokens[0] == 'p':
				respondPrepare(socketSet, localState, tokens[2], tokens[1])
			elif tokens[0] == 'ac':
				existedDecision.append([tokns[2],tokens[3]])
				# here 0 could be replaced by any value proposed by client
				leaderRespondAck(socketSet, localState, existedDecision, 0)
			elif tokens[0] == 'a1':
				followerRespondAc(socketSet, localState, tokens[1], tokens[2], localState[4])
			elif tokens[0] == 'a2':
				continue # I am not leaders
			elif tokens[0] == 'a3':
				continue
		
		# Part II: test whether leader is alive. If so, apply for leader
		if localState[5] > 5:
			localState[5] = 0
			applyForLeader(socketSet, localState)



def separateData(data,dataQueue):
	begin = 0	
	for i in range(len(data)):
		if data[i] == 'p':
			begin = i
			i += 1
			while i < len(data) and data[i] != 'p' and data[i] != 'a':
				i += 1
			dataQueue.append(data[begin:i])
			i -= 1
		if data[i] == 'a':
			begin = i
			i+=1
			while i < len(data) and data[i] != 'p' and data[i] != 'a':
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
		tokens.append(data[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])	
		return tokens


	elif s[0] == 'a' and s[1] == '1':
		tokens.append("a1")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])	
		return tokens


	elif s[0] == 'a' and s[1] == '2':
		tokens.append("a2")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])	
		return tokens


	elif s[0] == 'a' and s[1] == '3':
		tokens.append("a3")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])	
		return tokens

	elif s[0] == 'a' and s[1] == 'c':
		tokens.append("ac")
		begin = 3		
		i = 3
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])	
		i += 1
		begin = i	
		while i < len(s) and s[i] != ',':
			i += 1
		tokens.append(data[begin:i])	
		return tokens

