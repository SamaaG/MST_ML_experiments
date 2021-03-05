import socket
import pickle
import numpy
from MST import *
import numpy as np
import time
import sys
import json

def cloud(yolo):
    times = list()
    host = '172.31.76.231' # cloud private ipv4
    port = 8085

    s = socket.socket()
    s.bind((host, port))

    print(f'Listening on port {port}..')
    s.listen(1)
    print('Waiting..')

    edge_socket, adress = s.accept()
    print("Connection from: " + str(adress))

    c = 0
    frameisnotdone = True
    frame = bytearray()

    while True:
        time_before_frame_recv = time.time()
        while frameisnotdone:
            data = edge_socket.recv(1024)
            frame.extend(data)

            if len(frame) >= 1229888:
                frameisnotdone = False
            elif len(frame) == 0:
                edge_socket.close()
        try:
            f = pickle.loads(frame)
            time_after_frame_recv = time.time()
        except:
            frame = bytearray()
            frameisnotdone = True
            d = pickle.dumps('error')
            edge_socket.send(d)
            continue
        print('from edge:', len(f))

        frameisnotdone = True
        frame = bytearray()

        time_before_detect = time.time()
        result = detect(f, yolo, .9, 0)
        print(result)
        time_after_detect = time.time()

        # print(len(result))

        # d = pickle.dumps(result)
        # print(sys.getsizeof(d))
        # print(pickle.loads(d))
        # time.sleep(5)

        d = json.dumps(result)
        print(d, type(d))
        edge_socket.send(d.encode('utf-8'))
        print("done")

        times.append([time_after_frame_recv - time_before_frame_recv , time_after_detect - time_before_detect])
        np.save('times', times)


    edge_socket.close()

if __name__ == '__main__':
    yolo = load_model('yolov3')
    cloud(yolo)