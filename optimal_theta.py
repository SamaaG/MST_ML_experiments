from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import random

import sys
from random import randint

def get_abs_min_delay_cell(t, A, D):
    min_delay = 1
    min_r = None
    min_c = None
    for row in range(len(A)):
        for column in range(0, len(A) - row):

            if A[row][column] >= t and  D[row][column] < min_delay:
                min_delay = D[row][column]
                min_r, min_c  = row, column
    print('Finished brute force at ({},{}): A={}, D={}'.format(min_r, min_c, A[min_r][min_c], D[min_r][min_c]))
    return min_r, min_c

def get_neighbors(r, c, width, height):
    nighbors = []
    locations = ((r, c-1), (r, c+1),
                 (r-1, c-1), (r-1, c), (r-1, c+1),
                 (r+1, c-1), (r+1, c), (r+1, c+1))
    for row, col in locations:
        if ((row >= 0 and row < width)
                 and (col >= 0 and col < height)):
            nighbors.append((row, col))
    return nighbors

def get_local_min_delay_cell(r, c, t, A, D):
    locations = get_neighbors(r, c, len(A), len(A[0]))
    min_dely = 100
    min_row = r
    min_col = c
    for row, col in locations:
        if A[row][col] == None:
            continue
        elif A[row][col] >= t:
            if D[row][col] < min_dely:
               min_dely = D[row][col]
               min_row = row
               min_col = col

    # is the current cell better than best neighbor
    if A[r][c] != None and A[r][c] >= t:
        if D[r][c] <= min_dely:
            return r, c
    return min_row, min_col

def get_min_delay_cell(t, A, D):
    # pick a random cell in the upper right triangle
    row_prev = randint(0, len(A) - 1)
    col_prev = randint(0, len(A) - row_prev)


    print('Starting at ({},{}): A={}, D={}'.format(row_prev, col_prev, A[row_prev][col_prev], D[row_prev][col_prev]))
    exhausted = False
    while not exhausted:
        row, col = get_local_min_delay_cell(row_prev, col_prev, t, A, D)
        if row == row_prev and col == col_prev:
            exhausted = True
        row_prev = row
        col_prev = col

    print('Finished gradient step at ({},{}): A={}, D={}'.format(row_prev, col_prev, A[row_prev][col_prev], D[row_prev][col_prev]))
    return row_prev, col_prev




fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = np.arange(0, 1, 0.1)
print(X)
Y = np.arange(0, 1, 0.1)
X, Y = np.meshgrid(X, Y)

performance = np.load('BU.npy')
fscore = np.load('Acc.npy')


import time
first = time.time()
myDict = {}
for i in range(1000):
    try:
        row, col = get_min_delay_cell(0.95, fscore, performance)
        if myDict.get(str(row)+','+str(col))!=None:
            myDict[str(row)+','+str(col)] += 1
        else:
            myDict[str(row)+','+str(col)] = 1
    except:
        pass
second = time.time()

print(myDict)

get_abs_min_delay_cell(0.95, fscore, performance)
third = time.time()

print((second - first )/(third - second))


# performance = np.array(performance)
# # Plot the surface of performance.
# surf_p = ax.plot_surface(X, Y, performance, cmap=cm.prism,
#                        linewidth=0, antialiased=False)
# fscore = np.array(fscore)
# # Plot the surface of
# surf_f = ax.plot_surface(X, Y, fscore, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)

# # cbar_f = fig.colorbar(surf_f, shrink=0.5, aspect=5)
# # cbar_f.ax.set_title('fscore')

# # Customize the z axis.
# ax.set_zlim(0, 1.01)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))


# # replace unwanted threshold performances with a None
# perfromance_adjusted = np.where(fscore < .9, np.inf, performance)

# # get the index of the min value
# result = np.where(perfromance_adjusted == np.amin(perfromance_adjusted))

# print('List of coordinates of minimum value:')
# # zip the 2 arrays to get the exact coordinates
# listOfCordinates = list(zip(result[0], result[1]))
# # travese over the list of cordinates
# for cord in listOfCordinates:
#     print(cord)

# # plt.show()