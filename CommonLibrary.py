import threading
import socket
import time
import sys, select

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





