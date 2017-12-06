import socket,traceback,threading
import os,sys,time
import socket

def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.bind(('', 5555))  
    sock.listen(5)  
    while True:  
        try :
            connection,address = sock.accept()  
            buf = connection.recv(1024)  
            print "recv data from Client1", buf
            connection.send(buf)    
            connection.close()
        except :
            traceback.print_exc()


def doConnect(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :         
        sock.connect((host,port))
    except :
        pass 
    return sock
        
def Client():   
    host,port = '',6666
    print host,port    
    sockLocal = doConnect(host,port)   
    
    while True :
        try :
            msg = str(time.time())
            sockLocal.send(msg) 
            print "send msg ok (Client2): ",msg                
            print "recv data from (server2):",sockLocal.recv(1024)
        except socket.error :
            print "\r\nsocket error,do reconnect "
            time.sleep(3)
            sockLocal = doConnect(host,port)   
        except :
            print '\r\nother error occur '            
            time.sleep(3) 
        time.sleep(1)

if __name__ == "__main__" :
    
    print "Server2 up"
    S1 = threading.Thread(target = server, args = ())
    S2 = threading.Thread(target = Client, args = ())
    S1.start()
    S2.start()
    S1.join()
    S2.join()