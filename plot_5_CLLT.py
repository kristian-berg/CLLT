import numpy as np
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import re

# load the Monte Carlo results
pneo_global = pd.read_csv("data/TUM_pneo_global_100.csv", sep = ",", index_col = 0)

decs = range(1800,1910,10)

# the number of simulations is extracted from the dataframe
nr_sim = pneo_global.shape[0]

# this function draws the areas into which a given amount (conf) data fall.
# It takes as an argument a dataframe with a given number of simulations (df), x-values (x), a boundary (as a fraction of 1) (conf), a colour (col), and a plot (plot_x).
# the idea is to sort the actual values of the simulations for each decade;
# then we determine which values serve as lower and upper boundaries;
# and then to plot an area with these boundaries.
def conf_int(df, x, conf, col, plot_x):
    conf_max = int(round(nr_sim * conf -1))  # upper boundary. example: p = 0.9, nr_sim =1000. conf_max = 899. In an ascending list of values for each decade, the 899th of 1,000 values is the upper boundary (for p = 0.9)
    conf_min = nr_sim - conf_max -1  # lower boundary. example: nr_sim =1000. conf_min = 1000 - 899 -1 = 100

    df =  df.transpose()
    df.values.sort() # sort the values
    line = np.empty([2, len(df)], dtype= float) # set up an empty array that contains values for two lines.

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

fig = plt.figure(figsize = (6,3))
ax1 = fig.add_subplot(111)
plt.ylabel("$P_{neo}$", fontsize=16)

ax1.plot(list(pneo_global),pneo_global.mean(axis = 0, skipna =  True).values, linewidth = 0.7, color = "black")

ax1.set_title('Pneo -tum', style = 'italic', family =  'serif')

# proxy artists
p1 = mpatches.Rectangle((0, 0), 1, 1, fc="white", edgecolor = "dimgrey")
p5 = mpatches.Rectangle((0, 0), 1, 1, fc="lightgrey", edgecolor = "dimgrey")
p = mpatches.Rectangle((0, 0), 1, 1, fc=[0.6,0.6,0.6], edgecolor = "dimgrey")

ax1.legend([p,p5,p1], ["p > 0.05", "p < 0.05", "p < 0.01"], loc = 4)

ax1.grid()

ax1.set_ylim(0,0.5)

ax1.set_xlim(1800,1900)

conf_int(pneo_global, decs, 0.98, 'grey', ax1)
conf_int(pneo_global, decs, 0.9,'dimgrey', ax1)

fig.tight_layout(pad = 2)
fig.savefig('plots/plot_5_pneo_tum.png', dpi=1200)