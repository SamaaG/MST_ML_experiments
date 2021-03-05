import socket
import pickle
import numpy
from MST import *

def cloud():

    host = socket.gethostname()  # cloud ipv4
    port = 8082

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
        while frameisnotdone:
            data = edge_socket.recv(1024)
            frame.extend(data)

            if len(frame) >= 1229888:
                frameisnotdone = False
            elif len(frame) == 0:
                edge_socket.close()

        f = pickle.loads(frame)
        print('from edge:', len(f))
        frameisnotdone = True
        frame = bytearray()

        yolo = load_model('yolov3')
        result = detect(f, yolo, .8, 0)

        
        print(len(result))

        d = pickle.dumps(result)
        edge_socket.send(d)
        print("done")

    edge_socket.close()

if __name__ == '__main__':
    cloud()