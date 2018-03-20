# Monte Carlo simulation for to determine the productivity of word formation patterns
# Kristian Berg, 2018
# kristian.berg@uni-oldenburg.de
# This script applies Säily's (2016) method of gauging the productivity by comparing the actual vocabulary real_size
# to a randomly re-sampled corpus.
# to speed things up, the corpus is resampled many times, but we shuffle only the metadata. The search was performed before;
# there is a list of tokens, and each token comes with information about the text it occurs in
# this way, we can shuffle the corpus, and use the list of files that are in it at any given moment, and from this
# derive the amount of tokens in the corpus (without actually searching it).
# The output is a table with one line per iteration which contains the Pneo values and a list of filenames with a set of distinct words in this file.

import pandas as pd
import numpy as np
import pylab as pl
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from timeit import default_timer as timer

# Timer
start =  timer()

# Load list of files
texts_dta  = pd.read_csv('data/dta_texts_18c.csv', sep= ',') # this file includes the filename, the decade the text was printed, and the total tokens
isch_raw  = pd.read_csv('data/isch_18c.csv', sep = ";")            # this file includes a line for each pertinent -isch-token in the DTA corpus

nr_texts = len(texts_dta)  # extract the number of different texts in the corpus

# establish a list of a list of lemmas per text
# initialize variable
types_texts = []

# for each text:
for index, row in texts_dta.iterrows():
    types_texts.append(set(isch_raw.loc[isch_raw['Datei'] == row['Datei'],'Lemma'])) # extract the different -isch types in the text
texts_dta['Types'] = types_texts  # write the list of different -isch types into the dataframe

texts_dta.to_csv("data/isch_texts_dta.csv", encoding = "utf-8")   # save the dataframe

# set parameters
nr_sim = 100            # nr of simulations
decs = range(1800,1890,10) # the decades of interest

# initialize lists
result_types = np.empty([nr_sim, nr_texts+1], dtype= int)
result_tokens_total = np.empty([nr_sim, nr_texts+1], dtype= int)

# the first element in both lists is set to 0: the number of types at a corpus size of 0 tokens is, well, 0.
result_types[:,0] = 0
result_tokens_total[:,0] = 0

# this is where the actual computations happen.
# for each simulation:
for n in range(nr_sim):
    print("Nr. simulation: ", n)
    subcorpus = texts_dta.sample(frac = 1)    #shuffle the corpus
    types = set()                             #initialize local list of types
    tokens_total = 0                          #initialize local token count
    for m in range(nr_texts):                 # now read in the corpus, text by text. for each text in the corpus:
        tokens_total = tokens_total + subcorpus.iloc[m,0]   # add the token count of the text in question to the total token count
        types = types | subcorpus.iloc[m,3]                 # union of the set of types already there and the set of types in the new text
        result_tokens_total[n,m+1] = tokens_total           # hand over the token count to the global variable
        result_types[n,m+1] = len(types)                    # and do the same for the number of (distinct) types

result_types = pd.DataFrame(result_types)                   # turn ndarrays into dataframes
result_tokens_total = pd.DataFrame(result_tokens_total)

# we now have information about the corpus size and the number of types after each step of the sampling process.
# Yet the steps are not uniform: Sometimes the first text sampled is 100.000 tokens long, sometimes only 1.000.
# That means we have to interpolate the data. This is done in the following section.

# Determine intervals at which the number of types are interpolated
xnew = np.arange(0, 15000000, 100000)

# Initialize global variable
result_types_over_tokens_total = np.empty([result_types.shape[0], len(xnew)], dtype= int)

# and again, for each of these results
for p in range(result_types.shape[0]):
    print(p)
    y = result_types.iloc[p,:].values          # the y-values to interpolate from (the types)
    xt = result_tokens_total.iloc[p,:].values  # the x-values (the tokens)
    f = interp1d(xt, y)                        # linear interpolation function
    result_types_over_tokens_total[p,:] = f(xnew) # now compute the type values for the xnew intervals

result_types_over_tokens_total = pd.DataFrame(result_types_over_tokens_total)
result_types_over_tokens_total.to_csv("data/isch_types_over_tokens_total.csv", encoding = "utf-8")

end = timer()
print("time elapsed: ", end - start)
