import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy as np
import pickle
import pandas as pd
from math import sqrt
import matplotlib
import os
from math import log
  ######################################## Latexify Start#############################################
SPINE_COLOR = 'gray'

def latexify(fig_width=None, fig_height=None, columns=1):
    assert(columns in [1,2])

    if fig_width is None:
        fig_width =  3.39 if columns==1 else 6.9 # width in inches

    if fig_height is None:
        golden_mean = (sqrt(5)-1.0)/2.0    # Aesthetic ratio
        fig_height = fig_width*golden_mean # height in inches

    
    MAX_HEIGHT_INCHES = 8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large:" + fig_height + 
              "so will reduce to" + MAX_HEIGHT_INCHES + "inches.")
        fig_height = MAX_HEIGHT_INCHES
   
    params = {'backend': 'ps',
              'text.latex.preamble': ['\usepackage{gensymb}'],
              'axes.labelsize': 25, # fontsize for x and y labels (was 10)
              'axes.titlesize': 15,
              'font.size': 25, # was 10
              'legend.fontsize': 12, # was 10
              'xtick.labelsize': 25,
              'ytick.labelsize': 25,
              'text.usetex': True,
              'figure.figsize': [fig_width,fig_height],
              'font.family': 'serif'
    }

    matplotlib.rcParams.update(params)


def format_axes(ax):

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(SPINE_COLOR)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=SPINE_COLOR)

    return ax

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)    

######################################## Latexify #############################################

latexify()
size = 5
fig, ax = plt.subplots()


year = [0]*6



######################### TOP PAPER WISE EXPERIMENT 1 #######################################

# fname = "paperWise1SC" 
# with open(fname, "w") as citation_file:
#     pickle.dump(SC, citation_file)

# fname = "paperWise1CC" 
# with open(fname, "w") as citation_file:
#     pickle.dump(CC, citation_file)

# fname = "paperWise1CN" 
# with open(fname, "w") as citation_file:
#     pickle.dump(CN, citation_file)

SC = pickle.load(open("./paperWise1SC", "r"))
CC = pickle.load(open("./paperWise1CC", "r"))
CN = pickle.load(open("./paperWise1CN", "r"))

numberOfGroupsYears = 5
fig, ax = plt.subplots(figsize=(20,10))
index = np.arange(numberOfGroupsYears)
barWidth = .20
opacity = 1.0

rects1 = plt.bar(index, SC, barWidth, alpha=opacity, color='b', label='Self Copied')
rects2 = plt.bar(index + barWidth, CC, barWidth, alpha=opacity, color='r', label='Copied and Cited')
rects3 = plt.bar(index + 2*barWidth, CN, barWidth, alpha=opacity, color='g', label='Copied and Not Cited')

plt.xlabel('Years from Publication of Cited Paper')
plt.ylabel('Numbers of Citations')
# plt.title('Experiment 7')
plt.xticks(index + barWidth, ('Year-1', 'Year-2', 'Year-3', 'Year-4', 'Year-5'))
plt.legend()

plt.tight_layout()
# plt.show()
print "Process Completed"
fig.savefig("Figure2(b).pdf")
plt.close(fig)


##################################### TOP PAPER WISE EXPERIMENT 2 ##############################



CC = pickle.load(open("./paperWise2CC", "r"))
CN = pickle.load(open("./paperWise2CN", "r"))
# fname = "paperWise2CC" 
# with open(fname, "w") as citation_file:
#     pickle.dump(CC, citation_file)

# fname = "paperWise2CN" 
# with open(fname, "w") as citation_file:
#     pickle.dump(CN, citation_file)

numberOfGroupsYears = 5
fig, ax = plt.subplots(figsize=(20,10))
index = np.arange(numberOfGroupsYears)
barWidth = .20
opacity = 1.0

rects2 = plt.bar(index, CC, barWidth, alpha=opacity, color='r', label='Copied and Cited')
rects3 = plt.bar(index + barWidth, CN, barWidth, alpha=opacity, color='g', label='Copied and Not Cited')

plt.xlabel('Years from Publication of Cited Paper')
plt.ylabel('Numbers of Citations')
# plt.title('Experiment 9')
plt.xticks(index + barWidth, ('Year-1', 'Year-2', 'Year-3', 'Year-4', 'Year-5'))
plt.legend()

plt.tight_layout()
# plt.show()
fig.savefig("Figure2(a).pdf")
plt.close(fig)