import os,sys,time
import socket
import threading

def doConnect(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :         
        sock.connect((host,port))
    except :
        pass 
    return sock
        
def Client():   
    host,port = '',5555
    print host,port    
    sockLocal = doConnect(host,port)   
    
    while True :
        try :
            msg = str(time.time())
            sockLocal.send(msg) 
            print "send msg ok (Client1): ",msg                
            print "recv data from (server1):",sockLocal.recv(1024)
        except socket.error :
            print "\r\nsocket error,do reconnect "
            time.sleep(3)
            sockLocal = doConnect(host,port)   
        except :
            print '\r\nother error occur '            
            time.sleep(3) 
        time.sleep(1)

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.bind(('', 6666))  
    sock.listen(5)  
    while True:  
        try:
            connection,address = sock.accept()  
            buf = connection.recv(1024)  
            print "recv data from Client2", buf
            connection.send(buf)    
            connection.close()
        except :
            traceback.print_exc()
    
if __name__ == "__main__" :

    print "Server1 up"
    S1 = threading.Thread(target = server, args = ())
    S2 = threading.Thread(target = Client, args = ())
    S1.start()
    S2.start()
    S1.join()
    S2.join()
    