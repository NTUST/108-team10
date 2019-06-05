import time 
import socket
import sys
def doRequest():
    sock = socket.socket()
    sock.connect(('www.baidu.com',80))
    sock.send("GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: Close\r\n\r\n".encode("utf-8"))
    response = sock.recv(1024)
    return response
def main():
    start = time.time()
    for i in range(int(sys.argv[1])):
        doRequest()
        print("spend time : %s" %(time.time()-start))
main()