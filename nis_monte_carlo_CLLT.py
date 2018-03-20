# Monte Carlo simulation for the German word formation pattern -ieren
# The script randomly re-samples the corpus up to 4m words per decade ('target size')
# For each decade in each corpus version, the script determines a) the number of -nis types
# and b) the number of new -nis types
# The fraction of new -nis types and all -nis types ('pneo') is stored as a csv.

# import necessary libraries
import pandas as pd
import numpy as np
from itertools import compress
from timeit import default_timer as timer

# start the timer
start =  timer()

# read the necessary files:
texts_dta  = pd.read_csv('data/texts_dta.csv', sep= ',') # this file contains a line for each text in the corpus, together with the respective decade and the token count
suffix_raw  = pd.read_csv('data/nis.csv', sep = ";")       # this file contains a line for each -nis attestation in the corpus, together with the respective decade and filename

### set parameters
nr_sim = 100             # nr of simulations
decs = range(1490,1910,10) # decades in the corpus
decs_result = range(1800,1910,10) # decades of interest
target_size = 4000000      # maximum corpus size per decade

# from the metadata (texts_dta): extract a table with the total amount of tokens per decade
tokens_tot = pd.pivot_table(texts_dta, index = "Dekade", values = "Freq", aggfunc=np.sum)

# initialize list
pneo_global = pd.DataFrame(columns = decs_result)

# the following function takes a decade (int) as input and returns a list of files similar to texts_dta...
# ...if the real size in tokens exceeds the target size.
# if not, it returns the actual corpus
def shuffle_dec(decade, n):
    real_size = int(tokens_tot.loc[tokens_tot.index == decade]["Freq"])
    if real_size <= target_size:
        return texts_dta.loc[texts_dta.Dekade == decade]
    else:
        counter = 0
        nr_texts = len(texts_dta.loc[texts_dta.Dekade == decade])
        texts_dec = texts_dta.loc[texts_dta.Dekade == decade].sample(frac = 1)
        j = 1
        counter = 0
        while counter < target_size:
            counter = texts_dec.iloc[0:j,2].sum()
            j += 1
        return texts_dec.iloc[0:j,:]

# the following function finds the earliest attestation (the leftmost non-zero value in a series)
def find_min(series):
    mask = series > 0
    return(series.loc[mask].index[0])

# the following function returns (for a given decade) the number of lemmas that are not zero
def find_types(df, dec):
    if dec in df.columns.values:
        return np.nansum(df[dec] > 0)
    else:
        return 0

# this is the actual Monte Carlo simulation, with a for-loop running nr_sim times
for n in range(nr_sim):
    print("Simulation  ",n)

    # create a re-shuffled sub-corpus
    sub_corpus = pd.concat([shuffle_dec(dec, n) for dec in decs], axis=0)

    # create a new list of tokens that only includes texts that are in the new re-shuffled version
    suffix_sub = suffix_raw[suffix_raw['Datei'].isin(sub_corpus['Datei'])].loc[:,['Dekade', 'Lemma']]
    suffix_sub["Wert"] = 1

    # create a table in which the rows are lexemes and the columns are decades
    suffix_x = pd.pivot_table(suffix_sub, index = 'Lemma', columns = 'Dekade', aggfunc = 'count', fill_value=0)
    suffix_x.columns = list(suffix_x.columns.levels[1])

    # annotate for first occurrence: for each row (=lemma), find the decade of its first occurrence
    suffix_x["min"] = suffix_x.apply(find_min, axis = 1)

    # construct a new table with the number of 'min'-values for each decade of interest (how many -nis-words were new in each decade?)
    new_types_suffix = suffix_x["min"][suffix_x["min"] > 1790].value_counts().to_frame()

    # construct a new dataframe with the decades without new types
    filt = [dec not in new_types_suffix.index for dec in decs_result]
    ind = list(compress(list(decs_result), filt))
    values = [0] * len(ind)

    # merge this new dataframe with the existing one
    new_types_suffix = pd.concat([new_types_suffix, pd.DataFrame(values, index = ind, columns = ["min"])])

    # get the number of all types for each decade
    new_types_suffix["all_types"] = [find_types(suffix_x, dec) for dec in list(new_types_suffix.index)]

    # Pneo is simply the ratio of all types and new types
    new_types_suffix["pneo"] = new_types_suffix["min"]/new_types_suffix["all_types"]

    # for each value in the table: set the according value of the global dataframe
    for col, value in new_types_suffix["pneo"].iteritems():
        pneo_global.set_value(n, col, value)

# save dataframe
pneo_global.to_csv("data/NIS_pneo_global_100.csv", encoding = "utf-8")

end = timer()
print("time elapsed: ", end - start)
