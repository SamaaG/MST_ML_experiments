import os
import socket
import pickle 
import uuid
import string
import numpy as np
from random import choice
from random import randint

def get_age():
	return randint(1, 99)

def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(6))

def initializeDB(s):
	print("initialize a database...")
	id1 = str(uuid.uuid4())
	id2 = str(uuid.uuid4())

	data = {id1:{'name':get_random_string(), 'age': get_age()}, 
	        id2:{'name':get_random_string(), 'age':get_age()}}

	np.save('allUIDs', [id1, id2])

	data = pickle.dumps(data)
	s.send(data)

	data = pickle.loads(s.recv(1024))
	print('Received from server: ', data)


def client():
	cwd = os.getcwd()

	port = 65008
	host = '54.183.187.178'# edge   cloud '3.15.43.53' # cloud '54.183.187.178' # edge #'3.15.43.53'  cloud 
	print('Connecting to '+ host)

	s = socket.socket()
	s.connect((host, port))
  
	initializeDB(s)

	allUIDs = np.load(os.path.join(cwd,'allUIDs.npy'))

	txn_num = input('txn_num -> ')
	op_num = input('op_num -> ')
  

	for i in range(int(txn_num)):
		for j in range(int(op_num)):
			c = choice(['read', 'write'])
			print(f'the choice is {c}')
			if c == 'read':
				allUIDs = np.load(os.path.join(cwd,'allUIDs.npy'))
				idn = str(choice(allUIDs))
				s.send(pickle.dumps(idn))

			elif c == 'write':
				idn = str(uuid.uuid4())
				data = {idn:{'name': get_random_string(), 'age': get_age()}}

				allUIDs = np.append(allUIDs, [idn])
				np.save('allUIDs', allUIDs)
				s.send(pickle.dumps(data))


			# s.send(pickle.dumps(message))

			data = pickle.loads(s.recv(1024))
			print('Received from server: ', data)
		
	s.close()

if __name__ == '__main__':
	client()