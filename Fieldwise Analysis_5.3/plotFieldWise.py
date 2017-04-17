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
from matplotlib import rcParams



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
              'axes.labelsize': 10, # fontsize for x and y labels (was 10)
              'axes.titlesize': 10,
              'font.size': 10, # was 10
              'legend.fontsize': 10, # was 10
              'xtick.labelsize': 10,
              'ytick.labelsize': 10,
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


###################################################################################################


cosine_values = pickle.load( open( "fields[%d]", "rb" ) )



#################################################################################################

bin_counts = {} 

fields = [0]*24
fieldDataframe = [0]*24

alg = pd.DataFrame(cosine_values['algorithms_and_theory'], columns = ['cosine','cat1','cat2'])
inf = pd.DataFrame(cosine_values['information_retrieval'], columns = ['cosine','cat1','cat2'])
dat = pd.DataFrame(cosine_values['data_mining'], columns = ['cosine','cat1','cat2'])
gra = pd.DataFrame(cosine_values['graphics'], columns = ['cosine','cat1','cat2'])

prg = pd.DataFrame(cosine_values['programming_languages'], columns = ['cosine','cat1','cat2']) 
net = pd.DataFrame(cosine_values['networks_and_communications'], columns = ['cosine','cat1','cat2'])
dbms = pd.DataFrame(cosine_values['databases_'], columns = ['cosine','cat1','cat2']) 


bin_counts['algorithms_and_theory'], edges1 = np.histogram(a=alg['cosine'], bins=500, density=True)
at = bin_counts['algorithms_and_theory']

fname = 'at'
with open(fname,'w') as atfile:
    pickle.dump(at,atfile)
fname = 'atedges'
with open(fname,'w') as atfile:
    pickle.dump(edges1,atfile)

bin_counts['information_retrieval'], edges2 = np.histogram(a=inf['cosine'], bins=500, density=True)

fname = 'ir'
with open(fname,'w') as irfile:
    pickle.dump(ir,irfile)
fname = 'iredges'
with open(fname,'w') as irfile:
    pickle.dump(edges2,irfile)

bin_counts['data_mining'], edges3 = np.histogram(a=dat['cosine'], bins=500, density=True)
dm = bin_counts['data_mining']

fname = 'dm'
with open(fname,'w') as dmfile:
    pickle.dump(dm,dmfile)
fname = 'dmedges'
with open(fname,'w') as dmfile:
    pickle.dump(edges3,dmfile)

bin_counts['graphics'], edges4 = np.histogram(a=gra['cosine'], bins=500, density=True)
g = bin_counts['graphics']

fname = 'g'
with open(fname,'w') as gfile:
    pickle.dump(g,gfile)
fname = 'gedges'
with open(fname,'w') as gfile:
    pickle.dump(edges2,gfile)

bin_counts['programming_languages'], edges5 = np.histogram(a=prg['cosine'], bins=500, density=True)
pl = bin_counts['programming_languages']

fname = 'pl'
with open(fname,'w') as plfile:
    pickle.dump(pl,plfile)
fname = 'pledges'
with open(fname,'w') as plfile:
    pickle.dump(edges5,plfile)

bin_counts['networks_and_communications'], edges6 = np.histogram(a=net['cosine'], bins=500, density=True)
nc = bin_counts['networks_and_communications']

fname = 'nc'
with open(fname,'w') as ncfile:
    pickle.dump(nc,ncfile)
fname = 'ncedges'
with open(fname,'w') as ncfile:
    pickle.dump(edges6,ncfile)

bin_counts['databases_'], edges7 = np.histogram(a=dbms['cosine'], bins=500, density=True)
d = bin_counts['databases_']

fname = 'd'
with open(fname,'w') as dfile:
    pickle.dump(d,dfile)
fname = 'dedges'
with open(fname,'w') as dfile:
    pickle.dump(edges7,dfile)




##################################### FIELD WISE HISTOGRAM ###########################################################


at = pickle.load(open('at','r'))
pl = pickle.load(open('pl','r'))
nc = pickle.load(open('nc','r'))
d = pickle.load(open('d','r'))
edges1 = pickle.load(open('atedges','r'))
edges5 = pickle.load(open('pledges','r'))
edges6 = pickle.load(open('ncedges','r'))
edges7 = pickle.load(open('dedges','r'))


plt.figure()

plt.plot(edges1[:-1] + np.diff(edges1) / 2 , at)   
plt.plot(edges5[:-1] + np.diff(edges5) / 2 , pl)   
plt.xlabel("Cosine Similarity")
plt.xlim(xmin=0.0, xmax=1.0)
plt.yscale("log")
plt.ylabel("Frequency (Normalized Log scale)")
plt.savefig('Mixture1' + "_lognorm.pdf", bbox_inches='tight')
plt.close(fig)


plt.figure()
plt.plot(edges6[:-1] + np.diff(edges6) / 2 , nc)   
plt.plot(edges7[:-1] + np.diff(edges7) / 2 , d)   
plt.xlabel("Cosine Similarity")
plt.xlim(xmin=0.0, xmax=1.0)
plt.yscale("log")
plt.ylabel("Frequency (Normalized Log scale)")
plt.savefig('Mixture2' + "_lognorm.pdf", bbox_inches='tight')
plt.close(fig)


###########################################################################################




####################################### FIELD WISE SC, CC, CN #############################################################

dic = cosine_values

fields = [0]*24
pairNumber=[0]*24
copiedPairNumber = [0]*24
fieldDataframe = [0]*24
SC = [0]*24
CC = [0]*24
CN = [0]*24

inputData = list(zip(fields, pairNumber, copiedPairNumber))
inputDataFrame = pd.DataFrame(inputData, columns=['Field', 'Total Pairs', 'Copied Pairs'])

for i, key in enumerate(dic.keys()):
    fields[i] = key
    fieldDataframe[i] = pd.DataFrame(dic[key])
    pairNumber[i] = fieldDataframe[i].shape[0]
    fieldDataframe[i] = fieldDataframe[i].loc[fieldDataframe[i][0] >= 0.8]
    copiedPairNumber[i] = fieldDataframe[i].shape[0]
    groupedCategories = fieldDataframe[i].groupby(1).size().to_frame(name='Count').reset_index()
    try:
        SC[i] = float(groupedCategories.loc[groupedCategories[1]== 'SC', 'Count'])/copiedPairNumber[i]
    except:
        SC[i] = 0
    try:
        CC[i] = float(groupedCategories.loc[groupedCategories[1]== 'CC', 'Count'])/copiedPairNumber[i]
    except:
        CC[i] = 0
    try:
        CN[i] = float(groupedCategories.loc[groupedCategories[1]== 'CN', 'Count'])/copiedPairNumber[i]
    except:
        CN[i] = 0

graphData = list(zip(fields, SC, CC, CN))
graphDataFrame = pd.DataFrame(graphData, columns=['Field','SC','CC','CN'])
graphDataFrame = graphDataFrame.sort_values('SC',axis=0,ascending=False).reset_index(drop=True)

fields = graphDataFrame['Field'].tolist()
SC = graphDataFrame['SC'].tolist()
CC = graphDataFrame['CC'].tolist()
CN = graphDataFrame['CN'].tolist()


fname = 'SC'
with open(fname,'w') as scfile:
    pickle.dump(SC,scfile)

fname = 'CC'
with open(fname,'w') as ccfile:
    pickle.dump(CC,ccfile)

fname = 'CN'
with open(fname,'w') as cnfile:
    pickle.dump(CN,cnfile)

fname = 'fieldNames'
with open(fname,'w') as fieldfile:
    pickle.dump(fields, fieldfile)




SC = pickle.load(open('SC','r'))
CC = pickle.load(open('CC','r'))
CN = pickle.load(open('CN','r'))
fields = pickle.load(open('fieldNames','r'))


numberOfGroupsYears = len(fields)
fig, ax = plt.subplots(figsize=(45,20))
index = np.arange(numberOfGroupsYears)
barWidth = .20
opacity = 1.0

rects1 = plt.bar(index, SC, barWidth, alpha=opacity, color='b', label='Self Copied')
rects2 = plt.bar(index, CC, barWidth, alpha=opacity, color='r', label='Copied and Cited')
rects3 = plt.bar(index, CN, barWidth, alpha=opacity, color='g', label='Copied and Not Cited')


plt.xlabel('Paper Fields')
plt.ylabel('Fraction of Citation Contexts Copied')
plt.title('Variation of Categories among Fields')
plt.xticks(index + barWidth, fields)
plt.legend()
# rcParams.update({'figure.autolayout': True})
plt.setp(ax.get_xticklabels(), rotation=90, fontsize=12)
# plt.tight_layout()
# plt.gcf().subplots_adjust(bottom=0.02)
plt.show()
print "Process Completed"
fig.savefig("Experiment-10.pdf")
plt.close(fig)


#########################################################################################################################




###################################### FIELD WISE DISTRIBUTION PIE CHART ###################################################

dic = pickle.load(open('fields200Fieldcount','r'))

fields = [0]*24
fieldDist = [0]*24

for i, key in enumerate(dic.keys()):
    fields[i] = key
    fieldDist[i] = dic[key]

total = pickle.load(open('fields200CCcount','r'))

print "Total Citation Contexts" + " " , total

fig, ax1 = plt.subplots()

ax1.pie(
    # using data total)arrests
    fieldDist,
    # with the labels being officer names
    labels=fields,
    # with no shadows
    shadow=True,
    # with colors
    # with one slide exploded out
    explode=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.15),
    # with the start angle at 90%
    startangle=90,
    # with the percent listed as a fraction
    autopct='%1.1f%%',
    )

ax1.axis('equal')

# View the plot
plt.tight_layout()
fig.savefig("fieldDist.pdf")
plt.closefig(fig)
##################################################################################################