from overlapping import compare_frame
import numpy as np
import time
import cv2
import os
import csv


# 'detections' is a list of detected objects locations, confidence, where all are the same object, and no overlap between them and all with confidence over the theta that was sent to detect with


def getCornersList(detections):
    boxes = detections['boxes']
    buffer_list = list()

    for i in range(len(boxes)):
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        buffer_list.append([[x, y],[x + w, y + h]])
    return buffer_list


def getTheTruth(cap, lookfor, UpperTheta):

    # load the YOLO model 
    yolo = load_model('yolov3')
    # load labels

    allCorners = list()
    i = 0
    # iterate over all frames of the video
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        detections = detect(frame, yolo, UpperTheta, lookfor)

        i += 1


        # here I should save the numpy of corners
        corners = getCornersList(detections)
        allCorners.extend([corners])
 
    cap.release()

    cv2.destroyAllWindows()
    return allCorners


def twoStageTxn(cap, lookfor, lowerTheta, UpperTheta):
    # load the tiny-YOLO model
    tiny_yolo = load_model('yolov3-tiny')
    # load the YOLO model 
    yolo = load_model('yolov3')
    # load labels

    allCorners = list()

    i = 0
    CloudCount = 0
    # iterate over all frames of the video
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        # here send the frame to predict with the lower theta and the tiny yolo moedel
        detections = detect(frame, tiny_yolo, lowerTheta, lookfor)


        rang = [i for i, e in enumerate(detections['classIDs']) if e == lookfor]

        if (any(detections['confidences'][i] < UpperTheta for i in rang)):
                detections = detect(frame, yolo, 0.9, lookfor)
                CloudCount += 1

        i += 1

        # here I should save the numpy of corners
        corners = getCornersList(detections)
        allCorners.extend([corners])



    cap.release()

    cv2.destroyAllWindows()

    print("the percent going to cloud is ", CloudCount/i)

    with open('frame_stats.csv','a', newline='') as exp_file:
        wr = csv.writer(exp_file)
        wr.writerow([lowerTheta, UpperTheta, CloudCount, i])

    return allCorners



def load_model(scen):
    CWD_PATH = os.getcwd() 
    # load the COCO class labels our YOLO model was trained on
    modeldir=os.path.join(CWD_PATH, 'models')
    labelsPath = os.path.sep.join([modeldir, "coco.names"])
    labels = open(labelsPath).read().strip().split("\n")

    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([modeldir, scen + ".weights"])
    configPath = os.path.sep.join([modeldir, scen + ".cfg"])

    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

    return net

def detect(frame, model, theta, lookfor):

    NMS_theta = 0.3
    (H, W) = frame.shape[:2]

    ln = model.getLayerNames()
    ln = [ln[i[0] - 1] for i in model.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    model.setInput(blob)

    layerOutputs = model.forward(ln)

    boxes = []
    confidences = []
    classIDs = []
    results = dict()

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            
            if confidence > theta:

                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                if classID == lookfor:
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

    results['boxes'] = boxes
    results['confidences'] = confidences
    results['classIDs'] = classIDs

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, theta, NMS_theta)

    newResults = dict()
    newResults['boxes'] = list()
    newResults['confidences'] = list()
    newResults['classIDs'] = list()

    if len(idxs) > 0:
        for i in idxs.flatten():
            newResults['boxes'].append(results['boxes'][i])
            newResults['confidences'].append(results['confidences'][i])
            newResults['classIDs'].append(results['classIDs'][i])

    return newResults


def analyzeVid_GetFscore(truth, pred, lt, ut):
    TR_PR_overlap = 0
    total_truth = 0
    total_pred = 0


    for i in range(len(truth)):
        with open('Truth_data.csv','a', newline='') as exp_file1:
            wr = csv.writer(exp_file1)
            wr.writerow(truth[i])

        with open('Pred_data.csv','a', newline='') as exp_file2:
            wr = csv.writer(exp_file2)
            wr.writerow(pred[i])

        number_of_matches = 0   
        total_truth += len(truth[i])
        total_pred += len(pred[i])

        TR_PR_overlap += compare_frame(truth[i], pred[i])


    if total_pred == 0:
        F1 = 0

    # print('the total overlapp so far', TR_PR_overlap)
    # print('the total truuth', total_truth, 'and the total pred', total_pred)
    else: 
        precision = TR_PR_overlap/float(total_pred)
        recall = TR_PR_overlap/float(total_truth)
        print("for lower_theta", lt, "and higher_theta", ut)
        print("precision is ", precision, " and recall is ", recall)
        if precision > 0 or recall > 0:
            F1 = (2 * precision * recall)/(precision + recall)
        else:
            F1 = 0
    
        print('the f score is', F1)
    with open('fscores_raw.csv','a', newline='') as exp_file:
        wr = csv.writer(exp_file)
        wr.writerow([lt, ut, F1])

    return F1



# # define the thetas
# lt = 0.1
# ut = 0.4

# # Opens the Video file
# cap = cv2.VideoCapture('1.mp4')
# truth = getTheTruth(cap, 0, 0.9)

# cap = cv2.VideoCapture('1.mp4')
# pred = twoStageTxn(cap, 0, lt, ut)

# f1 = analyzeVid_GetFscore(truth, pred, lt, ut)
# print('f1 is', f1)


# ====================================================================================

# vids = ['1.mp4', '2_trim.mp4', '4_trim.mp4', '6.mp4']
# lookfor = [5, 0, 14, 0]

# print('now working on the truth')
# # Opens the Video file
# cap = cv2.VideoCapture(vids[0])
# truth = getTheTruth(cap, lookfor[0], 0.9)

# # this code to run the whole experiment through all the thresholds
# F1_scores = [[0] * 11] * 11

# for i in range(0, 10):
#     lower_theta = i / 10

#     for j in range(i, 10):
#         upper_theta = j / 10

#         print('now working on lt', lower_theta, 'AND UT:', upper_theta)

#         cap = cv2.VideoCapture(vids[0])
#         pred = twoStageTxn(cap, lookfor[0], lower_theta, upper_theta)

#         f1 = analyzeVid_GetFscore(truth, pred, lower_theta, upper_theta)
#         print('f1 is ', f1)