# Information about supplementary material

In this repository, we include the data, code, and models that we used in our evaluations and experiments. Specifically, they are divided into the following:

## Preprocessing code to generate thresholds
This part is what we use to generate the space of f-1 and bandwidth utilization numbers for different configurations of lower and upper thresholds. These results are used to generate the heatmaps in Figure 6. This code is placed in the files Preprocessing.py and MST.py in this repository. 

## optimization functions
This part is what we use to run the optimization functions that we describe in Section 3.4. This code is used to choose the optimal pair of thresholds denoted by stars in Figure 6. This code is placed in the file optimal_theta.py in this repository.

## Croesus edge-cloud implementation
This part is the implementation of our Croesus prototype. This includes an implementation of a client, edge, and cloud nodes. The client generates requests and sends frames to be processed, the edge processes requests, transactions, and coordinate with the cloud for cloud labels, and the cloud node runs the cloud CNN model. This part is used for experiments shown in Figures 4 and 5. The files for these implementations are in Croesus\MST_Client_ML.py, Croesus\MST_Edge_ML.py and Croesus\MST_Cloud_ML.py this repository.

## CNN Model processing and detection functions
This part handles the functions that related to processing CNN models as well as other image processing functions such computing overlapping bounding boxes. This part is used in the experiments shown in Figures 4 and 5. The files for these implementations are overlapping.py and MST.py in this repository.

## Models
The cofiguration and weights of the CNN models used in this project can be accessed here: https://pjreddie.com/darknet/yolo/

## Video repo
The videos used in the experiments can be accessed here: https://github.com/SamaaG/Croesus-videos


