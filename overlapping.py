#  3(x, y + h)-----------4(x + w, y + h)
#		|						|
#		|						|
#		|						|	
#		|						|	
#   1(x, y)----------------2(x + w, y)
#
import matplotlib.pyplot as plt
import numpy as np
def get_corners(x, y, w, h):
	(x1, y1) = (x, y)
	(x2, y2) = (x + w, y)
	(x3, y3) = (x, y + h)
	(x4, y4) = (x + w, y + h)

	return [x1, x2, x3 ,x4], [y1, y2, y3, y4]

def plot_rect(first_x, second_x, first_y, second_y):
	plt.plot(first_x, first_y, 'ro')
	plt.plot(second_x, second_y, 'bo')
	plt.ylabel('some numbers')
	plt.show()

def get_cornerPts(x, y, w, h):
	return [x, y], [x + w, y + h]

def doOverlap(l_truth, r_truth, l_pred, r_pred):
	if (l_truth[0] >= r_pred[0]) or (l_pred[0] >= r_truth[0]):
		return False
	if (r_truth[1] <= l_pred[1]) or (r_pred[1] <= l_truth[1]):
		return False
	return True



def overlappingArea(l_truth, r_truth, l_pred, r_pred): 
    area_truth = abs(l_truth[0] - r_truth[0]) * abs(l_truth[1] - r_truth[1]) 
    area_pred = abs(l_pred[0] - r_pred[0]) * abs(l_pred[1] - r_pred[1])

    areaI = (min(r_truth[0], r_pred[0]) - max(l_truth[0], l_pred[0])) * (min(r_truth[1], r_pred[1]) - max(l_truth[1], l_pred[1]))
    areaU = (area_truth + area_pred - areaI) 

    overlap_percentage = float(areaI) / float(areaU)

    return overlap_percentage

def get_numpy(thing):
	# x = np.arange(10000)
	# np.save('outfile', x)
	x =  np.load('out_'+str(thing)+'_truth.npy')
	# print("truth length is", len(x))
	y =  np.load('out_'+str(thing)+'_pred.npy')
	# print("prediction length is", len(y))

	return x, y
	
def compare_frame(tr, pr):
	number_of_matches = 0
	# if a prediction is matched to a truth, it cannot be matched to any other thruth
	set_of_pred_matched = set()

	for j in range(len(tr)):
		# in 'match_is', the first position is the percentage of match. the second position is detection that matched
		match_is = [0, 0]
		for i in range(len(pr)):
			if doOverlap(tr[j][0], tr[j][1], pr[i][0], pr[i][1]):
				percentage = overlappingArea(tr[j][0], tr[j][1], pr[i][0], pr[i][1])
			else:
				percentage = 0

			if percentage > match_is[0]:
				match_is = [percentage, j]

		if match_is[0] > .10 and not (match_is[1] in set_of_pred_matched):
			set_of_pred_matched.add(match_is[1])
			number_of_matches += 1

	
	return number_of_matches




# first_x, first_y = get_corners(1, 2, 3, 5)
# second_x, second_y = get_corners(1, 4, 3, 3)
# plot_rect(first_x, second_x, first_y, second_y)



# x, y = get_numpy(0)
# n = 0
# for i in x:
# 	print(n)
# 	for j in i:
# 		print(j)
# 	n += 1

# for thing in lookfor:
# 	write_numpy(thing)


##############################################################

# lookfor = [5, 0, 14]
# truth, pred = get_numpy(lookfor[0])

# for i in range(len(truth)):
# 	TR_PR_overlap, total_truth, total_pred= compare_frame(truth[i], pred[i])
# print(TR_PR_overlap, total_truth, total_pred)
# precision = TR_PR_overlap/total_pred
# recall = TR_PR_overlap/total_truth
# print("precision is ", precision, " and recall is ", recall)
# F1 = (2 * precision * recall)/(precision + recall)
# print("F1 score is ", F1)

##################################################################


# box_1 = get_box(1, 2, 3, 5)
# box_2 = get_box(2, 5, 3, 3)
# print(calculate_iou(box_1, box_2))

