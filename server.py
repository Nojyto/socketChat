import sys
from socket    import *
from threading import Thread
from time      import strftime as curTime


MAXUSERS = 10
try:
	HOST, PORT = sys.argv
except:
	print("Invalid cmd line options.")
	HOST, PORT = "localhost", 4444
	#HOST, PORT = str(input("Host: ")), int(input("Port: "))


def clientThread(conn, addr):
	while True:
		try:
			msg = conn.recv(2048).decode("utf-8")
			if msg:
				msg = f"[{curTime('%H:%M')}]<{addr[0]}>:{msg}"
				print(msg)
				broadcast(msg, conn)
		except:
			continue
 
def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode("utf-8"))
            except:
                client.close()
                if sender in clients:
                    clients.remove(sender)
                    broadcast(f"[{curTime('%H:%M')}]<Server>: {addr[0]} has disconnected", conn)


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
    s.bind((HOST, PORT))
    s.listen(MAXUSERS)
    
    clients = []

    try:
        print(f"[{curTime('%H:%M')}]<Server>Server started on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            print(f"[{curTime('%H:%M')}]<Server>: {addr[0]} has connected.")
            Thread(target=clientThread, args=(conn, addr)).start()
    except:
        print("Exiting...")
    finally:
        s.close()