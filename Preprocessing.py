import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd


cloud_percnt =  [[np.nan for _ in range(10)] for _ in range(10)]
xticklabels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 ,0.7, 0.8, 0.9]
yticklabels = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]

with open('frame_stats.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')

	for row in csv_reader:		
		r = int(float(row[1]) * 10)
		c = int(float(row[0]) * 10)
		
		cloud_percnt[r][c] = float(row[2])/float(row[3])

cloud_percnt = pd.DataFrame(np.array(cloud_percnt[::-1]))
mask = cloud_percnt.isnull()


heat_map = sb.heatmap(cloud_percnt, annot=True, cmap="YlGnBu", yticklabels = yticklabels, xticklabels = xticklabels, cbar_kws = {'label': 'Percentage of frames going to cloud', 'orientation': 'horizontal'})
plt.ylabel('Upper Threshold')
plt.xlabel('Lower Threshold')
plt.show()

print(cloud_percnt)
np.save('BU', cloud_percnt)
# ============================================
f_scores =  [[np.nan for _ in range(10)] for _ in range(10)]

with open('fscores_raw.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')

	for row in csv_reader:		
		r = int(float(row[1]) * 10)
		c = int(float(row[0]) * 10)
		
		f_scores[r][c] = float(row[2])

f_scores = pd.DataFrame(np.array(f_scores[::-1]))
mask = f_scores.isnull()


heat_map = sb.heatmap(f_scores, mask = mask, annot = True, cmap = "YlGnBu", yticklabels = yticklabels, xticklabels = xticklabels, cbar_kws={'label': 'F1-Score', 'orientation': 'horizontal'})
plt.ylabel('Upper Threshold')
plt.xlabel('Lower Threshold')
plt.show()
print(f_scores)
np.save('Acc', f_scores)