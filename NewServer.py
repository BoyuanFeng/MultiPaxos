import socket,traceback,threading
import os,sys,time
import socket

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.bind(('', 5555))  
    sock.listen(5)  
    connection,address = sock.accept()  
    while True:  
        try :
            buf = connection.recv(1024)
            if buf == "":
                connection.close()
                connection,address = sock.accept()
				 
            print "recv data from Client1", buf
            connection.send(buf)    
        except :
            connection.close()
            connection,address = sock.accept()
            pass


def doConnect(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :         
        sock.connect((host,port))
    except :
        pass 
    return sock
        
if __name__ == "__main__" :
    
    print "Server2 up"
    S1 = threading.Thread(target = server, args = ())
    S1.start()
    S1.join()
 
