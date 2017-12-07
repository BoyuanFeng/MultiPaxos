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
    count = 0
    while True :
        try :
            count += 1
            msg = str(count)
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

    
if __name__ == "__main__" :

    print "Server1 up"
    S2 = threading.Thread(target = Client, args = ())
    S2.start()
    S2.join()
    
