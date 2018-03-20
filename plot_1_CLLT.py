import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pylab import *

#  load Monte Carlo results and a list of texts from the DTA corpus which contains, for each text, a list of distinct types in that text
types_tokens_total = pd.read_csv("data/isch_types_over_tokens_total.csv", sep = ",", index_col  = 0)
texts = pd.read_csv('data/isch_texts_dta.csv', sep= ',')

decs = range(1800,1900,10)
xnew = np.arange(0, 15000000, 100000)

# this function returns the number of distinct words per decade
def extract_sets(series):
    result = set()
    for st in series:
        result = result | eval(st)
    return len(result)

types_tokens_total[types_tokens_total < 0] = 0

running_words_dec = pd.pivot_table(texts, index = "Dekade", values = "Freq", aggfunc=np.sum)

types_dec = np.empty([len(decs), 1], dtype= int)
for i in range(len(decs)):
    types_dec[i,0] = extract_sets(texts.loc[texts["Dekade"] == decs[i],"Types"])

nr_sim = types_tokens_total.shape[0]

# this function draws the areas into which a given amount (conf) data fall.
# It takes as an argument a dataframe with a given number of simulations (df), x-values (x), a boundary (as a fraction of 1) (conf), a colour (col), and a plot (plot_x).
# the idea is to sort the actual values of the simulations for each decade;
# then we determine which values serve as lower and upper boundaries;
# and then to plot an area with these boundaries.
def conf_int(df, x, conf, col, plot_x):
    conf_max = int(round(nr_sim * conf -1))  # upper boundary. example: p = 0.9, nr_sim =1000. conf_max = 899. In an ascending list of values for each decade, the 899th of 1,000 values is the upper boundary (for p = 0.9)
    conf_min = nr_sim - conf_max - 1  # lower boundary. example: nr_sim =1000. conf_min = 1000 - 899 -1 = 100

    df =  df.transpose()
    df.values.sort() # sort the values
    line = np.empty([2, len(df)], dtype= int) # set up an empty array that contains values for two lines.

    inx = 0 #set up counter to specify row number
    for row in df.iterrows():
        if conf_max <= 0: # if conf_max is equal to or below zero, there is no boundary
            line[0,inx] = None
            line[1,inx] = None
        else:   # if conf_max is above zero, the line values (upper and lower boundaries) are simply the conf_max-th and conf_min-th value of all simulation values for each decade
            line[0,inx] = df.iloc[inx,conf_min]
            line[1,inx] = df.iloc[inx,conf_max]
        inx +=1

    plot_x.fill_between(x,  line[0,:], line[1,:], facecolor=col, alpha='0.5') # fill the area that is enclosed by the lines

# set up plot
fig = plt.figure(figsize = (6,6))
ax1 = fig.add_subplot(111)

# draw a line of the mean values
ax1.plot(xnew, types_tokens_total.mean(axis = 0), linewidth = 0.7, color = "black")

# draw points for the actual values
ax1.plot(running_words_dec, types_dec, '.', c = "black")

# set title and labels
ax1.set_title('-isch', style = 'italic', family =  'serif')
plt.ylabel("Types", fontsize=12)
plt.xlabel("Running words (millions)", fontsize=12)

# add grid
ax1.grid()

# set y-axis limit
ax1.set_ylim(0,2000)

# set x-axis limit and convert the ticks to millions of running words
ax1.set_xlim(0,14000000)
locs,labels = xticks()
xticks(locs, map(lambda x: "%g" % x, locs/1000000))

# add boundaries for 98% and 90% of the data; that means 1%/5% of the data are above the upper boundary, 1%/5% are below the lower boundary
conf_int(types_tokens_total, xnew, 0.98, 'grey', ax1)
conf_int(types_tokens_total, xnew, 0.90, 'dimgrey', ax1)

# proxy artists
p1 = mpatches.Rectangle((0, 0), 1, 1, fc="white", edgecolor = "dimgrey")
p5 = mpatches.Rectangle((0, 0), 1, 1, fc="lightgrey", edgecolor = "dimgrey")
p = mpatches.Rectangle((0, 0), 1, 1, fc=[0.6,0.6,0.6], edgecolor = "dimgrey")

# add legend
ax1.legend([p,p5,p1], ["p > 0.05", "p < 0.05", "p < 0.01"], loc = 4)

# labels for the points
for i in [0,3,4]:
    ax1.annotate(decs[i], (running_words_dec.loc[decs[i],'Freq'], types_dec[i]),
    xytext=(0, -20), textcoords='offset points', ha='center', va='top',
    bbox=dict(fc='white', alpha=0.5),
    arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

for i in [8,9]:
    ax1.annotate(decs[i], (running_words_dec.loc[decs[i],'Freq'], types_dec[i]),
    xytext=(0, 20), textcoords='offset points', ha='center', va='bottom',
    bbox=dict(fc='white', alpha=0.5),
    arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

ax1.annotate(decs[1], (running_words_dec.loc[decs[1],'Freq'], types_dec[1]),
xytext=(20, -20), textcoords='offset points', ha='left', va='top',
bbox=dict(fc='white', alpha=0.5),
arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

ax1.annotate(decs[2], (running_words_dec.loc[decs[2],'Freq'], types_dec[2]),
xytext=(-20, 20), textcoords='offset points', ha='right', va='bottom',
bbox=dict(fc='white', alpha=0.5),
arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

ax1.annotate(decs[5], (running_words_dec.loc[decs[5],'Freq'], types_dec[5]),
xytext=(30, -10), textcoords='offset points', ha='left', va='top',
bbox=dict(fc='white', alpha=0.5),
arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

ax1.annotate(decs[6], (running_words_dec.loc[decs[6],'Freq'], types_dec[6]),
xytext=(10, -20), textcoords='offset points', ha='left', va='top',
bbox=dict(fc='white', alpha=0.5),
arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

ax1.annotate(decs[7], (running_words_dec.loc[decs[7],'Freq'], types_dec[6]),
xytext=(-20, 20), textcoords='offset points', ha='center', va='bottom',
bbox=dict(fc='white', alpha=0.5),
arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

# tighten layout and save
fig.tight_layout(pad = 2)
fig.savefig('plots/säily_plot_isch.png', dpi=1200)
