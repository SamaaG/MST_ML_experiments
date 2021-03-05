import os
import socket
import pickle
import time
import cv2
from sys import getsizeof
import numpy as np
def client():
        times = list()
        cwd = os.getcwd()
        host = '13.56.59.242'  # edge public ipv4 address
        port =  8082

        #host = socket.gethostname()  # get local machine name
        # port = 8081
        print('Connecting to '+ host)

        s = socket.socket()
        s.connect((host, port))

        c = 0
        cap = cv2.VideoCapture('1.mp4')
        frames = getFrames(cap)
        print(f'there are {len(frames)} frames')
        for f in frames:
                c +=1
                print(c)
                if c < 40:
                        pass #continue
                size = getsizeof(f)
                time_before_frame_is_sent = time.time()
                # print(getsizeof(f)) this size is used in the condition len(frame) >= ... in the server
                if getsizeof(f) != size:
                        print('size', getsizeof(f), size)
                        s.close()
                        break

                else:
                        # print(f'the size is {size}')
                        # s.send(pickle.dumps(size))
                        s.send(pickle.dumps(f))
                time_after_frame_is_sent = time.time()
                data = pickle.loads(s.recv(1024))
                time_after_result_is_recieved = time.time() # print('Received from server:', data)

                # print("it took {:.4f}sec to send and {:.4f}sec to process and receive a response".format(time_after_frame_is_sent - time_before_frame_is_sent, time_after_result_is_recieved - time_after_frame_is_sent))

                times.append([time_after_frame_is_sent - time_before_frame_is_sent, time_after_result_is_recieved - time_after_frame_is_sent])
                np.save('times', times)

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