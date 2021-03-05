import socket
import pickle
import numpy
from MST import *
import uuid
import string
from random import choice
from random import randint
import pickledb
import traceback
import os

def process(op, db):
    if type(op) == type(dict()):
        return write(op, db)
    elif type(op) == type(str()):
        return read(op, db)

def read(op, db):
    return db[op]

def write(op, db):
    for k in op:
        db.set(k, op[k])
        return 'done writing'

def get_age():
    return randint(1, 99)

def get_random_string():
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(6))

def initializeDB(db):
    print("initialize a database...")
    id1 = str(uuid.uuid4())
    id2 = str(uuid.uuid4())

    data = {id1:{'name':get_random_string(), 'age': get_age()}, 
            id2:{'name':get_random_string(), 'age':get_age()}}

    np.save('allUIDs', [id1, id2])
    process(data, db)


def txn(txn_num, op_num):
    cwd = os.getcwd()
    allUIDs = np.load(os.path.join(cwd,'allUIDs.npy'))

    for i in range(int(txn_num)):
        for j in range(int(op_num)):
            c = choice(['read', 'write'])
            print(f'the choice is {c}')
            if c == 'read':
                allUIDs = np.load(os.path.join(cwd,'allUIDs.npy'))
                idn = str(choice(allUIDs))
                process(idn, db)

            elif c == 'write':
                idn = str(uuid.uuid4())
                data = {idn:{'name': get_random_string(), 'age': get_age()}}

                allUIDs = np.append(allUIDs, [idn])
                np.save('allUIDs', allUIDs)
                process(data, db)

# def final_txn():

def go2Cloud(result, lookfor, upper_theta):
    rang = [i for i, e in enumerate(result['classIDs']) if e == lookfor]
    return any(result['confidences'][i] < upper_theta for i in rang)
         
def edge(db, lower_theta, upper_theta, lookfor):
    # SEND A FIRST PACKET WITH LT, UT, SIZE, LOOKFOR

    host_edge = socket.gethostname()  # edge ipv4
    port_edge = 8081

    s_edge = socket.socket()
    s_edge.bind((host_edge, port_edge))

    #####################################
    host_cloud = socket.gethostname()  # cloud public ipv4 address
    port_cloud = 8082

    s_cloud = socket.socket()
    s_cloud.connect((host_cloud, port_cloud))
    #####################################

    print(f'Listening on port {port_edge}..')
    s_edge.listen(1)
    print('Waiting..')

    client_socket, adress = s_edge.accept()
    print("Connection from: " + str(adress))

    c = 0
    frameisnotdone = True
    frame = bytearray()

    while True:
        # size = client_socket.recv(40)
        # s = pickle.loads(size)
        # print(s)
        while frameisnotdone:
            data = client_socket.recv(1024)
            frame.extend(data)
            if len(frame) >= 1229888:
                frameisnotdone = False
            elif len(frame) == 0:
                client_socket.close()

        f = pickle.loads(frame)

        frameisnotdone = True
        frame = bytearray()

        yolo = load_model('yolov3-tiny')
        result = detect(f, yolo, lower_theta, lookfor)
        

        #  INITIAL TRANSACTION 
        txn(2,3)

        if go2Cloud(result, lookfor, upper_theta):
            s_cloud.send(pickle.dumps(f))
            data = pickle.loads(s_cloud.recv(1024))
            print('Received from cloud:', len(data))

        # FINAL TRANSACTION
        txn(2,3)

        d = pickle.dumps(result)
        client_socket.send(d)
        print("done")

    client_socket.close()

if __name__ == '__main__':
    db = pickledb.load('MyDB.db', True)
    initializeDB(db)
    lower_theta = 0.1 # don't trust predictions with less confidence
    upper_theta = 0.4 # validate predictions under this confidence

    lookfor = 0 #car

    edge(db, lower_theta, upper_theta, lookfor)