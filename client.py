import os
import sys
from socket    import *
from threading import Thread
from time      import strftime as curTime
from typing import final


try:
	HOST, PORT = sys.argv
except:
	print("Invalid cmd line options.")
	HOST, PORT = "localhost", 4444
	#HOST, PORT = str(input("Host: ")), int(input("Port: "))


def printConsole():
	cmnd = 'clear'
	if os.name in ('nt', 'dos'):
		cmnd = 'cls'
	os.system(cmnd)

	print(*log, sep='\n')

def recvMsg():
	while True:
		try:
			msg = s.recv(2048).decode("utf-8")
			if msg:
				log.append(f"[{curTime('%H:%M')}]{msg}")
				printConsole()
		except:
			continue
		

if __name__ == '__main__':
	s = socket(AF_INET, SOCK_STREAM)
	s.connect((HOST, PORT))

	Thread(target=recvMsg)
	log = [f"Connected to {HOST}:{PORT}"]
	printConsole()
	
	while True:
		try:
			msg = input(f"[{curTime('%H:%M')}]<127.0.0.1>:")
			if msg:
				log.append(f"[{curTime('%H:%M')}]<127.0.0.1>:{msg}")
				printConsole()
				s.send(msg.encode("utf-8"))
		except:
			continue

	s.close()