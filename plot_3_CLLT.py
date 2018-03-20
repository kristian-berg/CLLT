# This script produces plot3 in my CLLT paper and computes Spearman's rho for the relation in question.

import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import interp1d
from scipy.stats import spearmanr

decs = range(1800,1900,10)
xnew = np.arange(0, 15000000, 100000)

def extract_sets(series):
    result = set()
    for st in series:
        result = result | eval(st)
    return len(result)

types_tokens_isch = pd.read_csv("data/isch_types_over_tokens_total.csv", sep = ",", index_col  = 0)
types_tokens_nis = pd.read_csv("data/nis_types_over_tokens_total.csv", sep = ",", index_col  = 0)
texts_isch = pd.read_csv('data/isch_texts_dta.csv', sep= ',')
texts_nis = pd.read_csv('data/nis_texts_dta.csv', sep= ',')

types_tokens_isch[types_tokens_isch < 0] = 0
types_tokens_nis[types_tokens_nis < 0] = 0

running_words_dec_isch = pd.pivot_table(texts_isch, index = "Dekade", values = "Freq", aggfunc=np.sum)
running_words_dec_nis = pd.pivot_table(texts_nis, index = "Dekade", values = "Freq", aggfunc=np.sum)

types_dec_isch = np.empty([len(decs), 1], dtype= int)
types_dec_nis = np.empty([len(decs), 1], dtype= int)

for i in range(len(decs)):
    types_dec_isch[i,0] = extract_sets(texts_isch.loc[texts_isch["Dekade"] == decs[i],"Types"])
    types_dec_nis[i,0] = extract_sets(texts_nis.loc[texts_nis["Dekade"] == decs[i],"Types"])

types_dec_isch = pd.DataFrame(types_dec_isch)
types_dec_nis = pd.DataFrame(types_dec_nis)

types_dec_isch.columns = ["types"]
types_dec_nis.columns = ["types"]

types_dec_isch["running_words"] = running_words_dec_isch["Freq"].values
types_dec_nis["running_words"] = running_words_dec_nis["Freq"].values

nr_sim = types_tokens_isch.shape[0]

##calculate distance for -isch
y = types_tokens_isch.mean(axis = 0)
f = interp1d(xnew, y)
types_dec_isch["mean_diff"] = types_dec_isch["types"] - f(types_dec_isch["running_words"])
types_dec_isch["running_words_cumulative"] = types_dec_isch["running_words"].rolling(10, 1).sum()

print("spearman's rho for -isch", spearmanr(types_dec_isch["mean_diff"],types_dec_isch["running_words_cumulative"]))

##calculate distance for -nis
y = types_tokens_nis.mean(axis = 0)
f = interp1d(xnew, y)
types_dec_nis["mean_diff"] = types_dec_nis["types"] - f(types_dec_nis["running_words"])
types_dec_nis["running_words_cumulative"] = types_dec_nis["running_words"].rolling(10, 1).sum()

print("spearman's rho for -nis", spearmanr(types_dec_nis["mean_diff"],types_dec_nis["running_words_cumulative"]))

# set up plot
fig = plt.figure(figsize = (10,5))

# plot 1: -isch
ax1 = fig.add_subplot(121)

# plot decades as points
ax1.plot(types_dec_isch["running_words_cumulative"],types_dec_isch["mean_diff"], '.', c = "black")

# specify labels and title
ax1.set_title('-isch', style = 'italic', family =  'serif')
plt.ylabel("Actual V - mean V (100,000 iterations)", fontsize=12)
plt.xlabel("Running words (millions), cumulative", fontsize=12)

# add grid
ax1.grid()
locs,labels = pl.xticks()
pl.xticks(locs, map(lambda x: "%g" % x, locs/1000000))

# annotate the plot
for i in range(len(decs)):
    ax1.annotate(decs[i], (types_dec_isch.loc[i,"running_words_cumulative"],types_dec_isch.loc[i,"mean_diff"]),
    xytext=(0, -12), textcoords='offset points', ha='center', va='top',
    arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

# set y-axis limit
ax1.set_ylim(-350,200)


# plot 2: -nis
ax2 = fig.add_subplot(122)

# specify labels and title
ax2.set_title('-nis', style = 'italic', family =  'serif')
plt.ylabel("Actual V - mean V (100,000 iterations)", fontsize=12)
plt.xlabel("Running words (millions), cumulative", fontsize=12)

# plot decades as points
ax2.plot(types_dec_nis["running_words_cumulative"],types_dec_nis["mean_diff"], '.', c = "black")

# add grid
ax2.grid()
locs,labels = pl.xticks()
pl.xticks(locs, map(lambda x: "%g" % x, locs/1000000))

# annotate the plot
for i in range(len(decs)):
    ax2.annotate(decs[i], (types_dec_nis.loc[i,"running_words_cumulative"],types_dec_nis.loc[i,"mean_diff"]),
    xytext=(0, -12), textcoords='offset points', ha='center', va='top',
    arrowprops=dict(arrowstyle = '-', connectionstyle='arc3,rad=0'))

# set y-axis limit
ax2.set_ylim(-13,4)

fig.tight_layout(pad = 2)
fig.savefig('plots/säily_plot_3_mean_V.png', dpi=1200)
