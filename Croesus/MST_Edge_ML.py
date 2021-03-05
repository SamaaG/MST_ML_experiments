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
import numpy as np
import time
import sys
import json

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


def txn(txn_num, op_num, allUIDs):
    txn_processing_time = 0
    for i in range(int(txn_num)):
        for j in range(int(op_num)):
            c = choice(['read', 'write'])
            if c == 'read':
                idn = str(choice(allUIDs))
                t1 = time.time()
                process(idn, db)
                t2 = time.time()
                txn_processing_time += (t2 - t1)

            elif c == 'write':
                idn = str(uuid.uuid4())
                data = {idn:{'name': get_random_string(), 'age': get_age()}}

                allUIDs = np.append(allUIDs, [idn])
                np.save('allUIDs', allUIDs)
                t1 = time.time()
                process(data, db)
                t2 = time.time()
                txn_processing_time += (t2 - t1)
    return txn_processing_time

# def final_txn():

def go2Cloud(result, lookfor, upper_theta):
    rang = [i for i, e in enumerate(result['classIDs']) if e == lookfor]
    return any(result['confidences'][i] < upper_theta for i in rang)

def edge(db, yolo, lower_theta, upper_theta, lookfor):
    # SEND A FIRST PACKET WITH LT, UT, SIZE, LOOKFOR
    times = list()
    allCorners = list()
    cwd = os.getcwd()
    allUIDs = np.load(os.path.join(cwd,'allUIDs.npy'))

    host_edge =  '172.31.21.233' # edge private ipv4
    port_edge = 8082
    s_edge = socket.socket()
    s_edge.bind((host_edge, port_edge))

    #####################################
    host_cloud =  '3.236.113.252'  # cloud public ipv4 address
    port_cloud = 8085

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

    went_to_cloud = 0
    total_frames_count = 0
    while True:
        time_before_frame_recv = time.time()
        while frameisnotdone:
            data = client_socket.recv(1024)
            frame.extend(data)
            if len(frame) >= 1229888:
                try:
                    f = pickle.loads(frame)
                    time_after_frame_recv = time.time()
                    frameisnotdone = False
                except:
                    frameisnotdone = True
                    continue
            elif len(frame) == 0:
                client_socket.close()
#        try:
#            f = pickle.loads(frame)
#            time_after_frame_recv = time.time()
#        except:
#            frameisnotdone = True
#            continue
        total_frames_count += 1
        frameisnotdone = True
        frame = bytearray()

        time_before_detect = time.time()
        result = detect(f, yolo, lower_theta, lookfor)

        time_after_detect = time.time()

        #  INITIAL TRANSACTION
        txn_time_i = txn(1,1, allUIDs)

        time_after_txn = time.time()
        N = 180
        edge = 0 # edge = zeros, N-edge aka clouds =  ones
        cloud_choice = np.array([0] * edge + [1] * (N-edge))
        np.random.shuffle(cloud_choice)
        print(cloud_choice[total_frames_count - 1])
        if cloud_choice[total_frames_count - 1]: # go2Cloud(result, lookfor, upper_theta):
            time_before_going2cloud = time.time()
            went_to_cloud += 1
            s_cloud.send(pickle.dumps(f))
            d = s_cloud.recv(2048)
            print(sys.getsizeof(d))
            # result = pickle.loads(d)
            result = json.loads(d)
            print('Received from cloud:', result)
            time_after_cloud = time.time()

        time_after_backfrom_cloud = time.time()
        # FINAL TRANSACTION
        txn_time_j = txn(1,1, allUIDs)

        time_after_txn2 = time.time()
        print('total frames so far', total_frames_count)

        corners = getCornersList(result)
        allCorners.extend([corners])
        np.save('allCorners-croesus', allCorners)

        d = pickle.dumps(result)
        client_socket.send(d)
        print("done")
        if cloud_choice[total_frames_count - 1]: # go2Cloud(result, lookfor, upper_theta):
            times.append([time_after_frame_recv - time_before_frame_recv, time_after_detect -  time_before_detect, txn_time_i,time_after_cloud - time_before_going2cloud , txn_time_j ])
        else:
            times.append([time_after_frame_recv - time_before_frame_recv, time_after_detect -  time_before_detect, txn_time_i ,0, txn_time_j])

        np.save('times', times)
        print('the percentage is', (went_to_cloud/total_frames_count)*100)
    client_socket.close()

if __name__ == '__main__':
    db = pickledb.load('MyDB.db', True)
    initializeDB(db)
    lower_theta = 0.5 # don't trust predictions with less confidence
    upper_theta = 0.6 # validate predictions under this confidence

    lookfor = 0 #car
    yolo = load_model('yolov3-tiny')
    edge(db, yolo, lower_theta, upper_theta, lookfor)