import os
import socket
import pickle
import time
import cv2
from sys import getsizeof

def client():
	cwd = os.getcwd()

	# host = '18.144.8.14'  # edge public ipv4 address
	# port =  65009

	host = socket.gethostname()  # get local machine name
	port = 8081

	print('Connecting to '+ host)

	s = socket.socket()
	s.connect((host, port))
  
	
	cap = cv2.VideoCapture('1.mp4')
	frames = getFrames(cap)
	  
	for f in frames:
		size = getsizeof(f)
	 	# print(getsizeof(f)) this size is used in the condition len(frame) >= ... in the server
		if getsizeof(f) != size:
			s.close()
			break
			
		else:
			# print(f'the size is {size}')
			# s.send(pickle.dumps(size))
			s.send(pickle.dumps(f))

		data = pickle.loads(s.recv(1024))
		# print('Received from server:', data)

	s.close()

def getFrames(cap):
	frames = list()
	while(cap.isOpened()):
		ret, frame = cap.read()
		frames.append(frame)
		if ret == False:
			break
 
	cap.release()
	return frames

if __name__ == '__main__':
	client()